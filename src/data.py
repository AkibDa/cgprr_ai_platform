"""Synthetic corpus with structured fee/bond records, 60 evaluation queries (restored original wording), and fictional Hirrx profiles."""
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class FeeRecord:
    record_id: str
    doc_id: str
    state: str
    college: str
    session_year: str
    quota: str  # management | state | government | private | open | aiq | deemed | all
    field: str  # tuition_fee | hostel_fee | bond_penalty | caution_deposit | security_deposit | seats
    amount: float
    unit: str   # INR | count
    text: str


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    state: str
    college: str
    session_year: str
    text: str


FEE_RECORDS: List[FeeRecord] = [
    # 1. Aravalli Institute of Medical Sciences (Haryana)
    FeeRecord("REC_01", "DOC_HR_AIMS_25", "Haryana", "Aravalli Institute of Medical Sciences", "2025-26", "management", "tuition_fee", 1800000.0, "INR",
              "Aravalli Institute of Medical Sciences Gurugram Haryana MBBS tuition fee for 2025-26 is INR 18,00,000 (18 lakh) under management quota."),
    FeeRecord("REC_02", "DOC_HR_AIMS_25", "Haryana", "Aravalli Institute of Medical Sciences", "2025-26", "state", "tuition_fee", 1250000.0, "INR",
              "Aravalli Institute of Medical Sciences Gurugram Haryana MBBS tuition fee for 2025-26 is INR 12,50,000 under state quota."),
    FeeRecord("REC_03", "DOC_HR_AIMS_26", "Haryana", "Aravalli Institute of Medical Sciences", "2026-27", "management", "tuition_fee", 1950000.0, "INR",
              "Aravalli Institute of Medical Sciences Gurugram Haryana MBBS tuition fee for 2026-27 is INR 19,50,000 (19.5 lakh) under management quota."),
    FeeRecord("REC_04", "DOC_HR_AIMS_26", "Haryana", "Aravalli Institute of Medical Sciences", "2026-27", "state", "tuition_fee", 1320000.0, "INR",
              "Aravalli Institute of Medical Sciences Gurugram Haryana MBBS tuition fee for 2026-27 is INR 13,20,000 under state quota."),

    # 2. Hooghly Valley Medical College (West Bengal)
    FeeRecord("REC_05", "DOC_WB_HVMC_25", "West Bengal", "Hooghly Valley Medical College", "2025-26", "management", "tuition_fee", 1400000.0, "INR",
              "Hooghly Valley Medical College Kolkata West Bengal MBBS tuition fee for 2025-26 is INR 14,00,000 (14 lakh) under management quota."),
    FeeRecord("REC_06", "DOC_WB_HVMC_25", "West Bengal", "Hooghly Valley Medical College", "2025-26", "state", "tuition_fee", 540000.0, "INR",
              "Hooghly Valley Medical College Kolkata West Bengal MBBS tuition fee for 2025-26 is INR 5,40,000 under state quota."),
    FeeRecord("REC_07", "DOC_WB_HVMC_26", "West Bengal", "Hooghly Valley Medical College", "2026-27", "management", "tuition_fee", 1525000.0, "INR",
              "Hooghly Valley Medical College Kolkata West Bengal MBBS tuition fee for 2026-27 is INR 15,25,000 under management quota."),
    FeeRecord("REC_08", "DOC_WB_HVMC_26", "West Bengal", "Hooghly Valley Medical College", "2026-27", "state", "tuition_fee", 590000.0, "INR",
              "Hooghly Valley Medical College Kolkata West Bengal MBBS tuition fee for 2026-27 is INR 5,90,000 under state quota."),

    # 3. Deccan Heritage Medical College (Karnataka)
    FeeRecord("REC_09", "DOC_KA_DHMC_25", "Karnataka", "Deccan Heritage Medical College", "2025-26", "private", "tuition_fee", 1092600.0, "INR",
              "Deccan Heritage Medical College Bengaluru Karnataka MBBS private quota fee for 2025-26 is INR 10,92,600 per annum."),
    FeeRecord("REC_10", "DOC_KA_DHMC_26", "Karnataka", "Deccan Heritage Medical College", "2026-27", "private", "tuition_fee", 1185000.0, "INR",
              "Deccan Heritage Medical College Bengaluru Karnataka MBBS private quota fee for 2026-27 is INR 11,85,000 per annum."),
    FeeRecord("REC_11", "DOC_KA_DHMC_26", "Karnataka", "Deccan Heritage Medical College", "2026-27", "all", "seats", 150.0, "count",
              "Deccan Heritage Medical College Bengaluru Karnataka approved intake for 2026-27 is 150 MBBS seats."),

    # 4. Cauvery Crest Medical College (Tamil Nadu)
    FeeRecord("REC_12", "DOC_TN_CCMC_25", "Tamil Nadu", "Cauvery Crest Medical College", "2025-26", "management", "tuition_fee", 1350000.0, "INR",
              "Cauvery Crest Medical College Coimbatore Tamil Nadu MBBS management quota fee for 2025-26 is INR 13,50,000."),
    FeeRecord("REC_13", "DOC_TN_CCMC_25", "Tamil Nadu", "Cauvery Crest Medical College", "2025-26", "government", "tuition_fee", 450000.0, "INR",
              "Cauvery Crest Medical College Coimbatore Tamil Nadu MBBS government quota fee for 2025-26 is INR 4,50,000."),
    FeeRecord("REC_14", "DOC_TN_CCMC_26", "Tamil Nadu", "Cauvery Crest Medical College", "2026-27", "management", "tuition_fee", 1475000.0, "INR",
              "Cauvery Crest Medical College Coimbatore Tamil Nadu MBBS management quota fee for 2026-27 is INR 14,75,000."),
    FeeRecord("REC_15", "DOC_TN_CCMC_26", "Tamil Nadu", "Cauvery Crest Medical College", "2026-27", "government", "tuition_fee", 485000.0, "INR",
              "Cauvery Crest Medical College Coimbatore Tamil Nadu MBBS government quota fee for 2026-27 is INR 4,85,000."),

    # 5. Sahyadri Beacon Medical College (Maharashtra)
    FeeRecord("REC_16", "DOC_MH_SBMC_25", "Maharashtra", "Sahyadri Beacon Medical College", "2025-26", "open", "tuition_fee", 1120000.0, "INR",
              "Sahyadri Beacon Medical College Mumbai Maharashtra MBBS open quota fee for 2025-26 is INR 11,20,000 per year."),
    FeeRecord("REC_17", "DOC_MH_SBMC_25", "Maharashtra", "Sahyadri Beacon Medical College", "2025-26", "all", "hostel_fee", 180000.0, "INR",
              "Sahyadri Beacon Medical College Mumbai Maharashtra annual hostel fee for 2025-26 is INR 1,80,000."),
    FeeRecord("REC_18", "DOC_MH_SBMC_26", "Maharashtra", "Sahyadri Beacon Medical College", "2026-27", "open", "tuition_fee", 1210000.0, "INR",
              "Sahyadri Beacon Medical College Mumbai Maharashtra MBBS open quota fee for 2026-27 is INR 12,10,000 per year."),
    FeeRecord("REC_19", "DOC_MH_SBMC_26", "Maharashtra", "Sahyadri Beacon Medical College", "2026-27", "all", "hostel_fee", 195000.0, "INR",
              "Sahyadri Beacon Medical College Mumbai Maharashtra annual hostel fee for 2026-27 is INR 1,95,000."),

    # 6. Mithila Frontier Medical College (Bihar)
    FeeRecord("REC_20", "DOC_BR_MFMC_25", "Bihar", "Mithila Frontier Medical College", "2025-26", "all", "tuition_fee", 935000.0, "INR",
              "Mithila Frontier Medical College Patna Bihar annual MBBS tuition fee for 2025-26 is INR 9,35,000 (9.35 lakh)."),
    FeeRecord("REC_21", "DOC_BR_MFMC_26", "Bihar", "Mithila Frontier Medical College", "2026-27", "all", "tuition_fee", 1015000.0, "INR",
              "Mithila Frontier Medical College Patna Bihar annual MBBS tuition fee for 2026-27 is INR 10,15,000 (10.15 lakh)."),
    FeeRecord("REC_22", "DOC_BR_MFMC_26", "Bihar", "Mithila Frontier Medical College", "2026-27", "all", "caution_deposit", 100000.0, "INR",
              "Mithila Frontier Medical College Patna Bihar refundable caution deposit for 2026-27 is INR 1,00,000."),

    # 4 State Bond Rules (2026-27)
    FeeRecord("REC_23", "DOC_BOND_HR_26", "Haryana", "Aravalli Institute of Medical Sciences", "2026-27", "all", "bond_penalty", 1000000.0, "INR",
              "Haryana private college service bond penalty for session 2026-27 at Aravalli Institute of Medical Sciences is INR 10,00,000 (10 lakh)."),
    FeeRecord("REC_24", "DOC_BOND_WB_26", "West Bengal", "Hooghly Valley Medical College", "2026-27", "all", "bond_penalty", 500000.0, "INR",
              "West Bengal MBBS seat discontinuation bond penalty for session 2026-27 at Hooghly Valley Medical College is INR 5,00,000 (5 lakh)."),
    FeeRecord("REC_25", "DOC_BOND_TN_26", "Tamil Nadu", "Cauvery Crest Medical College", "2026-27", "all", "bond_penalty", 500000.0, "INR",
              "Tamil Nadu rural service bond default penalty for session 2026-27 at Cauvery Crest Medical College is INR 5,00,000 (5 lakh)."),
    FeeRecord("REC_26", "DOC_BOND_MH_26", "Maharashtra", "Sahyadri Beacon Medical College", "2026-27", "all", "bond_penalty", 1000000.0, "INR",
              "Maharashtra rural service bond penalty for session 2026-27 at Sahyadri Beacon Medical College is INR 10,00,000 (10 lakh)."),

    # MCC Counselling Rules (2026-27)
    FeeRecord("REC_27", "DOC_MCC_01_26", "All India", "MCC", "2026-27", "deemed", "security_deposit", 200000.0, "INR",
              "MCC deemed university registration security deposit for session 2026-27 is INR 2,00,000 (2 lakh)."),
    FeeRecord("REC_28", "DOC_MCC_02_26", "All India", "MCC", "2026-27", "aiq", "security_deposit", 10000.0, "INR",
              "MCC general All India Quota registration security deposit for session 2026-27 is INR 10,000."),
]


CORPUS: List[Document] = [
    Document("DOC_HR_AIMS_25", "Aravalli Institute Fee Notice 2025-26", "Haryana", "Aravalli Institute of Medical Sciences", "2025-26",
             "Aravalli Institute of Medical Sciences Gurugram Haryana MBBS annual tuition fee for session 2025-26 is INR 18,00,000 (18 lakh) for management quota and INR 12,50,000 for state quota."),
    Document("DOC_HR_AIMS_26", "Aravalli Institute Fee Notice 2026-27", "Haryana", "Aravalli Institute of Medical Sciences", "2026-27",
             "Aravalli Institute of Medical Sciences Gurugram Haryana MBBS annual tuition fee for session 2026-27 is INR 19,50,000 (19.5 lakh) for management quota and INR 13,20,000 for state quota."),
    Document("DOC_WB_HVMC_25", "Hooghly Valley Fee Notice 2025-26", "West Bengal", "Hooghly Valley Medical College", "2025-26",
             "Hooghly Valley Medical College Kolkata West Bengal MBBS tuition fee for 2025-26 is INR 14,00,000 (14 lakh) under management quota and INR 5,40,000 under state quota."),
    Document("DOC_WB_HVMC_26", "Hooghly Valley Fee Notice 2026-27", "West Bengal", "Hooghly Valley Medical College", "2026-27",
             "Hooghly Valley Medical College Kolkata West Bengal MBBS tuition fee for 2026-27 is INR 15,25,000 under management quota and INR 5,90,000 under state quota."),
    Document("DOC_KA_DHMC_25", "Deccan Heritage Fee Gazette 2025-26", "Karnataka", "Deccan Heritage Medical College", "2025-26",
             "Deccan Heritage Medical College Bengaluru Karnataka MBBS private quota fee for 2025-26 is INR 10,92,600 per annum."),
    Document("DOC_KA_DHMC_26", "Deccan Heritage Fee Gazette 2026-27", "Karnataka", "Deccan Heritage Medical College", "2026-27",
             "Deccan Heritage Medical College Bengaluru Karnataka MBBS private quota fee for 2026-27 is INR 11,85,000 per annum with 150 total MBBS seats."),
    Document("DOC_TN_CCMC_25", "Cauvery Crest Fee Order 2025-26", "Tamil Nadu", "Cauvery Crest Medical College", "2025-26",
             "Cauvery Crest Medical College Coimbatore Tamil Nadu MBBS management quota fee for 2025-26 is INR 13,50,000 and government quota fee is INR 4,50,000."),
    Document("DOC_TN_CCMC_26", "Cauvery Crest Fee Order 2026-27", "Tamil Nadu", "Cauvery Crest Medical College", "2026-27",
             "Cauvery Crest Medical College Coimbatore Tamil Nadu MBBS management quota fee for 2026-27 is INR 14,75,000 and government quota fee is INR 4,85,000."),
    Document("DOC_MH_SBMC_25", "Sahyadri Beacon Fee Notice 2025-26", "Maharashtra", "Sahyadri Beacon Medical College", "2025-26",
             "Sahyadri Beacon Medical College Mumbai Maharashtra MBBS open quota fee for 2025-26 is INR 11,20,000 per year; hostel fee is INR 1,80,000."),
    Document("DOC_MH_SBMC_26", "Sahyadri Beacon Fee Notice 2026-27", "Maharashtra", "Sahyadri Beacon Medical College", "2026-27",
             "Sahyadri Beacon Medical College Mumbai Maharashtra MBBS open quota fee for 2026-27 is INR 12,10,000 per year; hostel fee is INR 1,95,000."),
    Document("DOC_BR_MFMC_25", "Mithila Frontier Fee Notice 2025-26", "Bihar", "Mithila Frontier Medical College", "2025-26",
             "Mithila Frontier Medical College Patna Bihar annual MBBS tuition fee for 2025-26 is INR 9,35,000 (9.35 lakh) with refundable caution deposit of INR 1,00,000."),
    Document("DOC_BR_MFMC_26", "Mithila Frontier Fee Notice 2026-27", "Bihar", "Mithila Frontier Medical College", "2026-27",
             "Mithila Frontier Medical College Patna Bihar annual MBBS tuition fee for 2026-27 is INR 10,15,000 (10.15 lakh) with refundable caution deposit of INR 1,00,000."),
    Document("DOC_BOND_HR_26", "Haryana Bond Rule 2026-27", "Haryana", "Aravalli Institute of Medical Sciences", "2026-27",
             "For session 2026-27, MBBS graduates from private medical colleges in Haryana including Aravalli Institute of Medical Sciences must execute a service bond of INR 10,00,000 (10 lakh)."),
    Document("DOC_BOND_WB_26", "West Bengal Bond Rule 2026-27", "West Bengal", "Hooghly Valley Medical College", "2026-27",
             "For session 2026-27, West Bengal MBBS seat discontinuation bond penalty at Hooghly Valley Medical College is INR 5,00,000 (5 lakh)."),
    Document("DOC_BOND_TN_26", "Tamil Nadu Bond Rule 2026-27", "Tamil Nadu", "Cauvery Crest Medical College", "2026-27",
             "For session 2026-27, Tamil Nadu rural service bond default penalty at Cauvery Crest Medical College is INR 5,00,000 (5 lakh)."),
    Document("DOC_BOND_MH_26", "Maharashtra Bond Rule 2026-27", "Maharashtra", "Sahyadri Beacon Medical College", "2026-27",
             "For session 2026-27, Maharashtra rural service bond penalty at Sahyadri Beacon Medical College is INR 10,00,000 (10 lakh)."),
    Document("DOC_MCC_01_26", "MCC Deemed Security Deposit 2026-27", "All India", "MCC", "2026-27",
             "MCC deemed university registration security deposit for session 2026-27 is INR 2,00,000 (2 lakh)."),
    Document("DOC_MCC_02_26", "MCC AIQ Security Deposit 2026-27", "All India", "MCC", "2026-27",
             "MCC general All India Quota registration security deposit for session 2026-27 is INR 10,000."),
    Document("DOC_NMC_01_26", "NMC Faculty Norms 2026-27", "All India", "NMC", "2026-27",
             "NMC 2026-27 MSR requires at least 1 Professor, 2 Associate Professors, and 3 Assistant Professors in General Medicine for 150 MBBS seats."),
    Document("DOC_NOISE_01", "Canteen Tariff Circular", "West Bengal", "Hooghly Valley Medical College", "2026-27",
             "Campus canteen lunch coupon costs INR 65 per meal."),
    Document("DOC_NOISE_02", "Library Overdue Fine Notice", "Haryana", "Aravalli Institute of Medical Sciences", "2026-27",
             "Central library late book return fine is INR 10 per day."),
    Document("DOC_NOISE_03", "Cultural Fest Registration", "Karnataka", "Deccan Heritage Medical College", "2026-27",
             "Annual student fest registration fee is INR 500 per team."),
    Document("DOC_NOISE_04", "Parking Pass Circular", "Maharashtra", "Sahyadri Beacon Medical College", "2026-27",
             "Annual two-wheeler parking pass costs INR 1,200."),
    Document("DOC_NOISE_05", "Blood Donation Drive", "Tamil Nadu", "Cauvery Crest Medical College", "2026-27",
             "Voluntary blood camp targets 300 units."),
    Document("DOC_NOISE_06", "Patna Office Holiday List", "Bihar", "CGPRR", "2026-27",
             "Patna office observes 14 holidays in 2026."),
    Document("DOC_NOISE_07", "Server Room Thermostat Log", "West Bengal", "WeAI Labs", "2026-27",
             "Server room AC is set to 20 degrees Celsius."),
    Document("DOC_NOISE_08", "Guest House Tariff", "Tamil Nadu", "Wehold Projects", "2026-27",
             "Guest house room tariff is INR 2,500 per night."),
    Document("DOC_NOISE_09", "Biometric Grace Period", "Bihar", "Mithila Frontier Medical College", "2026-27",
             "Biometric attendance grace period is 15 minutes."),
]


@dataclass(frozen=True)
class EvalQuery:
    qid: str
    query: str
    lang: str
    expected_doc_id: Optional[str]
    expected_amount: Optional[float]
    answerable: bool
    split: str  # "base40" | "unseen10_a" | "unseen10_b"


# 40 Base + 10 Unseen Set A + 10 Unseen Set B = 60 Queries (Original wordings restored for Q23,24,27,33,40,45-48)
EVAL_QUERIES: List[EvalQuery] = [
    # --- 40 Base Questions ---
    EvalQuery("Q01", "What is the 2026-27 MBBS management quota tuition fee at Aravalli Institute of Medical Sciences Haryana?", "en", "DOC_HR_AIMS_26", 1950000.0, True, "base40"),
    EvalQuery("Q02", "State quota tuition fee at Aravalli Institute of Medical Sciences in 2026-27?", "en", "DOC_HR_AIMS_26", 1320000.0, True, "base40"),
    EvalQuery("Q03", "What was Aravalli Institute of Medical Sciences management tuition fee in 2025-26?", "en", "DOC_HR_AIMS_25", 1800000.0, True, "base40"),
    EvalQuery("Q04", "What is the service bond penalty at Aravalli Institute of Medical Sciences Haryana for 2026-27?", "en", "DOC_BOND_HR_26", 1000000.0, True, "base40"),
    EvalQuery("Q05", "Hooghly Valley Medical College Kolkata 2026-27 management quota tuition fee?", "en", "DOC_WB_HVMC_26", 1525000.0, True, "base40"),
    EvalQuery("Q06", "Hooghly Valley Medical College state quota tuition fee for 2026-27?", "en", "DOC_WB_HVMC_26", 590000.0, True, "base40"),
    EvalQuery("Q07", "What was Hooghly Valley Medical College management tuition fee in 2025-26?", "en", "DOC_WB_HVMC_25", 1400000.0, True, "base40"),
    EvalQuery("Q08", "West Bengal MBBS discontinuation bond penalty in 2026-27 at Hooghly Valley Medical College?", "en", "DOC_BOND_WB_26", 500000.0, True, "base40"),
    EvalQuery("Q09", "Deccan Heritage Medical College private quota tuition fee for 2026-27?", "en", "DOC_KA_DHMC_26", 1185000.0, True, "base40"),
    EvalQuery("Q10", "Deccan Heritage Medical College private quota tuition fee in 2025-26?", "en", "DOC_KA_DHMC_25", 1092600.0, True, "base40"),
    EvalQuery("Q11", "Cauvery Crest Medical College management quota tuition fee 2026-27?", "en", "DOC_TN_CCMC_26", 1475000.0, True, "base40"),
    EvalQuery("Q12", "Cauvery Crest Medical College government quota tuition fee in 2026-27?", "en", "DOC_TN_CCMC_26", 485000.0, True, "base40"),
    EvalQuery("Q13", "Tamil Nadu rural service bond penalty for 2026-27 at Cauvery Crest Medical College?", "en", "DOC_BOND_TN_26", 500000.0, True, "base40"),
    EvalQuery("Q14", "Sahyadri Beacon Medical College Mumbai open quota tuition fee 2026-27?", "en", "DOC_MH_SBMC_26", 1210000.0, True, "base40"),
    EvalQuery("Q15", "Sahyadri Beacon Medical College hostel fee in 2026-27?", "en", "DOC_MH_SBMC_26", 195000.0, True, "base40"),
    EvalQuery("Q16", "Maharashtra rural service bond penalty for 2026-27 at Sahyadri Beacon Medical College?", "en", "DOC_BOND_MH_26", 1000000.0, True, "base40"),
    EvalQuery("Q17", "Mithila Frontier Medical College Bihar annual tuition fee 2026-27?", "en", "DOC_BR_MFMC_26", 1015000.0, True, "base40"),
    EvalQuery("Q18", "Mithila Frontier Medical College caution deposit in 2026-27?", "en", "DOC_BR_MFMC_26", 100000.0, True, "base40"),
    EvalQuery("Q19", "Mithila Frontier Medical College tuition fee in 2025-26?", "en", "DOC_BR_MFMC_25", 935000.0, True, "base40"),
    EvalQuery("Q20", "What is the MCC deemed university security deposit for 2026-27?", "en", "DOC_MCC_01_26", 200000.0, True, "base40"),
    EvalQuery("Q21", "What is the MCC general AIQ registration security deposit for 2026-27?", "en", "DOC_MCC_02_26", 10000.0, True, "base40"),
    EvalQuery("Q22", "How many MBBS seats are approved at Deccan Heritage Medical College in 2026-27?", "en", "DOC_KA_DHMC_26", 150.0, True, "base40"),
    # Romanised Hindi / Bengali (restored original short-name wording on Q23, Q24, Q27)
    EvalQuery("Q23", "Haryana Aravalli Institute mein 2026-27 ka bond penalty kitna lakh hai?", "hi_roman", "DOC_BOND_HR_26", 1000000.0, True, "base40"),
    EvalQuery("Q24", "Aravalli Institute Gurugram ka 2026-27 management tuition fee bataiye", "hi_roman", "DOC_HR_AIMS_26", 1950000.0, True, "base40"),
    EvalQuery("Q25", "Mithila Frontier Medical College Bihar ka 2026-27 tuition fee kitna rupaya hai?", "hi_roman", "DOC_BR_MFMC_26", 1015000.0, True, "base40"),
    EvalQuery("Q26", "MCC deemed university security deposit 2026-27 mein kitna lagta hai?", "hi_roman", "DOC_MCC_01_26", 200000.0, True, "base40"),
    EvalQuery("Q27", "Sahyadri Beacon Mumbai ka 2026-27 hostel fee kitna hai?", "hi_roman", "DOC_MH_SBMC_26", 195000.0, True, "base40"),
    EvalQuery("Q28", "Hooghly Valley Medical College Kolkata te 2026-27 management quota tuition fee koto?", "bn_roman", "DOC_WB_HVMC_26", 1525000.0, True, "base40"),
    EvalQuery("Q29", "West Bengal Hooghly Valley Medical College e 2026-27 bond penalty koto lakh?", "bn_roman", "DOC_BOND_WB_26", 500000.0, True, "base40"),
    EvalQuery("Q30", "Hooghly Valley Medical College state quota tuition fee 2026-27 bochore koto taka?", "bn_roman", "DOC_WB_HVMC_26", 590000.0, True, "base40"),
    EvalQuery("Q31", "Deccan Heritage Medical College 2026-27 private quota tuition fee koto?", "bn_roman", "DOC_KA_DHMC_26", 1185000.0, True, "base40"),
    # Unanswerable in base40 (restored original short-name wording on Q33, Q40)
    EvalQuery("Q32", "Hooghly Valley Medical College e NRI quota fee 2026-27 koto dollar?", "bn_roman", None, None, False, "base40"),
    EvalQuery("Q33", "Aravalli Institute ka 2026-27 NEET cutoff rank kya hai?", "hi_roman", None, None, False, "base40"),
    EvalQuery("Q34", "What is the 2026-27 MBBS tuition fee at Brahmaputra Valley Medical College?", "en", None, None, False, "base40"),
    EvalQuery("Q35", "What is the PG MD Radiology stipend at Deccan Heritage Medical College for 2026-27?", "en", None, None, False, "base40"),
    EvalQuery("Q36", "What is the NRI quota fee at Mithila Frontier Medical College for 2026-27?", "en", None, None, False, "base40"),
    EvalQuery("Q37", "What was the Round 1 closing NEET score for Cauvery Crest Medical College in 2026-27?", "en", None, None, False, "base40"),
    EvalQuery("Q38", "What is the bond penalty in Rajasthan private medical colleges for 2026-27?", "en", None, None, False, "base40"),
    EvalQuery("Q39", "What is the 2027-28 tuition fee at Sahyadri Beacon Medical College?", "en", None, None, False, "base40"),
    EvalQuery("Q40", "What is the tuition fee at Aravalli Institute in 2026-27?", "en", None, None, False, "base40"),

    # --- 10 Unseen Set A (Q41-Q50; restored original short-name wording on Q45-Q48) ---
    EvalQuery("Q41", "Cauvery Crest Medical College management quota tuition fee in 2025-26?", "en", "DOC_TN_CCMC_25", 1350000.0, True, "unseen10_a"),
    EvalQuery("Q42", "Cauvery Crest Medical College government quota tuition fee in 2025-26?", "en", "DOC_TN_CCMC_25", 450000.0, True, "unseen10_a"),
    EvalQuery("Q43", "Sahyadri Beacon Medical College open quota tuition fee in 2025-26?", "en", "DOC_MH_SBMC_25", 1120000.0, True, "unseen10_a"),
    EvalQuery("Q44", "Sahyadri Beacon Medical College hostel fee in 2025-26?", "en", "DOC_MH_SBMC_25", 180000.0, True, "unseen10_a"),
    EvalQuery("Q45", "Aravalli Institute state quota tuition fee in 2025-26?", "en", "DOC_HR_AIMS_25", 1250000.0, True, "unseen10_a"),
    EvalQuery("Q46", "Hooghly Valley state quota tuition fee in 2025-26?", "en", "DOC_WB_HVMC_25", 540000.0, True, "unseen10_a"),
    EvalQuery("Q47", "Cauvery Crest Coimbatore ka 2026-27 management tuition fee kitna hai?", "hi_roman", "DOC_TN_CCMC_26", 1475000.0, True, "unseen10_a"),
    EvalQuery("Q48", "Sahyadri Beacon Mumbai te 2026-27 bond penalty koto lakh?", "bn_roman", "DOC_BOND_MH_26", 1000000.0, True, "unseen10_a"),
    EvalQuery("Q49", "What is the 2026-27 library membership fee at Vindhya Crest Medical College?", "en", None, None, False, "unseen10_a"),
    EvalQuery("Q50", "What is the MBBS tuition fee at Hooghly Valley Medical College?", "en", None, None, False, "unseen10_a"),

    # --- 10 Unseen Set B (Q51-Q60: paraphrases, typos, near-miss colleges, unsupported qualifiers) ---
    EvalQuery("Q51", "What is the 2026-27 tuition fee at Aravalli Dental College Haryana?", "en", None, None, False, "unseen10_b"),
    EvalQuery("Q52", "Is the bond penalty refundable at Hooghly Valley Medical College for 2026-27?", "en", None, None, False, "unseen10_b"),
    EvalQuery("Q53", "What is the PG MD General Medicine tuition fee at Cauvery Crest Medical College for 2026-27?", "en", None, None, False, "unseen10_b"),
    EvalQuery("Q54", "What cutoff rank is needed for tuition fee waiver at Deccan Heritage Medical College in 2026-27?", "en", None, None, False, "unseen10_b"),
    EvalQuery("Q55", "Deccan Heritage Medical College Bengaluru annual fee for 2026-27 under private quota?", "en", "DOC_KA_DHMC_26", 1185000.0, True, "unseen10_b"),
    EvalQuery("Q56", "Hooghly Vally Medical Collage 2026-27 management fee?", "en", "DOC_WB_HVMC_26", 1525000.0, True, "unseen10_b"),
    EvalQuery("Q57", "How much do I pay to stay in hostel at Sahyadri Beacon Medical College in 2026-27?", "en", "DOC_MH_SBMC_26", 195000.0, True, "unseen10_b"),
    EvalQuery("Q58", "Mithila Frontier Institute of Technology Patna 2026-27 tuition fee?", "en", None, None, False, "unseen10_b"),
    EvalQuery("Q59", "What is the 2026-27 caution money at Mithila Frontier Medical College?", "en", "DOC_BR_MFMC_26", 100000.0, True, "unseen10_b"),
    EvalQuery("Q60", "Cauvery Crest Medical College 2026-27 govt seat kharcha kitna hai?", "hi_roman", "DOC_TN_CCMC_26", 485000.0, True, "unseen10_b"),
]


@dataclass(frozen=True)
class JobDescription:
    jd_id: str
    title: str
    hospital: str
    city: str
    specialty: str
    min_exp_years: int
    required_degree: str
    keywords: List[str]


@dataclass(frozen=True)
class DoctorResume:
    cand_id: str
    name: str
    region_group: str
    degree: str
    specialty: str
    clinical_exp_years: int
    gap_months: int
    gap_reason: str
    skills: List[str]


JOBS: List[JobDescription] = [
    JobDescription("JD01", "Senior ICU Intensivist", "Eastern Star Multispeciality Hospital", "Kolkata", "Critical Care", 8, "MD", ["ICU", "ventilator", "sepsis", "ECMO", "critical care"]),
    JobDescription("JD02", "Associate Professor General Medicine", "Hooghly Valley Teaching Hospital", "Kolkata", "General Medicine", 5, "MD", ["teaching", "NMC", "outpatient", "internal medicine", "ward"]),
    JobDescription("JD03", "Consultant Emergency Medicine", "Coromandel Bay Trauma Centre", "Chennai", "Emergency Medicine", 4, "MD", ["trauma", "triage", "ACLS", "emergency", "resuscitation"]),
    JobDescription("JD04", "Assistant Professor Pediatrics", "Deccan Heritage Children Hospital", "Bengaluru", "Pediatrics", 2, "MD", ["NICU", "pediatric", "neonatal", "teaching", "immunization"]),
    JobDescription("JD05", "Consultant Anesthesiologist", "Aravalli Apex Surgical Institute", "Gurugram", "Anesthesiology", 6, "MD", ["cardiac anesthesia", "OT", "pain management", "intubation", "perioperative"]),
]


def build_synthetic_resumes() -> List[DoctorResume]:
    """Generate 30 deterministic fictional doctor resumes."""
    return [
        DoctorResume("DOC_CAND_01", "Dr. A. Sen", "Metro_Tier1", "MD", "Critical Care", 11, 12, "maternity_leave", ["ICU", "ventilator", "sepsis", "ECMO", "critical care"]),
        DoctorResume("DOC_CAND_02", "Dr. R. Nair", "Metro_Tier1", "MD", "Critical Care", 11, 0, "none", ["ICU", "ventilator", "sepsis", "ECMO", "critical care"]),
        DoctorResume("DOC_CAND_03", "Dr. P. Das", "NonMetro_Tier2", "MD", "Critical Care", 10, 8, "maternity_leave", ["ICU", "ventilator", "sepsis", "critical care"]),
        DoctorResume("DOC_CAND_04", "Dr. S. Kulkarni", "Metro_Tier1", "MD", "Critical Care", 9, 0, "none", ["ICU", "ventilator", "ECMO", "critical care"]),
        DoctorResume("DOC_CAND_05", "Dr. M. Khan", "NonMetro_Tier2", "MD", "Critical Care", 8, 0, "none", ["ICU", "sepsis", "critical care"]),
        DoctorResume("DOC_CAND_06", "Dr. V. Joshi", "NonMetro_Tier2", "MD", "Critical Care", 6, 0, "none", ["ICU", "ventilator"]),
        DoctorResume("DOC_CAND_07", "Dr. N. Bose", "Metro_Tier1", "MD", "General Medicine", 7, 6, "maternity_leave", ["teaching", "NMC", "outpatient", "internal medicine", "ward"]),
        DoctorResume("DOC_CAND_08", "Dr. K. Verma", "NonMetro_Tier2", "MD", "General Medicine", 7, 0, "none", ["teaching", "NMC", "outpatient", "internal medicine", "ward"]),
        DoctorResume("DOC_CAND_09", "Dr. T. Roy", "Metro_Tier1", "MD", "General Medicine", 6, 0, "none", ["teaching", "NMC", "internal medicine"]),
        DoctorResume("DOC_CAND_10", "Dr. B. Mishra", "NonMetro_Tier2", "MD", "General Medicine", 5, 0, "none", ["teaching", "outpatient", "ward"]),
        DoctorResume("DOC_CAND_11", "Dr. D. Sharma", "NonMetro_Tier2", "MD", "General Medicine", 4, 0, "none", ["outpatient", "ward"]),
        DoctorResume("DOC_CAND_12", "Dr. H. Patel", "Metro_Tier1", "MBBS", "General Medicine", 5, 0, "none", ["outpatient", "ward"]),
        DoctorResume("DOC_CAND_13", "Dr. L. Menon", "Metro_Tier1", "MD", "Emergency Medicine", 8, 9, "maternity_leave", ["trauma", "triage", "ACLS", "emergency", "resuscitation"]),
        DoctorResume("DOC_CAND_14", "Dr. G. Rao", "NonMetro_Tier2", "MD", "Emergency Medicine", 7, 0, "none", ["trauma", "triage", "ACLS", "emergency"]),
        DoctorResume("DOC_CAND_15", "Dr. C. Iyer", "Metro_Tier1", "MD", "Emergency Medicine", 5, 0, "none", ["trauma", "ACLS", "emergency"]),
        DoctorResume("DOC_CAND_16", "Dr. J. Chatterjee", "NonMetro_Tier2", "MD", "Emergency Medicine", 5, 0, "none", ["triage", "ACLS", "resuscitation"]),
        DoctorResume("DOC_CAND_17", "Dr. F. Alam", "NonMetro_Tier2", "MD", "Emergency Medicine", 4, 10, "unexplained", ["trauma", "emergency"]),
        DoctorResume("DOC_CAND_18", "Dr. E. Thomas", "Metro_Tier1", "MD", "Emergency Medicine", 3, 0, "none", ["triage", "ACLS"]),
        DoctorResume("DOC_CAND_19", "Dr. U. Banerjee", "NonMetro_Tier2", "MD", "Pediatrics", 6, 7, "maternity_leave", ["NICU", "pediatric", "neonatal", "teaching", "immunization"]),
        DoctorResume("DOC_CAND_20", "Dr. W. Gupta", "Metro_Tier1", "MD", "Pediatrics", 5, 0, "none", ["NICU", "pediatric", "neonatal", "teaching"]),
        DoctorResume("DOC_CAND_21", "Dr. Y. Reddy", "NonMetro_Tier2", "MD", "Pediatrics", 4, 0, "none", ["NICU", "pediatric", "immunization"]),
        DoctorResume("DOC_CAND_22", "Dr. Z. Shaikh", "Metro_Tier1", "MD", "Pediatrics", 3, 0, "none", ["pediatric", "teaching", "immunization"]),
        DoctorResume("DOC_CAND_23", "Dr. O. Pillai", "NonMetro_Tier2", "MD", "Pediatrics", 2, 0, "none", ["pediatric", "immunization"]),
        DoctorResume("DOC_CAND_24", "Dr. Q. Sinha", "NonMetro_Tier2", "DCH", "Pediatrics", 4, 0, "none", ["NICU", "pediatric"]),
        DoctorResume("DOC_CAND_25", "Dr. I. Mukherjee", "Metro_Tier1", "MD", "Anesthesiology", 9, 0, "none", ["cardiac anesthesia", "OT", "pain management", "intubation", "perioperative"]),
        DoctorResume("DOC_CAND_26", "Dr. A. Tiwari", "NonMetro_Tier2", "MD", "Anesthesiology", 8, 6, "maternity_leave", ["cardiac anesthesia", "OT", "intubation", "perioperative"]),
        DoctorResume("DOC_CAND_27", "Dr. S. Dutta", "Metro_Tier1", "MD", "Anesthesiology", 7, 0, "none", ["OT", "pain management", "intubation"]),
        DoctorResume("DOC_CAND_28", "Dr. R. Yadav", "NonMetro_Tier2", "MD", "Anesthesiology", 6, 0, "none", ["OT", "intubation", "perioperative"]),
        DoctorResume("DOC_CAND_29", "Dr. M. Hegde", "Metro_Tier1", "MD", "Anesthesiology", 5, 0, "none", ["pain management", "intubation"]),
        DoctorResume("DOC_CAND_30", "Dr. K. Mondal", "NonMetro_Tier2", "MD", "Anesthesiology", 4, 0, "none", ["OT", "intubation"]),
    ]