"""
Manages pre-built CV and cover letter templates per niche.
These avoid AI API calls — user writes them once, reuses forever.
"""

import shutil
from pathlib import Path


CVS_DIR           = Path("data/cvs")
COVER_LETTERS_DIR = Path("data/cover_letters")
BASE_CV_PATH      = Path("data/base_cv.yaml")


# ─── Niche CVs ────────────────────────────────────────────────────────────────

def niche_cv_path(niche_id: str) -> Path:
    return CVS_DIR / f"{niche_id}.yaml"


def niche_cv_exists(niche_id: str) -> bool:
    return niche_cv_path(niche_id).exists()


def load_niche_cv(niche_id: str) -> dict:
    import yaml
    path = niche_cv_path(niche_id)
    if not path.exists():
        raise FileNotFoundError(f"No hay CV para el nicho '{niche_id}' en {path}")
    with open(path) as f:
        return yaml.safe_load(f)


def create_niche_cv(niche_id: str) -> Path:
    """Copy base CV as starting point for a niche-specific CV."""
    CVS_DIR.mkdir(parents=True, exist_ok=True)
    dest = niche_cv_path(niche_id)
    if not BASE_CV_PATH.exists():
        raise FileNotFoundError("No se encontró data/base_cv.yaml")
    shutil.copy(BASE_CV_PATH, dest)
    return dest


def list_niche_cvs() -> list[str]:
    if not CVS_DIR.exists():
        return []
    return [p.stem for p in sorted(CVS_DIR.glob("*.yaml"))]


# ─── Cover letters ────────────────────────────────────────────────────────────

def cover_letter_path(niche_id: str | None) -> Path:
    if niche_id:
        return COVER_LETTERS_DIR / f"{niche_id}.txt"
    return COVER_LETTERS_DIR / "generic.txt"


def cover_letter_exists(niche_id: str | None) -> bool:
    return cover_letter_path(niche_id).exists()


def load_cover_letter(niche_id: str | None, company: str, position: str, candidate_name: str = "") -> str:
    """
    Load cover letter template and substitute variables.
    Tries niche-specific first, falls back to generic.
    Variables available: {company}, {position}, {name}
    """
    path = cover_letter_path(niche_id)
    if not path.exists() and niche_id:
        path = cover_letter_path(None)  # fallback to generic
    if not path.exists():
        raise FileNotFoundError(
            "No se encontró ninguna carta de presentación. "
            "Creá una con: python main.py cover-letter init"
        )

    template = path.read_text(encoding="utf-8")
    return template.format(
        company=company,
        position=position,
        name=candidate_name,
    )


def which_cover_letter(niche_id: str | None) -> tuple[Path, bool]:
    """Returns (path_used, is_niche_specific)."""
    niche_path = cover_letter_path(niche_id)
    if niche_id and niche_path.exists():
        return niche_path, True
    generic = cover_letter_path(None)
    return generic, False


def list_cover_letters() -> list[str]:
    if not COVER_LETTERS_DIR.exists():
        return []
    return [p.stem for p in sorted(COVER_LETTERS_DIR.glob("*.txt"))]
