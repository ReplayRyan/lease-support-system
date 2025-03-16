import spacy
import json
import random
import os
from spacy.training import Example

# Load the model
nlp = spacy.blank("en") # create blank Language class
ner = nlp.add_pipe("ner") # add NER pipe to the pipeline
ner.add_label("GPE") # add named entity label to NER

# Ensure script finds the correct directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Moves up one level
data_path = os.path.join(BASE_DIR, "data", "training-data.json")

# Check if file exists before opening
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Training data file not found at: {data_path}")

# Load the dataset
with open(data_path, "r", encoding="utf-8") as f:
    TRAINING_DATA = json.load(f)

# Start the training
optimizer = nlp.begin_training()
for epoch in range(30):
    random.shuffle(TRAINING_DATA)
    losses = {}
    
    for entry in TRAINING_DATA:
        example = Example.from_dict(nlp.make_doc(entry["text"]), {"entities": entry["entities"]})
        nlp.update([example], losses=losses)
    
    print(f"Epoch {epoch + 1}, Loss: {losses}")

# Save the model
model_path = "models/lease_ner_model"
nlp.to_disk(model_path)
print(f"Model training complete. Saved at {model_path}")
