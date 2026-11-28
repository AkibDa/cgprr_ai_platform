"""Hirrx Match prototype: deterministic eligibility, zero penalty for ANY gap, all-5-job ranked output, and Top-10 + Top-3 fairness audit."""
from dataclasses import dataclass
from typing import List, Tuple
from src.data import DoctorResume, JobDescription, JOBS, build_synthetic_resumes


@dataclass
class CandidateRank:
    rank: int
    cand_id: str
    name: str
    region_group: str
    eligible: bool
    score: float
    explanation: str


def score_candidate(cand: DoctorResume, jd: JobDescription) -> Tuple[bool, float, str]:
    """
    Deterministic eligibility and scoring.
    Employment gaps (maternity, medical, or unexplained) carry ZERO penalty.
    """
    if cand.specialty != jd.specialty:
        return False, 0.0, f"Ineligible: specialty '{cand.specialty}' != '{jd.specialty}'.\nExcluded by specialty rule."
    if jd.required_degree == "MD" and cand.degree != "MD":
        return False, 0.0, f"Ineligible: degree '{cand.degree}' < required '{jd.required_degree}'.\nExcluded by degree rule."

    exp_ratio = min(cand.clinical_exp_years / max(1, jd.min_exp_years), 1.5)
    exp_score = round((exp_ratio / 1.5) * 50.0, 2)

    cand_skills = {s.lower() for s in cand.skills}
    jd_skills = {s.lower() for s in jd.keywords}
    overlap = sorted(cand_skills.intersection(jd_skills))
    skill_score = round((len(overlap) / max(1, len(jd_skills))) * 50.0, 2)

    total_score = round(exp_score + skill_score, 2)
    line1 = f"Score {total_score}/100: {cand.clinical_exp_years} yrs {cand.specialty} ({cand.degree}); matched skills: {', '.join(overlap)}."
    line2 = "Eligibility criteria met; employment gaps excluded from scoring."
    return True, total_score, f"{line1}\n{line2}"


def rank_job(jd: JobDescription, resumes: List[DoctorResume]) -> List[CandidateRank]:
    rows: List[Tuple[bool, float, str, DoctorResume]] = []
    for cand in resumes:
        elig, sc, expl = score_candidate(cand, jd)
        rows.append((elig, sc, expl, cand))
    rows.sort(key=lambda x: (not x[0], -x[1], x[3].cand_id))
    return [
        CandidateRank(idx + 1, c.cand_id, c.name, c.region_group, elig, sc, expl)
        for idx, (elig, sc, expl, c) in enumerate(rows)
    ]


def _calc_dir(pool: List[DoctorResume], selected: List[CandidateRank]) -> Tuple[float, float, float]:
    p_non = sum(1 for c in pool if c.region_group == "NonMetro_Tier2") / max(1, len(pool))
    p_met = 1.0 - p_non
    s_non = sum(1 for r in selected if r.region_group == "NonMetro_Tier2") / max(1, len(selected))
    s_met = 1.0 - s_non
    dir_val = (s_non / max(1e-6, p_non)) / (s_met / max(1e-6, p_met))
    return p_non, s_non, dir_val


def run_hirrx_demo() -> None:
    resumes = build_synthetic_resumes()
    print("\n=== PART E3: HIRRX MATCH RANKED LISTS WITH 2-LINE EXPLANATIONS (ALL 5 JOBS) ===")
    for jd in JOBS:
        ranked = [r for r in rank_job(jd, resumes) if r.eligible]
        print(f"\n[{jd.jd_id}] {jd.title} — {jd.hospital} ({jd.city}) | Eligible: {len(ranked)}")
        for r in ranked:
            print(f"  #{r.rank} {r.name} ({r.cand_id}, {r.region_group}) -> {r.score} pts")
            for line in r.explanation.split("\n"):
                print(f"      {line}")

    print("\n=== PART E3: FAIRNESS REPORT (ELIGIBLE CANDIDATES ONLY — TOP-10 BRIEF METRIC & TOP-3 DIAGNOSTIC) ===")
    print("Caveat: With only 5-6 eligible candidates per job in this 30-resume dataset, Top-10 selects 100% of eligible candidates (degenerate DIR=1.00); Top-3 (~50-60% selection) is shown alongside, still subject to small-sample variance.")

    all_elig_pool: List[DoctorResume] = []
    all_top10: List[CandidateRank] = []
    all_top3: List[CandidateRank] = []

    for jd in JOBS:
        elig_pool = [c for c in resumes if score_candidate(c, jd)[0]]
        elig_ranked = [r for r in rank_job(jd, resumes) if r.eligible]
        top10 = elig_ranked[:10]
        top3 = elig_ranked[:3]

        all_elig_pool.extend(elig_pool)
        all_top10.extend(top10)
        all_top3.extend(top3)

        p10, s10, d10 = _calc_dir(elig_pool, top10)
        _, s3, d3 = _calc_dir(elig_pool, top3)
        print(f"{jd.jd_id} ({jd.specialty:<18}): Elig={len(elig_pool)} | Pool NonMetro={p10:.0%} | Top-10 NonMetro={s10:.0%} (DIR={d10:.2f}) | Top-3 NonMetro={s3:.0%} (DIR={d3:.2f})")

    ov_p, ov_s10, ov_d10 = _calc_dir(all_elig_pool, all_top10)
    _, ov_s3, ov_d3 = _calc_dir(all_elig_pool, all_top3)
    print(f"OVERALL ({len(all_elig_pool)} Eligible Pairs)  : Pool NonMetro={ov_p:.1%} | Top-10 NonMetro={ov_s10:.1%} (DIR={ov_d10:.3f}) | Top-3 NonMetro={ov_s3:.1%} (DIR={ov_d3:.3f})")