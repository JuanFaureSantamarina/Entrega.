from pathlib import Path
import yaml

CATEGORIES_PATH = Path(__file__).resolve().parent.parent / "config" / "categories.yaml"


def load_categories() -> dict:
    if not CATEGORIES_PATH.exists():
        return {"income": [], "expense": []}
    with open(CATEGORIES_PATH) as f:
        data = yaml.safe_load(f) or {}
    return {"income": data.get("income", []), "expense": data.get("expense", [])}


def list_categories(kind: str) -> list:
    return load_categories().get(kind, [])
