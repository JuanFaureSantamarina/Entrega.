import yaml
from pathlib import Path


NICHES_DIR = Path("config/niches")


def load_niche(niche_id: str) -> dict:
    path = NICHES_DIR / f"{niche_id}.yaml"
    if not path.exists():
        raise ValueError(f"Nicho '{niche_id}' no encontrado en {NICHES_DIR}")
    with open(path) as f:
        return yaml.safe_load(f)


def list_niches() -> list[dict]:
    niches = []
    if not NICHES_DIR.exists():
        return niches
    for path in sorted(NICHES_DIR.glob("*.yaml")):
        with open(path) as f:
            data = yaml.safe_load(f)
            data["id"] = path.stem
            niches.append(data)
    return niches


def detect_niche_from_description(job_description: str) -> str | None:
    """Simple keyword-based niche detection as fallback."""
    job_lower = job_description.lower()
    scores = {}
    for niche in list_niches():
        score = sum(1 for kw in niche.get("keywords", []) if kw.lower() in job_lower)
        if score > 0:
            scores[niche["id"]] = score
    if not scores:
        return None
    return max(scores, key=scores.get)
