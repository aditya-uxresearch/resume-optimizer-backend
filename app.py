from flask import Flask, request, jsonify
import spacy
import subprocess

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading 'en_core_web_sm' model...")
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def analyze_job_description(job_description):
    doc = nlp(job_description)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return keywords

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    job_description = data.get("jobDescription")
    keywords = analyze_job_description(job_description)
    return jsonify({"keywords": keywords})

if __name__ == "__main__":
    app.run(debug=True)