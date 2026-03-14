#!/usr/bin/env python3
"""
EIR Parser - Convert any healthcare document to structured health.md format
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Document parsing libraries
try:
    import PyPDF2
    import pytesseract
    from PIL import Image
    import pandas as pd
    from docx import Document
except ImportError:
    print("Missing dependencies. Install with:")
    print("pip install pypdf2 pytesseract pillow pandas python-docx")
    sys.exit(1)

# Medical NLP (optional)
try:
    import spacy
    import medspacy
    nlp_available = True
except ImportError:
    nlp_available = False
    print("Warning: Medical NLP libraries not available. Install with:")
    print("pip install spacy medspacy")
    print("python -m spacy download en_core_web_sm")

class HealthDocumentParser:
    """Parse healthcare documents into EIR health.md format"""
    
    def __init__(self, privacy_level="anonymous"):
        self.privacy_level = privacy_level
        self.extracted_data = {
            'demographics': {},
            'medications': [],
            'conditions': [],
            'lab_results': [],
            'vital_signs': [],
            'allergies': [],
            'providers': [],
            'timeline': [],
            'unconfirmed_findings': [],
            'information_gaps': []
        }
        
        # Load medical NLP model if available
        if nlp_available:
            try:
                self.nlp = medspacy.load()
                self.medical_nlp = True
            except:
                self.medical_nlp = False
        else:
            self.medical_nlp = False
    
    def parse_file(self, file_path: str) -> Dict:
        """Parse any file format and extract health information"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine file type and parse accordingly
        extension = file_path.suffix.lower()
        
        if extension == '.pdf':
            text = self._parse_pdf(file_path)
        elif extension in ['.txt', '.md']:
            text = self._parse_text(file_path)
        elif extension == '.docx':
            text = self._parse_docx(file_path)
        elif extension in ['.jpg', '.jpeg', '.png', '.tiff']:
            text = self._parse_image_ocr(file_path)
        elif extension == '.csv':
            return self._parse_csv_labs(file_path)
        elif extension == '.json':
            return self._parse_json_data(file_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
        
        # Extract structured information from text
        return self._extract_health_information(text, str(file_path))
    
    def _parse_pdf(self, file_path: Path) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error parsing PDF: {e}")
        
        return text
    
    def _parse_text(self, file_path: Path) -> str:
        """Read plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
    
    def _parse_docx(self, file_path: Path) -> str:
        """Extract text from Word document"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return ""
    
    def _parse_image_ocr(self, file_path: Path) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error with OCR: {e}")
            return ""
    
    def _parse_csv_labs(self, file_path: Path) -> Dict:
        """Parse CSV lab results"""
        try:
            df = pd.read_csv(file_path)
            
            # Common CSV column mappings
            column_mappings = {
                'test_name': ['test', 'test_name', 'name', 'parameter'],
                'value': ['value', 'result', 'measurement'],
                'reference_range': ['reference', 'ref_range', 'normal_range'],
                'date': ['date', 'test_date', 'collected_date'],
                'units': ['units', 'unit', 'measurement_unit']
            }
            
            labs = []
            for _, row in df.iterrows():
                lab_entry = {}
                for key, possible_columns in column_mappings.items():
                    for col in possible_columns:
                        if col in df.columns:
                            lab_entry[key] = row[col]
                            break
                
                if 'test_name' in lab_entry and 'value' in lab_entry:
                    labs.append({
                        'test': lab_entry.get('test_name', ''),
                        'value': lab_entry.get('value', ''),
                        'reference_range': lab_entry.get('reference_range', ''),
                        'date': lab_entry.get('date', ''),
                        'units': lab_entry.get('units', ''),
                        'source': f'document_parsed ({file_path.name})',
                        'confidence': 'High'
                    })
            
            self.extracted_data['lab_results'] = labs
            return self.extracted_data
            
        except Exception as e:
            print(f"Error parsing CSV: {e}")
            return {}
    
    def _parse_json_data(self, file_path: Path) -> Dict:
        """Parse JSON health data"""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
            # Try to map common JSON structures
            if 'medications' in data:
                self.extracted_data['medications'] = data['medications']
            if 'conditions' in data:
                self.extracted_data['conditions'] = data['conditions']
            if 'labs' in data:
                self.extracted_data['lab_results'] = data['labs']
                
            return self.extracted_data
            
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return {}
    
    def _extract_health_information(self, text: str, source_file: str) -> Dict:
        """Extract structured health information from text"""
        
        # Use medical NLP if available
        if self.medical_nlp:
            doc = self.nlp(text)
            
            # Extract medications
            for ent in doc.ents:
                if ent.label_ == "DRUG":
                    medication = {
                        'name': ent.text,
                        'source': f'document_parsed ({Path(source_file).name})',
                        'confidence': 'Medium',
                        'context': self._get_surrounding_context(text, ent.text)
                    }
                    self.extracted_data['medications'].append(medication)
        
        # Fallback: Pattern-based extraction
        self._extract_patterns(text, source_file)
        
        # Detect document type and enhance extraction
        doc_type = self._detect_document_type(text)
        if doc_type == 'lab_report':
            self._extract_lab_patterns(text, source_file)
        elif doc_type == 'discharge_summary':
            self._extract_discharge_patterns(text, source_file)
        
        return self.extracted_data
    
    def _extract_patterns(self, text: str, source_file: str):
        """Extract information using regex patterns"""
        import re
        
        # Common medication patterns
        med_patterns = [
            r'(\w+)\s+(\d+(?:\.\d+)?)\s*(mg|mcg|g|units)',  # Drug dosage
            r'(?:taking|prescribed|on)\s+([A-Za-z]+)',      # Taking medication
        ]
        
        for pattern in med_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                medication = {
                    'name': match.group(1) if len(match.groups()) >= 1 else match.group(0),
                    'dosage': match.group(2) + match.group(3) if len(match.groups()) >= 3 else '',
                    'source': f'document_parsed ({Path(source_file).name})',
                    'confidence': 'Medium'
                }
                self.extracted_data['medications'].append(medication)
        
        # Lab value patterns
        lab_patterns = [
            r'(A1C|HbA1c|Hemoglobin A1c).*?(\d+\.?\d*)%',
            r'(Glucose|Blood Sugar).*?(\d+)\s*mg/dL',
            r'(Creatinine).*?(\d+\.?\d*)\s*mg/dL',
        ]
        
        for pattern in lab_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                lab = {
                    'test': match.group(1),
                    'value': match.group(2),
                    'units': '%' if 'A1C' in match.group(1) else 'mg/dL',
                    'source': f'document_parsed ({Path(source_file).name})',
                    'confidence': 'High'
                }
                self.extracted_data['lab_results'].append(lab)
    
    def _detect_document_type(self, text: str) -> str:
        """Detect the type of medical document"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ['lab results', 'laboratory', 'reference range']):
            return 'lab_report'
        elif any(term in text_lower for term in ['discharge summary', 'admission', 'discharge']):
            return 'discharge_summary'
        elif any(term in text_lower for term in ['medication list', 'prescriptions', 'current medications']):
            return 'medication_list'
        elif any(term in text_lower for term in ['progress note', 'clinic note', 'office visit']):
            return 'clinical_note'
        else:
            return 'unknown'
    
    def _extract_lab_patterns(self, text: str, source_file: str):
        """Enhanced lab result extraction"""
        import re
        
        # More sophisticated lab patterns
        patterns = [
            r'([A-Za-z0-9\s]+?)\s+(\d+\.?\d*)\s*([a-zA-Z/%]+)?\s*(?:Ref|Reference)?:?\s*([0-9.\-<>]+.*?)(?:\n|$)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.MULTILINE)
            for match in matches:
                lab = {
                    'test': match.group(1).strip(),
                    'value': match.group(2),
                    'units': match.group(3) or '',
                    'reference_range': match.group(4) or '',
                    'source': f'document_parsed ({Path(source_file).name})',
                    'confidence': 'High'
                }
                self.extracted_data['lab_results'].append(lab)
    
    def _extract_discharge_patterns(self, text: str, source_file: str):
        """Extract information specific to discharge summaries"""
        # Implementation for discharge summary parsing
        pass
    
    def _get_surrounding_context(self, text: str, entity: str, context_chars=100) -> str:
        """Get surrounding context for an entity"""
        start = text.find(entity)
        if start == -1:
            return ""
        
        context_start = max(0, start - context_chars)
        context_end = min(len(text), start + len(entity) + context_chars)
        
        return text[context_start:context_end]
    
    def generate_health_md(self, output_file="health.md") -> str:
        """Generate health.md file from extracted data"""
        
        timestamp = datetime.now().isoformat()
        
        health_md = f"""---
health_md_version: "1.1"
record_id: "parsed-record-{datetime.now().strftime('%Y%m%d')}"
generated: "{timestamp}"
privacy_level: "{self.privacy_level}"
last_updated: "{timestamp}"
data_sources: ["document_parsed"]
agent_compatible: true
provenance_policy: "required_for_agent_added_facts"
---

# Health Record - Document Parsed

## Demographics

*Demographics not extracted from document - please add manually*

## Current Medications

"""
        
        # Add medications
        for med in self.extracted_data['medications']:
            health_md += f"""### {med['name']}

- **Dosage:** {med.get('dosage', 'Not specified')}
- **Source:** {med['source']}
- **Confidence:** {med['confidence']}
- **Context:** {med.get('context', '')[:200]}...

"""
        
        # Add lab results
        if self.extracted_data['lab_results']:
            health_md += "## Lab Results\n\n"
            
            for lab in self.extracted_data['lab_results']:
                health_md += f"""### {lab['test']}

- **Value:** {lab['value']} {lab.get('units', '')}
- **Reference Range:** {lab.get('reference_range', 'Not specified')}
- **Date:** {lab.get('date', 'Not specified')}
- **Source:** {lab['source']}
- **Confidence:** {lab['confidence']}

"""
        
        # Add unconfirmed findings
        health_md += """## Unconfirmed Findings

*All information extracted from documents requires user confirmation*

"""
        
        for finding in self.extracted_data['medications'] + self.extracted_data['lab_results']:
            health_md += f"""### {finding.get('name', finding.get('test', 'Unknown'))} (Document Mention)
- **Type:** {finding.get('type', 'Extracted from document')}
- **Source:** {finding['source']}
- **Confidence:** {finding['confidence']}
- **Action Needed:** Confirm accuracy with user

"""
        
        # Add information gaps
        health_md += """## Information Gaps & Follow-up Questions

### Missing Demographics
- **Question:** Patient age, sex, and basic demographic information
- **Why It Matters:** Required for clinical context and reference ranges
- **Status:** Open

### Missing Medical History
- **Question:** Chronic conditions, past surgeries, family history
- **Why It Matters:** Essential for comprehensive health picture
- **Status:** Open

### Medication Details
- **Question:** Confirm current dosages, start dates, prescribing providers
- **Why It Matters:** Ensure accuracy of medication list
- **Status:** Open

"""
        
        # Save file
        with open(output_file, 'w') as f:
            f.write(health_md)
        
        return health_md

def main():
    parser = argparse.ArgumentParser(description='Parse healthcare documents into EIR health.md format')
    parser.add_argument('document', help='Path to document to parse')
    parser.add_argument('--output', default='health.md', help='Output health.md file')
    parser.add_argument('--privacy', choices=['anonymous', 'pseudonymized', 'identified'], 
                       default='anonymous', help='Privacy level')
    
    args = parser.parse_args()
    
    try:
        # Parse document
        print(f"Parsing {args.document}...")
        doc_parser = HealthDocumentParser(privacy_level=args.privacy)
        extracted_data = doc_parser.parse_file(args.document)
        
        # Generate health.md
        print(f"Generating {args.output}...")
        health_md_content = doc_parser.generate_health_md(args.output)
        
        print(f"✅ Successfully parsed document and created {args.output}")
        print(f"📊 Extracted: {len(extracted_data['medications'])} medications, {len(extracted_data['lab_results'])} lab results")
        print(f"\n📝 Next steps:")
        print(f"1. Review {args.output} for accuracy")
        print(f"2. Confirm extracted information")  
        print(f"3. Fill in missing demographic information")
        print(f"4. Move confirmed findings from 'Unconfirmed Findings' to appropriate sections")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()