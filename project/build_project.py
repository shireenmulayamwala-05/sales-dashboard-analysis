"""
Master build script — runs once and creates every project file.
"""
import os, shutil

BASE = "/Users/shireen/sales dashboard analysis /project"
SRC_CSV = "/Users/shireen/sales dashboard analysis /superstore.csv"

# ── copy raw data ──────────────────────────────────────────────────────────────
shutil.copy(SRC_CSV, os.path.join(BASE, "data", "superstore.csv"))
print("✓ Raw data copied")

# ── .gitignore ─────────────────────────────────────────────────────────────────
gitignore = """\
__pycache__/
*.pyc
.DS_Store
.env
*.ipynb_checkpoints
images/*.png
"""
with open(os.path.join(BASE, ".gitignore"), "w") as f:
    f.write(gitignore)
print("✓ .gitignore created")

# ── requirements.txt ───────────────────────────────────────────────────────────
req = """\
pandas==2.3.3
numpy>=1.24
matplotlib>=3.7
seaborn>=0.12
openpyxl>=3.1
sqlalchemy>=2.0
"""
with open(os.path.join(BASE, "requirements.txt"), "w") as f:
    f.write(req)
print("✓ requirements.txt created")

print("\nAll base files done. Run next scripts to build SQL, notebooks, reports.")
