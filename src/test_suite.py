"""Pytest unit tests covering citation stripping, Indian formats, allow-list refusal edge cases, and candidate gap neutrality."""
from dataclasses import replace
from src.data import CORPUS, FEE_RECORDS, JOBS, build_synthetic_resumes
from src.hirrx_matcher import score_candidate
from src.numeric_guard import parse_indian_numbers, strip_citations, verify_against_record
from src.qa_engine import HybridCounsellorQA

REC_MAP = {r.record_id: r for r in FEE_RECORDS}
ENGINE = HybridCounsellorQA(CORPUS, FEE_RECORDS)


def test_citation_id_digits_stripped() -> None:
    text = "Bond penalty is INR 10 lakh [DOC_BOND_HR_26]."
    assert "DOC_BOND_HR_26" not in strip_citations(text)
    nums = parse_indian_numbers(text)
    assert nums == {1000000.0}
    assert 26.0 not in nums


def test_indian_number_variants_parsed() -> None:
    assert 500000.0 in parse_indian_numbers("Penalty is five lakh rupees.")
    assert 500000.0 in parse_indian_numbers("Penalty is 5 lac.")
    assert 500000.0 in parse_indian_numbers("Penalty is 5L.")
    assert 500000.0 in parse_indian_numbers("Penalty is paanch lakh.")
    assert 500000.0 in parse_indian_numbers("Penalty is INR 5,00,000.")


def test_allowlist_refusals() -> None:
    must_refuse = [
        "What is the NRI quota fee at Mithila Frontier Medical College for 2026-27?",
        "What is the 2026-27 tuition fee at Aravalli Dental College Haryana?",
        "What cutoff rank is needed for tuition fee waiver at Deccan Heritage Medical College in 2026-27?",
        "What is the PG MD General Medicine tuition fee at Cauvery Crest Medical College for 2026-27?",
        "Is the bond penalty refundable at Hooghly Valley Medical College for 2026-27?",
        "What is the mess fee at Sahyadri Beacon Medical College for 2026-27?",
        "What is the exam fee at Aravalli Institute for 2026-27?",
        "What is the OBC quota tuition fee at Cauvery Crest Medical College for 2026-27?",
        "What is the BAMS tuition fee at Hooghly Valley Medical College for 2026-27?",
        "How many bond years apply at Aravalli Institute for 2026-27?",
        "What is the per semester tuition fee at Deccan Heritage Medical College for 2026-27?",
        "What is the total course fee at Mithila Frontier Medical College for 2026-27?",
        "Compare Aravalli Institute management tuition fee between 2025-26 and 2026-27?",
    ]
    for q in must_refuse:
        resp = ENGINE.answer_question(q)
        assert resp.refused, f"Expected refusal but answered: {q} -> {resp.answer}"


def test_unambiguous_short_name_and_all_quota_guard() -> None:
    ok_resp = ENGINE.answer_question("Aravalli Institute state quota tuition fee in 2025-26?")
    assert not ok_resp.refused
    assert "12,50,000" in ok_resp.answer

    rec = REC_MAP["REC_21"]  # Mithila Frontier 2026-27 quota='all'
    guard_res = verify_against_record(
        answer_text="Fee is INR 10,15,000 [DOC_BR_MFMC_26].",
        cited_doc_ids=["DOC_BR_MFMC_26"],
        record=rec,
        expected_state="Bihar",
        expected_college="Mithila Frontier Medical College",
        expected_session_year="2026-27",
        expected_quota="nri",
        expected_field="tuition_fee",
    )
    assert not guard_res.passed


def test_same_candidate_with_and_without_gap_identical_score() -> None:
    resumes = build_synthetic_resumes()
    base_cand = resumes[0]
    cand_with_maternity = replace(base_cand, gap_months=18, gap_reason="maternity_leave")
    cand_with_unexplained = replace(base_cand, gap_months=18, gap_reason="unexplained")
    cand_no_gap = replace(base_cand, gap_months=0, gap_reason="none")

    _, s_mat, _ = score_candidate(cand_with_maternity, JOBS[0])
    _, s_unexp, _ = score_candidate(cand_with_unexplained, JOBS[0])
    _, s_none, _ = score_candidate(cand_no_gap, JOBS[0])

    assert s_mat == s_none
    assert s_unexp == s_none