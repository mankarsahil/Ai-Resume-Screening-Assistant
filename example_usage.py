"""Tiny usage example for the resume screening NLP foundation modules."""

from preprocessing import clean_text
from skills import extract_skills


def run_example():
    """Show the expected call sequence so the Flask/FastAPI layer can wire these helpers together."""

    sample_filename = "sample_resume.txt"
    sample_text = "Python developer with ML, SQL, Docker, and strong communication skills."

    cleaned_text = clean_text(sample_text)
    skills_found = extract_skills(cleaned_text)

    print("Cleaned text:")
    print(cleaned_text)
    print("\nSkills found:")
    print(skills_found)

    print("\nText extraction router example:")
    try:
        from text_extraction import extract_text

        extract_text(b"dummy", sample_filename)
    except ValueError as error:
        print(error)
    except ModuleNotFoundError as error:
        print("Install dependencies from requirements.txt before using text_extraction:")
        print(error)


if __name__ == "__main__":
    run_example()
