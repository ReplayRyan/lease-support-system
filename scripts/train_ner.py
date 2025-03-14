import spacy
import json
import random
from spacy.training import Example

# Load the model
nlp = spacy.blank("en") # create blank Language class
ner = nlp.add_pipe("ner") # add NER pipe to the pipeline
ner.add_label("GPE") # add named entity label to NER

# Load the dataset
with open("data/training_data.json") as f:
    TRAINING_DATA = json.loads(f.read())

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
