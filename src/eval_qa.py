"""Evaluates Base 40, Unseen Set A, and Unseen Set B (reporting false refusals + unfiltered BM25/Dense/RRF ablation)."""
from typing import Dict, List
from src.data import CORPUS, EVAL_QUERIES, FEE_RECORDS, EvalQuery
from src.qa_engine import HybridCounsellorQA


def _score_subset(engine: HybridCounsellorQA, queries: List[EvalQuery]) -> Dict[str, str]:
    ans_total = 0
    r5_hits = 0
    mrr_sum = 0.0
    false_refusals = 0

    cited_total = 0
    cited_correct = 0

    drafted_total = 0
    faithful_total = 0

    unans_total = 0
    refusal_correct = 0

    for eq in queries:
        resp = engine.answer_question(eq.query)

        if resp.drafted:
            drafted_total += 1
            if resp.guard_passed:
                faithful_total += 1

        if eq.answerable:
            ans_total += 1
            if eq.expected_doc_id in resp.retrieved_doc_ids:
                r5_hits += 1
                mrr_sum += 1.0 / (resp.retrieved_doc_ids.index(eq.expected_doc_id) + 1)
            if resp.refused:
                false_refusals += 1
            elif resp.cited_doc_ids:
                cited_total += 1
                if resp.cited_doc_ids[0] == eq.expected_doc_id:
                    cited_correct += 1
        else:
            unans_total += 1
            if resp.refused:
                refusal_correct += 1

    return {
        "Recall@5 (Answerable)": f"{r5_hits}/{ans_total} ({r5_hits / max(1, ans_total):.3f})",
        "MRR (Answerable)": f"{mrr_sum / max(1, ans_total):.3f}",
        "Citation Precision": f"{cited_correct}/{cited_total} ({cited_correct / max(1, cited_total):.3f})",
        "Numeric Faithfulness (All Drafts)": f"{faithful_total}/{drafted_total} ({faithful_total / max(1, drafted_total):.3f})",
        "False Refusals (Answerable)": f"{false_refusals}/{ans_total} ({false_refusals / max(1, ans_total):.3f})",
        "Refusal Accuracy (Unanswerable)": f"{refusal_correct}/{unans_total} ({refusal_correct / max(1, unans_total):.3f})",
    }


def _eval_unfiltered_retrieval(engine: HybridCounsellorQA, queries: List[EvalQuery]) -> None:
    ans_queries = [q for q in queries if q.answerable and q.expected_doc_id is not None]
    stats = {"BM25-only": [0, 0.0], "Dense-only": [0, 0.0], "RRF-Fused": [0, 0.0]}

    for eq in ans_queries:
        b_ids, d_ids, f_ids = engine.retrieve_unfiltered_components(eq.query)
        for name, ranked in (("BM25-only", b_ids), ("Dense-only", d_ids), ("RRF-Fused", f_ids)):
            if ranked[0] == eq.expected_doc_id:
                stats[name][0] += 1
            if eq.expected_doc_id in ranked:
                stats[name][1] += 1.0 / (ranked.index(eq.expected_doc_id) + 1)

    n = len(ans_queries)
    print(f"\n=== UNFILTERED RETRIEVAL ABLATION ({n} ANSWERABLE QUERIES, NO METADATA FILTERS) ===")
    print(f"{'Method':<15} | {'Recall@1':<18} | {'MRR':<10}")
    print("-" * 48)
    for name, (r1, mrr) in stats.items():
        print(f"{name:<15} | {r1}/{n} ({r1 / n:.3f})     | {mrr / n:.3f}")


def run_qa_evaluation() -> None:
    engine = HybridCounsellorQA(CORPUS, FEE_RECORDS)
    base40 = [q for q in EVAL_QUERIES if q.split == "base40"]
    set_a = [q for q in EVAL_QUERIES if q.split == "unseen10_a"]
    set_b = [q for q in EVAL_QUERIES if q.split == "unseen10_b"]

    m_base = _score_subset(engine, base40)
    m_a = _score_subset(engine, set_a)
    m_b = _score_subset(engine, set_b)

    print("\n=== PART E2: COUNSELLOR ASSIST EVALUATION (QUERY-ONLY ALLOW-LIST INFERENCE, 60 QUESTIONS) ===")
    print(f"{'Metric':<35} | {'Base 40':<18} | {'Eval Set A (10)':<18} | {'Eval Set B (10)':<18}")
    print("-" * 98)
    for k in m_base:
        print(f"{k:<35} | {m_base[k]:<18} | {m_a[k]:<18} | {m_b[k]:<18}")

    _eval_unfiltered_retrieval(engine, EVAL_QUERIES)

    # Real failure produced by running the code (Q56 typo 'Hooghly Vally Medical Collage')
    fail_q = "Hooghly Vally Medical Collage 2026-27 management fee?"
    fail_resp = engine.answer_question(fail_q)
    print("\n--- REAL FAILURE PRODUCED BY RUNNING CODE (Q56) ---")
    print(f"Query          : {fail_q}")
    print(f"Inferred Scope : {fail_resp.scope}")
    print(f"Response       : {fail_resp.answer}")
    print(
        "Why It Failed  : Strict exact-phrase college matching failed on the user typo 'Vally ... Collage', "
        "leaving college=None and triggering a conservative false refusal even though dense retrieval finds DOC_WB_HVMC_26."
    )