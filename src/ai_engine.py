import os
import json
import urllib.request
import urllib.error
import yaml
from pathlib import Path


API_URL = "https://api.anthropic.com/v1/messages"


def _load_settings() -> dict:
    with open(Path("config/settings.yaml")) as f:
        return yaml.safe_load(f)


def _call_claude(prompt: str, max_tokens: int = 4096) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY no configurada. Agregala a tu archivo .env"
        )
    settings = _load_settings()
    payload = json.dumps({
        "model": settings["ai"]["model"],
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["content"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise RuntimeError(f"Error de API ({e.code}): {body}") from e


def tailor_cv(base_cv: dict, job_description: str, niche: dict) -> dict:
    """Use Claude to tailor the CV content for a specific job posting."""
    prompt = f"""Eres un experto en recursos humanos y redacción de CVs.
Tu tarea es adaptar el CV base al puesto específico de trabajo manteniendo toda la información real del candidato.

NICHO: {niche['name']}
TONO RECOMENDADO: {niche.get('tone', 'profesional')}
ÉNFASIS: {niche.get('emphasis', 'logros y experiencia')}

DESCRIPCIÓN DEL PUESTO:
{job_description}

CV BASE (en YAML):
{yaml.dump(base_cv, allow_unicode=True, default_flow_style=False)}

INSTRUCCIONES:
1. Reescribí el campo "summary" para que sea específico a este puesto (2-3 oraciones impactantes)
2. Reordenás o ajustá los logros en "experience" para destacar los más relevantes al puesto
3. Priorizá las skills más relevantes para este nicho y puesto
4. Adaptá las descripciones de experiencia para que resuenen con las palabras clave del puesto
5. NO inventes información, solo reorganizá y mejorá la redacción de lo existente
6. Mantené la estructura YAML exacta del CV base

Respondé ÚNICAMENTE con el YAML del CV adaptado, sin explicaciones adicionales ni bloques de código markdown.
El YAML debe comenzar directamente con "personal:" y ser válido."""

    raw = _call_claude(prompt)
    # Strip markdown code blocks if present
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:])
    if raw.endswith("```"):
        raw = raw[: raw.rfind("```")]
    return yaml.safe_load(raw.strip())


def generate_cover_letter(
    cv: dict,
    job_description: str,
    company: str,
    position: str,
    niche: dict,
) -> str:
    """Generate a cover letter tailored to the job posting."""
    candidate_name = cv.get("personal", {}).get("name", "El/la candidato/a")
    summary = cv.get("summary", "")
    experience_summary = ""
    for exp in cv.get("experience", [])[:2]:
        achievements = ", ".join(exp.get("achievements", [])[:2])
        experience_summary += f"- {exp['position']} en {exp['company']}: {achievements}\n"

    prompt = f"""Eres un experto en recursos humanos especializado en redacción de cartas de presentación.

Escribí una carta de presentación profesional y personalizada para:
- CANDIDATO: {candidate_name}
- EMPRESA: {company}
- PUESTO: {position}
- NICHO: {niche['name']}
- TONO: {niche.get('tone', 'profesional')}

RESUMEN PROFESIONAL DEL CANDIDATO:
{summary}

EXPERIENCIA DESTACADA:
{experience_summary}

DESCRIPCIÓN DEL PUESTO:
{job_description}

INSTRUCCIONES:
1. La carta debe tener 3-4 párrafos concisos
2. Párrafo 1: Presentación y por qué te interesa específicamente ESTA empresa y ESTE rol
3. Párrafo 2: Tu experiencia más relevante con logros concretos que se alineen al puesto
4. Párrafo 3: Por qué sos el candidato ideal y qué valor podés aportar
5. Párrafo 4 (cierre): Disponibilidad para entrevista y datos de contacto
6. Tono: {niche.get('tone', 'profesional')} pero humano y auténtico
7. Evitá frases genéricas como "soy un apasionado" o "trabajo muy bien en equipo"
8. Máximo 350 palabras
9. Escribí en primera persona, en español argentino

Respondé ÚNICAMENTE con el texto de la carta, sin asunto ni encabezado formal de email."""

    return _call_claude(prompt)


def suggest_niche(job_description: str, available_niches: list) -> str:
    """Ask Claude to identify the best niche for a job description."""
    niches_list = "\n".join(
        f"- {n['id']}: {n['name']} ({n['description']})"
        for n in available_niches
    )
    prompt = f"""Analizá la siguiente descripción de trabajo y determiná cuál de los nichos disponibles es el más apropiado.

NICHOS DISPONIBLES:
{niches_list}

DESCRIPCIÓN DEL PUESTO:
{job_description}

Respondé ÚNICAMENTE con el ID del nicho más apropiado (ej: "tech", "marketing", etc.).
Si ninguno aplica claramente, elegí el más cercano."""

    return _call_claude(prompt, max_tokens=50).strip('"').strip("'")
