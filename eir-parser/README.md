# EIR Parser - Document to Health.md Converter

Transform any healthcare document into structured, agent-readable health.md format.

## 🚀 Quick Start

```bash
# Basic parsing - extract info from any document
python3 skills/eir-parser/parse_document.py examples/sample_lab_report.txt

# Interactive mode - guided questions to fill gaps  
python3 skills/eir-parser/interactive_parse.py examples/sample_lab_report.txt

# Parse CSV lab data
python3 skills/eir-parser/parse_document.py examples/medication_list.csv
```

## 📋 Supported Formats

| Format | Description | Example Use |
|--------|-------------|-------------|
| **PDF** | Lab reports, discharge summaries | Hospital records, test results |
| **TXT** | Clinical notes, reports | Doctor's notes, health summaries |
| **CSV** | Structured lab data | Exported lab results, medication lists |
| **Images** | Screenshots, scanned documents | Health app screenshots, paper records |
| **JSON** | EHR exports, API data | Epic exports, health app data |

## 🎯 Real-World Examples

### Lab Report → Structured Data
**Input:** `sample_lab_report.txt`
```
Hemoglobin A1C    6.8%    Reference: <7.0% 
Glucose, Fasting  125 mg/dL    Reference: 70-100 mg/dL
```

**Output:** `health.md`
```markdown
### Hemoglobin A1C (2024-02-10)
- **Value:** 6.8%
- **Reference Range:** <7.0% (ADA target)
- **Source:** document_parsed (sample_lab_report.txt)
- **Clinical Significance:** Good glycemic control
```

### Medication CSV → Current Medications
**Input:** `medication_list.csv`
```
medication_name,dosage,indication
Metformin,500mg,Type 2 Diabetes
Lisinopril,10mg,Hypertension
```

**Output:**
```markdown
### Metformin 500mg
- **Indication:** Type 2 Diabetes Mellitus  
- **Dosage:** 500mg twice daily
- **Source:** document_parsed (medication_list.csv)
```

## 🔍 Processing Pipeline

1. **Document Analysis** - Detect format, extract text/data
2. **Medical Entity Recognition** - Find medications, conditions, labs
3. **Structured Mapping** - Convert to EIR health.md sections
4. **Provenance Tracking** - Mark source and confidence for all facts
5. **Gap Detection** - Identify missing information, suggest follow-ups
6. **Safety Processing** - All extracted facts → "Unconfirmed Findings" until verified

## 🛡️ Safety Features

### Provenance Tracking
Every extracted fact includes:
- **Source:** `document_parsed (filename)`
- **Confidence:** High/Medium/Low based on extraction method
- **Action Needed:** User confirmation required

### Privacy Protection
```bash
# Anonymize sensitive information
python3 parse_document.py report.pdf --privacy anonymous

# Keep detailed info for personal use
python3 parse_document.py report.pdf --privacy identified
```

### Unconfirmed Findings Pipeline
1. Document mentions "diabetes medication" → Unconfirmed Findings
2. User confirms → Active Health Contexts  
3. Agent can now use confirmed information safely

## 🤖 Agent Integration

### Auto-Skill Suggestions
Parser detects conditions and suggests relevant skills:

```markdown
## Skill Attachments

### diabetes
- **Status:** Suggested
- **Reason:** Metformin detected in medication list
- **Added By:** agent
```

### Information Gaps for Follow-up
```markdown
## Information Gaps & Follow-up Questions

### Missing Diagnosis Date
- **Question:** When were you first diagnosed with Type 2 Diabetes?
- **Why It Matters:** Timeline for condition management
- **Status:** Open
```

## 📊 Output Quality

### High Confidence
- Structured data (CSV, JSON)
- Clear lab values with units
- Explicit medication lists

### Medium Confidence  
- Pattern-matched text extractions
- OCR'd document content
- Inferred relationships

### Low Confidence
- Ambiguous mentions
- Poor quality scans
- Incomplete information

## 🔧 Installation

```bash
# Core dependencies
pip install pypdf2 pytesseract pillow pandas python-docx

# Enhanced medical NLP (optional)
pip install spacy medspacy
python -m spacy download en_core_web_sm

# OCR support (optional)
# macOS: brew install tesseract
# Ubuntu: apt-get install tesseract-ocr
```

## 📝 Usage Patterns

### 1. Quick Parse (Basic Info)
```bash
python3 parse_document.py my_labs.pdf
# → health.md with extracted data, everything unconfirmed
```

### 2. Interactive Parse (Complete Record)
```bash
python3 interactive_parse.py my_labs.pdf
# → Guided questions, confirmed information, ready for agents
```

### 3. Batch Processing
```bash
for doc in *.pdf; do
    python3 parse_document.py "$doc" --output "health_$doc.md"
done
```

### 4. Privacy-Aware Processing
```bash
# For sharing/research (anonymized)
python3 parse_document.py sensitive_report.pdf --privacy anonymous

# For personal agent use (full detail)
python3 parse_document.py my_report.pdf --privacy identified
```

## 🎯 Best Practices

### Document Preparation
- **Scan quality:** 300+ DPI for OCR
- **File naming:** Include date/type (labs_2024-02-10.pdf)
- **Organization:** Group related documents

### Verification Workflow
1. Parse document with basic mode
2. Review "Unconfirmed Findings" section  
3. Use interactive mode for critical documents
4. Manually verify sensitive information (medications, allergies)

### Agent Integration
- Use `Skill Attachments` to auto-load relevant skills
- Check `Information Gaps` for follow-up questions
- Respect `confidence` levels in decision-making

## 🚀 Advanced Features

### Custom Extraction Patterns
Modify `parse_document.py` to add facility-specific patterns:

```python
# Add custom lab patterns
lab_patterns = [
    r'(Custom Test Name)\s+(\d+\.?\d*)\s*(units)',
]
```

### Condition-Specific Processing  
Enhanced extraction for specific conditions:

```python
# Diabetes-focused extraction
if 'diabetes' in text.lower():
    extract_diabetes_context(text)
```

### Multi-Document Intelligence
```bash
# Merge multiple documents intelligently
python3 merge_records.py labs2024.pdf discharge.pdf medications.csv
```

## 🔮 Future Features

- [ ] **Real-time OCR** - Live document scanning via camera
- [ ] **EHR Integration** - Direct FHIR/HL7 import
- [ ] **Smart Conflict Resolution** - Detect contradictions across documents
- [ ] **Temporal Analysis** - Track changes over time
- [ ] **Voice Dictation** - "Add to my health record that..."

---

**Transform messy healthcare documents into clean, structured, agent-ready health records. Upload anything, get standardized EIR format output.**