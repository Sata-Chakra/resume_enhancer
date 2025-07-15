import nltk
import pdfplumber
from docx import Document
import re

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Keywords recruiters might be looking for
IMPORTANT_KEYWORDS = ['python', 'machine learning', 'data analysis', 'deep learning', 'aws', 'pandas']

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text.strip()

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_keywords(text):
    tokens = nltk.word_tokenize(text.lower())
    return [word for word in IMPORTANT_KEYWORDS if word in tokens]

def grammar_score(text):
    sentences = nltk.sent_tokenize(text)
    total = len(sentences)
    if total == 0:
        return 0
    grammar_errors = 0
    for s in sentences:
        tags = nltk.pos_tag(nltk.word_tokenize(s))
        if len(tags) < 3:
            grammar_errors += 1
    return round(100 * (1 - grammar_errors / total), 2)

def analyze_resume(text):
    keyword_matches = extract_keywords(text)
    score = grammar_score(text)
    suggestions = []

    if len(keyword_matches) < 3:
        suggestions.append("Consider adding more relevant technical keywords like 'Python', 'Pandas', 'AWS'.")

    if score < 70:
        suggestions.append("Improve grammar and sentence structure for better readability.")

    return {
        'grammar_score': score,
        'matched_keywords': keyword_matches,
        'suggestions': suggestions
    }
