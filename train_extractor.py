import json
import random
import os
import spacy
from spacy.training.example import Example

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def generate_training_data(data):
    """
    Generates synthetic training examples based on the provided data.json.
    This creates realistic text snippets and aligns the entity labels.
    """
    TRAIN_DATA = []
    
    templates = [
        "We are {COMPANY}, located at {ADDRESS}. You can reach our CEO {PERSON} at {PHONE} or {EMAIL}.",
        "The company {COMPANY} operates in the {INDUSTRY} sector.",
        "{PERSON} is the head of {COMPANY}, making around {REVENUE} annually.",
        "Contact {PERSON} via email at {EMAIL} or call {PHONE}.",
        "{COMPANY} is a major player in {INDUSTRY} with an estimated {REVENUE} turnover. They use {ERP}.",
    ]
    
    for item in data:
        company = item.get("Company Name", "").strip()
        person_block = item.get("Owner/ IT Head/ CEO/Finance Head Name", "").strip()
        # Just grab the first name in the block for simplicity
        person = person_block.split('\n')[0].replace("CEO - ", "").strip()
        phone = item.get("Phone Number", "").strip()
        email = item.get("EMail Address", "").split()[0].strip() if item.get("EMail Address") else ""
        address = item.get("Address", "").strip()
        industry = item.get("Industry_Type", "").strip()
        revenue = item.get("Annual_Turnover", "").strip()
        erp = item.get("Current_Use_ERP Software_Name", "").strip()
        
        entities_dict = {
            "COMPANY": company,
            "PERSON": person,
            "PHONE": phone,
            "EMAIL": email,
            "ADDRESS": address,
            "INDUSTRY": industry,
            "REVENUE": revenue,
            "ERP": erp
        }
        
        for template in templates:
            text = template
            entities = []
            
            # Very simplistic way to generate text and find offsets
            # In real-world, we'd need to be careful with overlapping matches
            for ent_label, ent_value in entities_dict.items():
                if not ent_value or ent_value == "Not publicly documented" or ent_value == "Not publicly disclosed":
                    # skip this entity for this template if it's not present or invalid
                    text = text.replace("{" + ent_label + "}", "")
                else:
                    text = text.replace("{" + ent_label + "}", ent_value)
            
            # Clean up double spaces from replacements
            text = " ".join(text.split())
            
            # Now find offsets
            for ent_label, ent_value in entities_dict.items():
                if not ent_value or ent_value == "Not publicly documented" or ent_value == "Not publicly disclosed":
                    continue
                start = text.find(ent_value)
                if start != -1:
                    entities.append((start, start + len(ent_value), ent_label))
                    
            if entities:
                TRAIN_DATA.append((text, {"entities": entities}))
                
    return TRAIN_DATA

def train_ner_model(train_data, output_dir="output/extractor_model", n_iter=20):
    """
    Trains a blank spaCy NER model on the synthetic dataset.
    """
    print(f"Initializing blank English model...")
    nlp = spacy.blank("en")
    
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")
        
    for _, annotations in train_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
            
    # Disable other pipes during training if they exist
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        print(f"Training model for {n_iter} iterations...")
        
        for itn in range(n_iter):
            random.shuffle(train_data)
            losses = {}
            
            for text, annotations in train_data:
                try:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    nlp.update([example], drop=0.5, sgd=optimizer, losses=losses)
                except ValueError:
                    # Skip overlapping entities exception for this quick script
                    pass
            print(f"Iteration {itn + 1}/{n_iter} - Loss: {losses.get('ner', 0):.3f}")
            
    # Save the model
    os.makedirs(output_dir, exist_ok=True)
    nlp.to_disk(output_dir)
    print(f"\\nModel successfully trained and saved to {output_dir}")
    print("Test it using: nlp = spacy.load('output/extractor_model')")

if __name__ == "__main__":
    data_path = "E:/data_harvester/data.json"
    print(f"Reading target data from {data_path}...")
    
    try:
        data = load_data(data_path)
    except FileNotFoundError:
        print(f"Error: Could not find {data_path}")
        exit(1)
        
    train_data = generate_training_data(data)
    print(f"Generated {len(train_data)} synthetic training examples.")
    
    # Train the model
    try:
        import spacy
        train_ner_model(train_data)
    except ImportError:
        print("\\nError: spaCy is not installed. Please run:")
        print("pip install spacy")
        print("Then run this script again.")
