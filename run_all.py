"""Single-command entrypoint: runs pytest suite, 50-question QA evaluation, and Hirrx Match fairness audit."""
import subprocess
import sys
from src.eval_qa import run_qa_evaluation
from src.hirrx_matcher import run_hirrx_demo


def main() -> None:
    print("1/3 Running pytest unit tests...")
    res = subprocess.run([sys.executable, "-m", "pytest", "-v", "src/test_suite.py"])
    if res.returncode != 0:
        sys.exit(res.returncode)

    print("\n2/3 Running Counsellor Assist evaluation (40 base + 10 held-out unseen queries)...")
    run_qa_evaluation()

    print("\n3/3 Running Hirrx Match ranking and fairness audit...")
    run_hirrx_demo()


if __name__ == "__main__":
    main()