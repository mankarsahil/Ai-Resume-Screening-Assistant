<<<<<<< HEAD
from typing import List


def extract_skills(text: str) -> List[str]:
    if not text:
        return []

    tokens = [token for token in text.lower().replace("-", " ").split() if token]
    skill_keywords = [
        "python",
        "flask",
        "sql",
        "django",
        "java",
        "javascript",
        "react",
        "aws",
        "docker",
        "pandas",
        "numpy",
        "machine learning",
        "data analysis",
        "api",
        "rest",
        "git",
    ]

    found = []
    for skill in skill_keywords:
        if skill in " ".join(tokens):
            found.append(skill.title())
    return found
=======
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
    """Load the skill list and synonym map from JSON so they can be edited without changing code."""

    with SKILLS_FILE.open("r", encoding="utf-8") as skills_file:
        skills = json.load(skills_file)

    with SYNONYMS_FILE.open("r", encoding="utf-8") as synonyms_file:
        synonyms = json.load(synonyms_file)

    return skills, synonyms


def extract_skills(cleaned_text):
    """Find skills in cleaned resume text because the API needs a simple list of matched keywords."""

    skills, synonyms = load_skills()
    normalized_text = _normalize_phrase(cleaned_text)
    found_skills = []
    seen = set()

    for skill in skills:
        normalized_skill = _normalize_phrase(skill)
        if not normalized_skill:
            continue

        if re.search(rf"(?<!\w){re.escape(normalized_skill)}(?!\w)", normalized_text):
            if skill not in seen:
                found_skills.append(skill)
                seen.add(skill)

    for synonym, canonical_skill in synonyms.items():
        normalized_synonym = _normalize_phrase(synonym)
        if not normalized_synonym:
            continue

        if re.search(rf"(?<!\w){re.escape(normalized_synonym)}(?!\w)", normalized_text):
            if canonical_skill not in seen:
                found_skills.append(canonical_skill)
                seen.add(canonical_skill)

    return found_skills


if __name__ == "__main__":
    sample_text = "Experienced in Python, ML, Docker, K8s, communication, and project management."
    print("Loaded skills:", len(load_skills()[0]))
    print("Extracted skills:", extract_skills(sample_text))
>>>>>>> origin/main
