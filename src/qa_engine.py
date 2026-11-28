"""Hybrid BM25 + Multilingual Sentence-Transformer Retrieval (paraphrase-multilingual-MiniLM-L12-v2, ~470 MB) with RRF and Strict Allow-List Scope Inference."""
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from src.data import Document, FeeRecord
from src.numeric_guard import verify_against_record

# Open-source multilingual embedding model (~470 MB download on first run; runs on CPU)
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


@dataclass
class InferredScope:
    state: Optional[str]
    college: Optional[str]
    session_year: Optional[str]
    quota: Optional[str]
    field: Optional[str]
    unmapped_tokens: List[str]
    refusal_reason: Optional[str]


@dataclass
class QAResponse:
    answer: str
    cited_doc_ids: List[str]
    retrieved_doc_ids: List[str]
    scope: InferredScope
    refused: bool
    drafted: bool
    guard_passed: bool
    guard_reason: str


# Unambiguous college aliases (longest match first) -> (Canonical College, State)
COLLEGE_ALIASES: List[Tuple[str, str, str]] = [
    ("aravalli institute of medical sciences", "Aravalli Institute of Medical Sciences", "Haryana"),
    ("aravalli institute", "Aravalli Institute of Medical Sciences", "Haryana"),
    ("hooghly valley medical college", "Hooghly Valley Medical College", "West Bengal"),
    ("hooghly valley", "Hooghly Valley Medical College", "West Bengal"),
    ("deccan heritage medical college", "Deccan Heritage Medical College", "Karnataka"),
    ("deccan heritage", "Deccan Heritage Medical College", "Karnataka"),
    ("cauvery crest medical college", "Cauvery Crest Medical College", "Tamil Nadu"),
    ("cauvery crest", "Cauvery Crest Medical College", "Tamil Nadu"),
    ("sahyadri beacon medical college", "Sahyadri Beacon Medical College", "Maharashtra"),
    ("sahyadri beacon", "Sahyadri Beacon Medical College", "Maharashtra"),
    ("mithila frontier medical college", "Mithila Frontier Medical College", "Bihar"),
    ("mithila frontier", "Mithila Frontier Medical College", "Bihar"),
    ("mcc", "MCC", "All India"),
]

# Near-miss institution keywords that disqualify short-name matches (e.g., 'Aravalli Dental College', 'Mithila Frontier Institute of Technology')
NEAR_MISS_INSTITUTION_WORDS: Set[str] = {
    "dental", "technology", "engineering", "pharmacy", "nursing", "ayurveda", "homoeopathy", "law", "management"
}

STATE_ALIASES: Dict[str, str] = {
    "haryana": "Haryana",
    "gurugram": "Haryana",
    "gurgaon": "Haryana",
    "west bengal": "West Bengal",
    "kolkata": "West Bengal",
    "karnataka": "Karnataka",
    "bengaluru": "Karnataka",
    "tamil nadu": "Tamil Nadu",
    "coimbatore": "Tamil Nadu",
    "maharashtra": "Maharashtra",
    "mumbai": "Maharashtra",
    "bihar": "Bihar",
    "patna": "Bihar",
}

# Strict allow-list of meaningful domain & Hindi/Bengali/English filler tokens.
# Any content token NOT matched by college, state, year, quota, field, or this allow-list causes refusal!
ALLOWED_TOKENS: Set[str] = {
    # English grammar / question / domain filler
    "what", "is", "the", "was", "for", "at", "in", "of", "to", "a", "an", "and", "or",
    "how", "many", "much", "do", "i", "pay", "stay", "are", "approved", "under", "annual",
    "per", "annum", "year", "session", "mbbs", "medical", "college", "institute", "sciences",
    "university", "registration", "general", "service", "discontinuation", "rural", "default",
    "seat", "seats", "intake", "quota", "fee", "fees", "tuition", "bond", "penalty",
    "hostel", "caution", "deposit", "money", "security", "management", "mgmt", "state",
    "government", "govt", "private", "open", "deemed", "aiq", "all", "india",
    # Romanised Hindi & Bengali question / grammar filler
    "mein", "ka", "ki", "ke", "ko", "se", "kitna", "kitni", "kitne", "kya", "hai", "hain",
    "bataiye", "batao", "lagta", "lagti", "rupaya", "rupees", "lakh", "lakhs", "lac", "lacs",
    "kharcha", "te", "e", "er", "koto", "bochore", "taka", "ar",
}


def infer_scope_from_query(query: str) -> InferredScope:
    """
    Allow-list scope parser: extracts (state, college, session_year, quota, field) from raw query text,
    and refuses unless EVERY meaningful token maps to a known entity, slot, or listed filler word.
    """
    q = query.lower()

    # 1. Check for multiple session years -> refuse
    years = re.findall(r"\b20\d{2}\s*[-–]\s*\d{2}\b", q)
    if len(years) != 1:
        reason = "Multiple session years in query." if len(years) > 1 else "Missing session year in query."
        return InferredScope(None, None, None, None, None, [], reason)
    session_year = years[0].replace(" ", "").replace("–", "-")

    # 2. Extract State
    state: Optional[str] = None
    for st_alias in sorted(STATE_ALIASES.keys(), key=len, reverse=True):
        if re.search(r"\b" + re.escape(st_alias) + r"\b", q):
            state = STATE_ALIASES[st_alias]
            break

    # 3. Extract College (unambiguous short names allowed ONLY when not followed by near-miss institution words)
    college: Optional[str] = None
    matched_college_phrase = ""
    for alias, col_name, col_state in COLLEGE_ALIASES:
        m = re.search(r"\b" + re.escape(alias) + r"\b", q)
        if m:
            # Check trailing words for near-miss institution types (e.g., 'Aravalli Dental College', 'Mithila Frontier Institute of Technology')
            after_text = q[m.end():].strip()
            after_tokens = re.findall(r"[a-z]+", after_text)[:3]
            if alias == "mcc":
                college = col_name
                matched_college_phrase = alias
                if state is None:
                    state = col_state
                break
            if any(w in NEAR_MISS_INSTITUTION_WORDS for w in after_tokens) and "medical" not in after_tokens:
                return InferredScope(state, None, session_year, None, None, after_tokens, f"Near-miss institution rejected after '{alias}'.")
            college = col_name
            matched_college_phrase = alias
            if state is None:
                state = col_state
            break

    if college is None:
        return InferredScope(state, None, session_year, None, None, [], "Unknown or unindexed college.")

    # 4. Extract Quota
    quota: Optional[str] = None
    if re.search(r"\b(management|mgmt)\b", q):
        quota = "management"
    elif re.search(r"\bstate quota\b", q) or (re.search(r"\bstate\b", q) and re.search(r"\b(tuition|fee|kharcha)\b", q)):
        quota = "state"
    elif re.search(r"\b(government|govt)\b", q):
        quota = "government"
    elif re.search(r"\bprivate quota\b", q):
        quota = "private"
    elif re.search(r"\bopen quota\b", q):
        quota = "open"
    elif re.search(r"\bdeemed\b", q):
        quota = "deemed"
    elif re.search(r"\b(aiq|all india)\b", q):
        quota = "aiq"

    # 5. Extract Field ('fee'/'tuition'/'kharcha' checked before 'seat')
    field: Optional[str] = None
    if re.search(r"\bbond\b", q):
        field = "bond_penalty"
    elif re.search(r"\bhostel\b", q):
        field = "hostel_fee"
    elif re.search(r"\bcaution\b", q):
        field = "caution_deposit"
    elif re.search(r"\bsecurity deposit\b", q):
        field = "security_deposit"
    elif re.search(r"\b(tuition|fee|fees|kharcha)\b", q):
        field = "tuition_fee"
    elif re.search(r"\b(seats?|intake)\b", q):
        field = "seats"

    # 6. Allow-list token coverage check: any unrecognized content word causes refusal!
    # Mask session year and matched college/state phrases before tokenizing
    residual = re.sub(r"\b20\d{2}\s*[-–]\s*\d{2}\b", " ", q)
    if matched_college_phrase:
        residual = re.sub(r"\b" + re.escape(matched_college_phrase) + r"\b", " ", residual)
    for st_alias in STATE_ALIASES:
        residual = re.sub(r"\b" + re.escape(st_alias) + r"\b", " ", residual)

    tokens = re.findall(r"[a-z0-9]+", residual)
    unmapped = [t for t in tokens if t not in ALLOWED_TOKENS]
    if unmapped:
        return InferredScope(
            state, college, session_year, quota, field, unmapped,
            f"Unmapped/unsupported terms in query: {unmapped}",
        )

    if field is None:
        return InferredScope(state, college, session_year, quota, None, [], "Missing target field in query.")

    return InferredScope(state, college, session_year, quota, field, [], None)


class HybridCounsellorQA:
    def __init__(self, documents: List[Document], records: List[FeeRecord]) -> None:
        self.documents = documents
        self.records = records
        corpus_texts = [f"{d.title} {d.state} {d.college} {d.session_year} {d.text}" for d in documents]

        tokenized = [re.findall(r"[a-zA-Z0-9\-]+", t.lower()) for t in corpus_texts]
        self.bm25 = BM25Okapi(tokenized)

        self.embedder = SentenceTransformer(EMBEDDING_MODEL_NAME, device="cpu")
        self.doc_embeddings = self.embedder.encode(corpus_texts, normalize_embeddings=True, show_progress_bar=False)

    def retrieve_unfiltered_components(self, query: str) -> Tuple[List[str], List[str], List[str]]:
        """Return ranked doc_ids for BM25-only, Dense-only, and RRF-fused WITHOUT metadata filters."""
        q_tokens = re.findall(r"[a-zA-Z0-9\-]+", query.lower())
        bm25_scores = self.bm25.get_scores(q_tokens)

        q_emb = self.embedder.encode([query], normalize_embeddings=True, show_progress_bar=False)[0]
        dense_scores = self.doc_embeddings @ q_emb

        n = len(self.documents)
        bm25_order = sorted(range(n), key=lambda i: bm25_scores[i], reverse=True)
        dense_order = sorted(range(n), key=lambda i: dense_scores[i], reverse=True)

        bm25_rank = {idx: r + 1 for r, idx in enumerate(bm25_order)}
        dense_rank = {idx: r + 1 for r, idx in enumerate(dense_order)}
        fused_order = sorted(
            range(n),
            key=lambda i: (1.0 / (60.0 + bm25_rank[i])) + (1.0 / (60.0 + dense_rank[i])),
            reverse=True,
        )

        return (
            [self.documents[i].doc_id for i in bm25_order],
            [self.documents[i].doc_id for i in dense_order],
            [self.documents[i].doc_id for i in fused_order],
        )

    def retrieve(self, query: str, scope: InferredScope, top_k: int = 5) -> List[Tuple[Document, float]]:
        q_tokens = re.findall(r"[a-zA-Z0-9\-]+", query.lower())
        bm25_scores = self.bm25.get_scores(q_tokens)

        q_emb = self.embedder.encode([query], normalize_embeddings=True, show_progress_bar=False)[0]
        dense_scores = self.doc_embeddings @ q_emb

        valid_indices: List[int] = []
        for idx, doc in enumerate(self.documents):
            if scope.session_year and doc.session_year != scope.session_year:
                continue
            if scope.state and doc.state.lower() != scope.state.lower() and doc.state != "All India":
                continue
            if scope.college and doc.college.lower() != scope.college.lower():
                continue
            valid_indices.append(idx)

        if not valid_indices:
            return []

        bm25_order = sorted(valid_indices, key=lambda i: bm25_scores[i], reverse=True)
        dense_order = sorted(valid_indices, key=lambda i: dense_scores[i], reverse=True)
        bm25_rank = {idx: r + 1 for r, idx in enumerate(bm25_order)}
        dense_rank = {idx: r + 1 for r, idx in enumerate(dense_order)}

        fused: List[Tuple[Document, float]] = []
        for idx in valid_indices:
            if dense_scores[idx] < 0.25 and bm25_scores[idx] <= 0.0:
                continue
            rrf = (1.0 / (60.0 + bm25_rank[idx])) + (1.0 / (60.0 + dense_rank[idx]))
            fused.append((self.documents[idx], rrf))

        fused.sort(key=lambda x: x[1], reverse=True)
        return fused[:top_k]

    def answer_question(self, query: str) -> QAResponse:
        scope = infer_scope_from_query(query)
        hits = self.retrieve(query, scope, top_k=5)
        retrieved_ids = [d.doc_id for d, _ in hits]

        if scope.refusal_reason is not None:
            return QAResponse(
                answer=f"REFUSAL: {scope.refusal_reason}",
                cited_doc_ids=[],
                retrieved_doc_ids=retrieved_ids,
                scope=scope,
                refused=True,
                drafted=False,
                guard_passed=True,
                guard_reason=scope.refusal_reason,
            )

        candidates = [
            r for r in self.records
            if r.college.lower() == (scope.college or "").lower()
            and r.session_year == scope.session_year
            and r.field == scope.field
        ]
        if scope.quota:
            candidates = [r for r in candidates if r.quota in (scope.quota, "all")]

        if len(candidates) != 1:
            return QAResponse(
                answer="REFUSAL: Ambiguous quota or no exact verified record for this college/session/field.",
                cited_doc_ids=[],
                retrieved_doc_ids=retrieved_ids,
                scope=scope,
                refused=True,
                drafted=False,
                guard_passed=True,
                guard_reason=f"Record match count = {len(candidates)} (requires exact 1).",
            )

        rec = candidates[0]
        if rec.doc_id not in retrieved_ids:
            return QAResponse(
                answer="REFUSAL: Matching record document failed retrieval confidence check.",
                cited_doc_ids=[],
                retrieved_doc_ids=retrieved_ids,
                scope=scope,
                refused=True,
                drafted=False,
                guard_passed=True,
                guard_reason="Record doc not in top-5 retrieved set.",
            )

        draft = f"{rec.text} [{rec.doc_id}]"
        guard = verify_against_record(
            answer_text=draft,
            cited_doc_ids=[rec.doc_id],
            record=rec,
            expected_state=scope.state,
            expected_college=scope.college,
            expected_session_year=scope.session_year,
            expected_quota=scope.quota,
            expected_field=scope.field,
        )
        if not guard.passed:
            return QAResponse(
                answer=f"REFUSAL (NUMERIC GUARD BLOCKED): {guard.reason}",
                cited_doc_ids=[],
                retrieved_doc_ids=retrieved_ids,
                scope=scope,
                refused=True,
                drafted=True,
                guard_passed=False,
                guard_reason=guard.reason,
            )

        return QAResponse(
            answer=draft,
            cited_doc_ids=[rec.doc_id],
            retrieved_doc_ids=retrieved_ids,
            scope=scope,
            refused=False,
            drafted=True,
            guard_passed=True,
            guard_reason=guard.reason,
        )