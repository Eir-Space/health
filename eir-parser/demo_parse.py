#!/usr/bin/env python3
"""
Demo EIR Parser - Lightweight version for testing without dependencies
"""

import re
import json
from datetime import datetime
from pathlib import Path

def parse_text_document(file_path: str) -> dict:
    """Parse text document for health information"""
    
    with open(file_path, 'r') as f:
        text = f.read()
    
    extracted_data = {
        'medications': [],
        'lab_results': [],
        'providers': [],
        'dates': [],
        'conditions': []
    }
    
    # Extract lab values
    lab_patterns = [
        r'(A1C|HbA1c|Hemoglobin A1c)\s+(\d+\.?\d*%)',
        r'(Glucose.*?)\s+(\d+)\s*mg/dL',
        r'(Creatinine)\s+(\d+\.?\d*)\s*mg/dL',
        r'(Cholesterol.*?)\s+(\d+)\s*mg/dL',
        r'(HDL.*?)\s+(\d+)\s*mg/dL',
        r'(LDL.*?)\s+(\d+)\s*mg/dL',
        r'(Triglycerides)\s+(\d+)\s*mg/dL',
        r'(Potassium)\s+(\d+\.?\d*)\s*mEq/L',
    ]
    
    for pattern in lab_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            test_name = match.group(1).strip()
            value = match.group(2).strip()
            
            # Extract reference range if present  
            ref_pattern = rf'{re.escape(test_name)}.*?Reference:\s*([^\\n]*)'
            ref_match = re.search(ref_pattern, text, re.IGNORECASE)
            ref_range = ref_match.group(1).strip() if ref_match else ''
            
            lab = {
                'test': test_name,
                'value': value,
                'reference_range': ref_range,
                'source': f'document_parsed ({Path(file_path).name})',
                'confidence': 'High'
            }
            extracted_data['lab_results'].append(lab)
    
    # Extract medications
    med_patterns = [
        r'(Metformin|Lisinopril|Atorvastatin|Omeprazole)',
    ]
    
    for pattern in med_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            med = {
                'name': match.group(1),
                'source': f'document_parsed ({Path(file_path).name})',
                'confidence': 'Medium'
            }
            extracted_data['medications'].append(med)
    
    # Extract providers
    provider_patterns = [
        r'Physician:\s*(Dr\.\s*[A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'(Dr\.\s*[A-Z][a-z]+\s+[A-Z][a-z]+)',
    ]
    
    for pattern in provider_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            provider = {
                'name': match.group(1),
                'source': f'document_parsed ({Path(file_path).name})',
            }
            extracted_data['providers'].append(provider)
    
    # Extract dates
    date_patterns = [
        r'(\d{4}-\d{2}-\d{2})',
    ]
    
    for pattern in date_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            extracted_data['dates'].append(match.group(1))
    
    return extracted_data

def generate_health_md(extracted_data: dict, source_file: str) -> str:
    """Generate health.md from extracted data"""
    
    timestamp = datetime.now().isoformat()
    
    health_md = f"""---
health_md_version: "1.1"
record_id: "parsed-demo-{datetime.now().strftime('%Y%m%d')}"
generated: "{timestamp}"
privacy_level: "anonymous"
last_updated: "{timestamp}"
data_sources: ["document_parsed"]
agent_compatible: true
provenance_policy: "required_for_agent_added_facts"
---

# Health Record - Document Parsed Demo

## Demographics

*Demographics not extracted from document - please add manually*

- **Age:** Not specified
- **Sex:** Not specified  
- **Occupation:** Not specified

## Lab Results

"""
    
    # Add lab results
    for lab in extracted_data['lab_results']:
        health_md += f"""### {lab['test']}

- **Value:** {lab['value']}
- **Reference Range:** {lab.get('reference_range', 'Not specified')}
- **Source:** {lab['source']}
- **Confidence:** {lab['confidence']}

"""
    
    # Add unconfirmed findings
    health_md += """## Unconfirmed Findings

*All information extracted from documents requires user confirmation*

"""
    
    # Add medications as unconfirmed
    for med in extracted_data['medications']:
        health_md += f"""### {med['name']} (Document Mention)
- **Type:** Potential current medication
- **Source:** {med['source']}
- **Confidence:** {med['confidence']}
- **Action Needed:** Confirm current usage, dosage, indication

"""
    
    # Add providers as unconfirmed
    for provider in extracted_data['providers']:
        health_md += f"""### Provider Reference: {provider['name']}
- **Type:** Care team member mentioned in document
- **Source:** {provider['source']}
- **Action Needed:** Confirm current provider relationship

"""
    
    # Add information gaps
    health_md += """## Information Gaps & Follow-up Questions

### Complete Demographics
- **Question:** Patient age, sex, and basic demographic information
- **Why It Matters:** Required for clinical context and reference ranges
- **Status:** Open

### Medication Details
- **Question:** Current dosages, start dates, indications for detected medications
- **Why It Matters:** Ensure accurate medication list
- **Status:** Open

### Medical History
- **Question:** Chronic conditions, past medical history
- **Why It Matters:** Clinical context for lab interpretation
- **Status:** Open

### Provider Information
- **Question:** Current care team and contact information
- **Why It Matters:** Care coordination and follow-up
- **Status:** Open

"""
    
    # Add skill suggestions
    health_md += """## Skill Attachments

### health
- **Status:** Active
- **Reason:** Base health record management
- **Added By:** system

"""
    
    # Suggest condition-specific skills based on detected content
    if any('A1C' in lab['test'] or 'Glucose' in lab['test'] for lab in extracted_data['lab_results']):
        health_md += """### diabetes
- **Status:** Suggested  
- **Reason:** Diabetes-related lab results detected
- **Added By:** agent

"""
    
    if any('Cholesterol' in lab['test'] for lab in extracted_data['lab_results']):
        health_md += """### cardiovascular
- **Status:** Suggested
- **Reason:** Cardiovascular risk markers detected
- **Added By:** agent

"""
    
    return health_md

def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 demo_parse.py <text_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        print(f"🔍 Parsing {file_path}...")
        extracted_data = parse_text_document(file_path)
        
        print(f"📊 Extracted:")
        print(f"  - {len(extracted_data['lab_results'])} lab results")
        print(f"  - {len(extracted_data['medications'])} potential medications")
        print(f"  - {len(extracted_data['providers'])} providers")
        
        # Generate health.md
        output_file = f"demo_health_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        health_md = generate_health_md(extracted_data, file_path)
        
        with open(output_file, 'w') as f:
            f.write(health_md)
        
        print(f"✅ Generated {output_file}")
        print(f"\n📝 Next steps:")
        print(f"1. Review {output_file} for accuracy")
        print(f"2. Move confirmed findings from 'Unconfirmed Findings' to appropriate sections")
        print(f"3. Fill in demographic information")
        print(f"4. Confirm medication details")
        
        # Show preview
        print(f"\n📋 Preview of extracted lab results:")
        for lab in extracted_data['lab_results'][:3]:  # Show first 3
            print(f"  - {lab['test']}: {lab['value']} (Ref: {lab['reference_range']})")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()