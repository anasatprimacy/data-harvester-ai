import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

class DataExtractor:
    """
    A robust, zero-dependency pattern-based data extractor.
    Since ML models like spaCy currently fail on Python 3.14 due to pydantic V1 incompatibility,
    this highly optimized rules-engine serves as a highly effective alternative to extract likely data.
    """
    def __init__(self):
        self.patterns = {
            "EMAIL": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
            "PHONE": re.compile(r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}"),
            "REVENUE": re.compile(r"(?:₹|\$|€|£|Rs\.?|INR|USD)?\s*[\d,.]+\s*(?:Cr|Crore|Million|Billion|Lakh)\b", re.IGNORECASE),
            "ERP": re.compile(r"\b(SAP|Oracle|Odoo|Dynamics|NetSuite|Tally|Zoho|Salesforce)\b", re.IGNORECASE),
            "EMPLOYEES": re.compile(r"(\d{1,6}\s*(?:\+|employees)|\d{1,6}\s*-\s*\d{1,6}\s*employees)", re.IGNORECASE),
            "LEADERSHIP_ROLE": re.compile(r"\b(?:CEO|CFO|CTO|Director|Founder|VP|President|Head)\b", re.IGNORECASE)
        }
        
    def extract_from_text(self, text):
        results = {}
        for entity_type, pattern in self.patterns.items():
            matches = pattern.findall(text)
            # Clean and deduplicate string matches
            clean_matches = list(set([m.strip() for m in matches if isinstance(m, str) and m.strip()]))
            
            # For capture groups that return tuples (e.g. employee regex)
            if not clean_matches and matches and isinstance(matches[0], tuple):
                clean_matches = list(set([" ".join(m).strip() for m in matches]))
                
            if clean_matches:
                results[entity_type] = clean_matches
                
        return results

    def extract_from_json(self, data_path):
        if not os.path.exists(data_path):
            print(f"File {data_path} not found.")
            return
            
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"Processing {len(data)} companies from dataset...")
        for item in data:
            # Combine text to simulate a raw body of text (like a scraped webpage)
            combined_text = " | ".join([str(v) for v in item.values() if v])
            
            company_name = item.get("Company Name", "Unknown")
            print(f"\n--- Extraction for: {company_name} ---")
            
            extracted = self.extract_from_text(combined_text)
            if not extracted:
                print("No entities found.")
                continue
                
            for k, v in extracted.items():
                print(f"  {k}: {', '.join(v)}")

if __name__ == "__main__":
    extractor = DataExtractor()
    
    print("=== Testing Single Unstructured String ===")
    test_text = "Wooden Street led by Lokendra Ranawat opened a new warehouse. Revenue was ₹255 crore+. SAP-ERP implemented. Phone: 9314444747"
    print(f"Raw Text: {test_text.encode('utf-8', 'replace').decode('utf-8')}")
    print(f"Extracted: {str(extractor.extract_from_text(test_text)).encode('utf-8', 'replace').decode('utf-8')}")
    print("\n==========================================")
    
    # Process the user's data.json file
    extractor.extract_from_json("E:/data_harvester/data.json")
