import sys
import spacy
import fitz # PyMuPDF

# Load trained NER model
model_path = "models/lease_ner_model"
nlp = spacy.load(model_path)

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

if __name__ == "__main__":
    if len(sys.argv) <2:
        print("Usage: python test_ner.py <path_to_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    pdf_text = extract_text_from_pdf(pdf_path)
    extracted_info = extract_entities(pdf_text)

    for entity_text, label in extracted_info:
        print(f"{entity_text} ({label})")

    # test_text = "The lease starts on January 1, 2025, and ends on December 31, 2030. The monthly rent is $2,500."
    # extracted_info = extract_entities(test_text)
    # print(extracted_info)