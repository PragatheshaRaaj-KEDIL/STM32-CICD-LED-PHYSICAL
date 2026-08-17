import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CAPTURE = ROOT / "tests" / "saleae_capture.py"
ANALYZE = ROOT / "tests" / "analyze_saleae.py"


def run(cmd):
    print("\n" + "=" * 60)
    print("RUNNING:", " ".join(map(str, cmd)))
    print("=" * 60)

    result = subprocess.run(cmd, cwd=ROOT)

    if result.returncode != 0:
        sys.exit(result.returncode)


print("=" * 60)
print("STM32 PHYSICAL SALEAE TEST")
print("=" * 60)

print("Project:", ROOT)

if not CAPTURE.exists():
    raise FileNotFoundError(f"{CAPTURE} not found.")

if not ANALYZE.exists():
    raise FileNotFoundError(f"{ANALYZE} not found.")

run([sys.executable, str(CAPTURE)])
run([sys.executable, str(ANALYZE)])

print("\n" + "=" * 60)
print("PHYSICAL HARDWARE TEST PASSED")
print("=" * 60)