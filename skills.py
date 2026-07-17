"""Skill loading and extraction helpers for resume screening."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SKILLS_FILE = BASE_DIR / "skills_list.json"
SYNONYMS_FILE = BASE_DIR / "skill_synonyms.json"


def _normalize_phrase(value):
    """Convert a skill label or resume text into a simple lowercase phrase for matching."""
    normalized = re.sub(r"[^a-z0-9\s]", " ", str(value).lower())
    return re.sub(r"\s+", " ", normalized).strip()


@lru_cache(maxsize=1)
def load_skills():
    """Load skills and synonyms from JSON files."""
    with SKILLS_FILE.open("r", encoding="utf-8") as skills_file:
        skills = json.load(skills_file)

    with SYNONYMS_FILE.open("r", encoding="utf-8") as synonyms_file:
        synonyms = json.load(synonyms_file)

    return skills, synonyms


def extract_skills(cleaned_text):
    """Extract matching skills from cleaned resume text."""
    skills, synonyms = load_skills()
    normalized_text = _normalize_phrase(cleaned_text)
    found_skills = []
    seen = set()

    for skill in skills:
        normalized_skill = _normalize_phrase(skill)
        if normalized_skill and re.search(
            rf"(?<!\w){re.escape(normalized_skill)}(?!\w)", normalized_text
        ):
            if skill not in seen:
                found_skills.append(skill)
                seen.add(skill)

    for synonym, canonical_skill in synonyms.items():
        normalized_synonym = _normalize_phrase(synonym)
        if normalized_synonym and re.search(
            rf"(?<!\w){re.escape(normalized_synonym)}(?!\w)", normalized_text
        ):
            if canonical_skill not in seen:
                found_skills.append(canonical_skill)
                seen.add(canonical_skill)

    return found_skills


if __name__ == "__main__":
    sample_text = "Experienced in Python, ML, Docker, K8s, communication, and project management."
    print("Loaded skills:", len(load_skills()[0]))
    print("Extracted skills:", extract_skills(sample_text))