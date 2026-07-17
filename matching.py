from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing import clean_text


def compute_match_score(resume_text: str, jd_text: str) -> float:
    """Compute a simple text similarity score between a resume and a job description."""
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    documents = [resume_clean, jd_clean]

    # Alternative approach: fit a vectorizer on a larger resume corpus and reuse it for
    # every comparison. Pair-fitting is simpler and always available, but a corpus-fit
    # vectorizer usually produces more stable and comparable scores across resumes.
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(float(similarity * 100), 1)


def get_matching_and_missing_skills(resume_skills: List[str], jd_skills: List[str]) -> Tuple[List[str], List[str]]:
    """Return matching and missing skills using case-insensitive comparison."""
    resume_normalized = {skill.strip().lower(): skill.strip() for skill in resume_skills if skill and skill.strip()}
    jd_normalized = {skill.strip().lower(): skill.strip() for skill in jd_skills if skill and skill.strip()}

    matching = []
    for skill in jd_normalized:
        if skill in resume_normalized:
            matching.append(resume_normalized[skill].strip().title())

    missing = []
    for skill in jd_normalized:
        if skill not in resume_normalized:
            missing.append(jd_normalized[skill].strip().title())

    return matching, missing


def generate_suggestions(missing_skills: List[str], match_score: float) -> List[str]:
    """Generate a short list of improvement suggestions for the candidate resume."""
    suggestions = []

    top_missing = missing_skills[:3]
    for skill in top_missing:
        suggestions.append(
            f"Consider adding experience with {skill}, which appears in the job description but not your resume."
        )

    if match_score < 50:
        suggestions.append(
            "Tailor your resume more closely to the job description by mirroring its language and priorities."
        )

    if match_score >= 85:
        suggestions.append(
            "Strong match — consider a final proofread and keyword double-check before applying."
        )

    if len(suggestions) < 3:
        suggestions.append("Add a few more concrete examples of your relevant achievements to strengthen the application.")

    if len(suggestions) > 5:
        suggestions = suggestions[:5]

    return suggestions
