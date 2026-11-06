"""Prepare the data/ folder used by all three notebooks.

Extracts the datasets bundled in Datasets.zip and downloads the small
LA "All City Funds" file used in the crime analysis.

    python setup_data.py
"""
import io
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
CITY_FUNDS_URL = "https://controllerdata.lacity.org/api/views/ej7u-di9z/rows.csv?accessType=DOWNLOAD"


def extract_datasets():
    with zipfile.ZipFile(ROOT / "Datasets.zip") as outer:
        for name in outer.namelist():
            if name.endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(outer.read(name))) as inner:
                    inner.extractall(DATA)
                print(f"extracted {Path(name).name}")


def download_city_funds():
    target = DATA / "All_City_Funds.csv"
    if target.exists():
        return
    urllib.request.urlretrieve(CITY_FUNDS_URL, target)
    print("downloaded All_City_Funds.csv")


if __name__ == "__main__":
    DATA.mkdir(exist_ok=True)
    extract_datasets()
    download_city_funds()
    for f in sorted(DATA.glob("*.csv")):
        print(f"  {f.name} ({f.stat().st_size / 1e6:.1f} MB)")
