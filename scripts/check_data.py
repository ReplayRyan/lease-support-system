import json
import spacy
import os
from spacy.training import offsets_to_biluo_tags

# Load a blank English model
nlp = spacy.blank("en")

# Ensure script finds the correct directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Moves up one level
data_path = os.path.join(BASE_DIR, "data", "training-data.json")

# Check if file exists before opening
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Training data file not found at: {data_path}")

# Load the dataset
with open(data_path, "r", encoding="utf-8") as f:
    training_data = json.load(f)

broken = []

for i, entry in enumerate(training_data):
    text = entry["text"]
    entities = [(ent["start"], ent["end"], ent["label"]) for ent in entry["entities"]]
    doc = nlp.make_doc(text)
    try:
        biluo = offsets_to_biluo_tags(doc, entities)
        if "-" in biluo:
            print(f"Misaligned Example {i}: {text}")
            print("Entities:")
            for start, end, label in entities:
                entity_text = text[start:end]
                print(f"  - Text: '{entity_text}', Start: {start}, End: {end}, Label: {label}")
            print("-" * 50)
            broken.append(i)
    except Exception as e:
        print(f"Crash in Example {i}: {e}")
        broken.append(i)

print(f"\nTotal broken examples: {len(broken)} out of {len(training_data)}")
