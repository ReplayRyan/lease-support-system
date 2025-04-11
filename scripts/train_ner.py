import spacy
import json
import random
import os
from spacy.training import Example

# Load a blank English NLP model
nlp = spacy.blank("en")  
ner = nlp.add_pipe("ner")  # Add Named Entity Recognizer (NER) pipeline

# Define your custom entity labels
ner.add_label("LEASE_START_DATE")
ner.add_label("LEASE_END_DATE")
ner.add_label("MONTHLY_RENT")
ner.add_label("TERMINATION_FEE")
ner.add_label("RENT_AMOUNT")
ner.add_label("ESCALATION_RATE")
ner.add_label("PROPERTY_ADDRESS")
ner.add_label("SECURITY_DEPOSIT")

# Ensure correct path to training data
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_path = os.path.join(BASE_DIR, "data", "training-data.json")

# Load training data
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Training data file not found at: {data_path}")

with open(data_path, "r", encoding="utf-8") as f:
    TRAINING_DATA = json.load(f)

# Start training
optimizer = nlp.begin_training()
for epoch in range(30):
    random.shuffle(TRAINING_DATA)
    losses = {}

    for entry in TRAINING_DATA:
        entities = [(ent["start"], ent["end"], ent["label"]) for ent in entry["entities"]]
        example = Example.from_dict(nlp.make_doc(entry["text"]), {"entities": entities})
        nlp.update([example], losses=losses)

    print(f"Epoch {epoch + 1}, Loss: {losses}")

# Save the trained model
model_path = os.path.join(BASE_DIR, "models", "lease_ner_model")
nlp.to_disk(model_path)
print(f"Model training complete. Saved at {model_path}")
