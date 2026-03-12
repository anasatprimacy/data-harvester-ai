import urllib.request
import json

r = urllib.request.urlopen('http://localhost:8000/api/extract')
d = json.loads(r.read())
print(f"Extracted {d['count']} companies")
for c in d['companies']:
    name = c.get("Company Name", "?")
    ext = c.get("_extracted", {})
    print(f"  {name}: {ext}")
