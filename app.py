from flask import Flask, render_template, request
import os
import PyPDF2
import docx

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"

# Extract text from PDF
def extract_text_from_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Extract text from DOCX
def extract_text_from_docx(path):
    doc = docx.Document(path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

# Core screening function
def calculate_match_score(resume_text, jd_text):
    resume_words = resume_text.lower().split()
    jd_words = jd_text.lower().split()

    matched = 0
    for w in jd_words:
        if w in resume_words:
            matched += 1

    score = (matched / len(jd_words)) * 100
    return round(score, 2)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        jd = request.form["jd"]

        file = request.files["resume"]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        if file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(filepath)
        else:
            resume_text = extract_text_from_docx(filepath)

        score = calculate_match_score(resume_text, jd)

        return render_template("index.html", score=score, resume_text=resume_text)

    return render_template("index.html", score=None)


if __name__ == "__main__":
    app.run(debug=True)