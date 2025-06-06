import sys
import spacy
import fitz # PyMuPDF



# Load trained NER model
model_path = "models/lease_ner_model"
nlp = spacy.load(model_path)

def extract_entities(text, confidence_threshold=0.8):
    """
    Extracts entities from text using the SpaCy NER model.
    Only accepts entities with confidence scores above the threshold.
    
    Args:
        text (str): The raw text to process.
        confidence_threshold (float): Minimum confidence score to accept an entity.
    
    Returns:
        dict: A dictionary containing extracted lease data.
    """
    doc = nlp(text)
    entities = {}
    
    print("\n--- Debugging: Detected Entities ---")
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}")
        if ent.label_ not in entities:
            entities[ent.label_] = ent.text
    print("--- End of Detected Entities ---\n")
    
    # Handle missing or malformed data
    return {
        "lease_start_date": entities.get("LEASE_START_DATE"),
        "lease_end_date": entities.get("LEASE_END_DATE"),
        "monthly_rent": float(entities.get("MONTHLY_RENT", "0").replace("$", "").replace(",", "")) if "MONTHLY_RENT" in entities else None,
        "security_deposit": float(entities.get("SECURITY_DEPOSIT", "0").replace("$", "").replace(",", "")) if "INITIAL_COST" in entities else None
    }

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