import spacy
import sys
import os

def load_model(model_dir="output/extractor_model"):
    if not os.path.exists(model_dir):
        print(f"Error: Model directory '{model_dir}' not found. Please train the model first.")
        sys.exit(1)
        
    print(f"Loading custom NER model from {model_dir}...")
    return spacy.load(model_dir)

def extract_entities(nlp, text):
    doc = nlp(text)
    extracted = {}
    for ent in doc.ents:
        if ent.label_ not in extracted:
            extracted[ent.label_] = []
        extracted[ent.label_].append(ent.text)
        
    return extracted

if __name__ == "__main__":
    nlp = load_model()
    
    sample_texts = [
        "In 2023, Wooden Street led by Lokendra Ranawat opened a new warehouse in Jaipur, Rajasthan, India.",
        "Sobisco operates in FMCG - Biscuits with Suresh Agarwal as their CFO. Contact them at info@sobisco.com",
    ]
    
    print("\\n--- Testing Extraction Inference ---\\n")
    for text in sample_texts:
        print(f"Raw Text: {text}")
        entities = extract_entities(nlp, text)
        print("Extracted Likely Data:")
        for k, v in entities.items():
            print(f"  {k}: {', '.join(v)}")
        print("-" * 50)
