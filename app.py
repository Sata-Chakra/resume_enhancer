from flask import Flask, request, render_template_string
from resume_analyzer import extract_text_from_pdf, extract_text_from_docx, analyze_resume
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>AI Resume Enhancer</title></head>
<body style="font-family:Arial;padding:20px;">
    <h2>📄 Upload Your Resume for AI Feedback</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="resume" required>
        <button type="submit">Analyze</button>
    </form>
    {% if result %}
    <h3>🔍 Analysis Result</h3>
    <p><strong>Grammar Score:</strong> {{ result.grammar_score }}%</p>
    <p><strong>Matched Keywords:</strong> {{ result.matched_keywords }}</p>
    <p><strong>Suggestions:</strong></p>
    <ul>
        {% for suggestion in result.suggestions %}
        <li>{{ suggestion }}</li>
        {% endfor %}
    </ul>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files["resume"]
        if file:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            if file.filename.endswith(".pdf"):
                text = extract_text_from_pdf(path)
            elif file.filename.endswith(".docx"):
                text = extract_text_from_docx(path)
            elif file.filename.endswith(".txt"):
                text = file.read().decode('utf-8')
            else:
                return "Unsupported file format"

            result = analyze_resume(text)

    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
