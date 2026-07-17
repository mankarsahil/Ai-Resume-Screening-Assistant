import os
from typing import Any, Dict, Optional
from preprocessing import clean_text
from skills import extract_skills
from text_extraction import extract_text
from flask import Flask, jsonify, request
from flask_cors import CORS

from classifier import load_classifier, predict_category
from matching import (
    compute_match_score,
    generate_suggestions,
    get_matching_and_missing_skills,
)
from preprocessing import clean_text
from skills import extract_skills
from text_extraction import extract_text


app = Flask(__name__)
CORS(app)

classifier = None


@app.before_request
def load_classifier_once():
    global classifier
    if classifier is None:
        classifier = load_classifier()


@app.route("/api/analyze", methods=["POST"])
def analyze_resume():
    resume_file = request.files.get("resume_file")
    job_description = request.form.get("job_description", "")

    if resume_file is None or resume_file.filename == "":
        return jsonify({"error": "Please upload a resume file."}), 400

    if not job_description or not job_description.strip():
        return jsonify({"error": "Please provide a job description."}), 400

    try:
        raw_resume_text = extract_text(resume_file.stream, resume_file.filename)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    cleaned_resume_text = clean_text(raw_resume_text)
    cleaned_jd_text = clean_text(job_description)

    resume_skills = extract_skills(cleaned_resume_text)
    jd_skills = extract_skills(cleaned_jd_text)

    match_score = compute_match_score(raw_resume_text, job_description)
    matching_skills, missing_skills = get_matching_and_missing_skills(resume_skills, jd_skills)
    suggestions = generate_suggestions(missing_skills, match_score)

    payload: Dict[str, Any] = {
        "match_score": match_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
    }

    if classifier is not None:
        model, vectorizer = classifier

        if model is not None and vectorizer is not None:
            try:
                category = predict_category(
                    cleaned_resume_text,
                    model,
                    vectorizer
                )
                payload["predicted_category"] = category
            except Exception as e:
                payload["prediction_error"] = str(e)

    return jsonify(payload)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
