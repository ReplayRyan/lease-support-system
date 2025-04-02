import spacy

# Load trained NER model
model_path = "models/lease_ner_model"
nlp = spacy.load(model_path)

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

if __name__ == "__main__":
    test_text = "The lease starts on January 1, 2025, and ends on December 31, 2030. The monthly rent is $2,500."
    extracted_info = extract_entities(test_text)
    print(extracted_info)