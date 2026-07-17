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
