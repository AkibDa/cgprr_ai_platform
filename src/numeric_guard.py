"""Record-level numeric guard: strips citation tags, parses Indian formats, and enforces exact quota/program scoping."""
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
from src.data import FeeRecord


@dataclass
class GuardResult:
    passed: bool
    extracted_numbers: List[float]
    unverified_numbers: List[float]
    reason: str


CITATION_TAG_RE = re.compile(r"\[[A-Z0-9_]+\]")
SESSION_RE = re.compile(r"\b(20\d{2})\s*[-–]\s*(\d{2})\b")

WORD_NUMBERS: Dict[str, float] = {
    "one": 1.0, "ek": 1.0,
    "two": 2.0, "do": 2.0, "dui": 2.0,
    "three": 3.0, "teen": 3.0, "tin": 3.0,
    "four": 4.0, "char": 4.0,
    "five": 5.0, "paanch": 5.0, "panch": 5.0,
    "six": 6.0, "chhe": 6.0, "choy": 6.0,
    "seven": 7.0, "saat": 7.0, "sat": 7.0,
    "eight": 8.0, "aath": 8.0, "aat": 8.0,
    "nine": 9.0, "nau": 9.0, "noy": 9.0,
    "ten": 10.0, "das": 10.0, "dosh": 10.0,
}

INDIAN_NUM_RE = re.compile(
    r"(?:INR|Rs\.?|₹)?\s*"
    r"(\d{1,3}(?:,\d{2})*(?:,\d{3})+|\d+(?:\.\d+)?|\b(?:" + "|".join(WORD_NUMBERS.keys()) + r")\b)"
    r"\s*(lakhs?|lacs?|l\b|crores?|cr\b)?",
    re.IGNORECASE,
)


def strip_citations(text: str) -> str:
    """Remove bracketed document IDs like [DOC_HR_AIMS_26] before extracting numeric claims."""
    return CITATION_TAG_RE.sub(" ", text)


def parse_indian_numbers(text: str) -> Set[float]:
    cleaned = strip_citations(text)
    values: Set[float] = set()

    def _mask_session(m: re.Match) -> str:
        y1 = int(m.group(1))
        y2 = int(str(y1)[:2] + m.group(2))
        values.add(float(y1))
        values.add(float(y2))
        return " SESSION_MASK "

    cleaned = SESSION_RE.sub(_mask_session, cleaned)

    for m in INDIAN_NUM_RE.finditer(cleaned):
        raw_token = m.group(1).lower().replace(",", "")
        unit = (m.group(2) or "").lower()

        if raw_token in WORD_NUMBERS:
            if not unit:
                continue
            val = WORD_NUMBERS[raw_token]
        else:
            try:
                val = float(raw_token)
            except ValueError:
                continue

        if unit in ("lakh", "lakhs", "lac", "lacs", "l"):
            val *= 100_000.0
        elif unit in ("crore", "crores", "cr"):
            val *= 10_000_000.0
        values.add(round(val, 4))

    return values


def verify_against_record(
    answer_text: str,
    cited_doc_ids: List[str],
    record: Optional[FeeRecord],
    expected_state: Optional[str],
    expected_college: Optional[str],
    expected_session_year: Optional[str],
    expected_quota: Optional[str],
    expected_field: Optional[str],
) -> GuardResult:
    """Verify every number in answer_text against the exact structured FeeRecord and query scope."""
    ans_nums = sorted(parse_indian_numbers(answer_text))
    if not ans_nums:
        return GuardResult(True, [], [], "No numeric claims in answer.")

    if not cited_doc_ids or record is None:
        return GuardResult(False, ans_nums, ans_nums, "Missing citation or matching structured record.")

    if record.doc_id not in cited_doc_ids:
        return GuardResult(False, ans_nums, ans_nums, f"Cited doc {cited_doc_ids} != record doc {record.doc_id}.")

    if expected_state and record.state.lower() != expected_state.lower() and record.state != "All India":
        return GuardResult(False, ans_nums, ans_nums, f"State mismatch: {record.state} != {expected_state}.")
    if expected_college and record.college.lower() != expected_college.lower():
        return GuardResult(False, ans_nums, ans_nums, f"College mismatch: {record.college} != {expected_college}.")
    if expected_session_year and record.session_year != expected_session_year:
        return GuardResult(False, ans_nums, ans_nums, f"Session year mismatch: {record.session_year} != {expected_session_year}.")

    # An 'all' quota record must NOT answer an explicitly unindexed quota (e.g., 'nri')
    if expected_quota:
        if record.quota == "all" and expected_quota not in ("all", "general", "mbbs"):
            return GuardResult(False, ans_nums, ans_nums, f"Record quota 'all' cannot satisfy specific unindexed quota '{expected_quota}'.")
        if record.quota != "all" and record.quota != expected_quota:
            return GuardResult(False, ans_nums, ans_nums, f"Quota mismatch: {record.quota} != {expected_quota}.")

    if expected_field and record.field != expected_field:
        return GuardResult(False, ans_nums, ans_nums, f"Field mismatch: {record.field} != {expected_field}.")

    allowed: Set[float] = {round(record.amount, 4)}
    allowed.update(parse_indian_numbers(record.session_year))

    unverified = [n for n in ans_nums if n not in allowed]
    if unverified:
        return GuardResult(
            False,
            ans_nums,
            unverified,
            f"Unverified numbers {unverified} do not match record {record.record_id} ({record.amount} {record.unit}).",
        )
    return GuardResult(True, ans_nums, [], "Verified against structured FeeRecord.")