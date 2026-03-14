# EIR Parser Skill

Parse and structure any healthcare document into the standardized EIR health.md format. Upload PDFs, text files, lab results, discharge summaries, or any health document - get clean, structured, agent-readable health records.

## Supported Formats

- **PDF**: Lab reports, discharge summaries, medical records
- **TXT/DOC**: Clinical notes, health summaries  
- **Images**: Screenshots of health apps, paper records (via OCR)
- **Structured data**: JSON, CSV lab results
- **EHR exports**: Epic, Cerner, Allscripts formats

## Usage

```bash
# Parse any document into health.md format
python3 skills/eir-parser/parse_document.py [document_path] [--output health.md] [--privacy anonymous|pseudonymized|identified]

# Interactive mode - ask questions to fill gaps
python3 skills/eir-parser/interactive_parse.py [document_path]

# Merge multiple documents into single health.md
python3 skills/eir-parser/merge_records.py doc1.pdf doc2.txt lab_results.json
```

## Features

### 🔍 Intelligent Extraction
- Medical entities (conditions, medications, lab values)
- Temporal relationships (when conditions started, medication changes)
- Provider information and care team
- Structured lab results with reference ranges

### 🛡️ Safety-First Processing
- All extracted facts marked with `source: document_parsed`
- Uncertain findings go to "Unconfirmed Findings" section
- Confidence scoring for each extracted element
- Privacy-aware anonymization

### 📋 Smart Structuring
- Auto-detects document type (lab report, discharge summary, etc.)
- Maps content to appropriate EIR sections
- Creates condition-specific files when warranted
- Suggests relevant skill attachments

### 🧠 Gap Detection
- Identifies missing critical information
- Generates follow-up questions for user
- Tracks information quality and completeness

## Example Workflow

1. **Upload**: User drops lab_results.pdf
2. **Extract**: Parse PDF → identify labs, medications, conditions
3. **Structure**: Map to health.md sections with provenance
4. **Review**: Show structured output, mark uncertainties
5. **Confirm**: User validates/corrects extracted information
6. **Integrate**: Merge into existing health.md or create new file

## Document Types & Parsing

### Lab Reports
- Extract test names, values, reference ranges, dates
- Detect trends (improving/worsening)
- Flag abnormal values
- Map to standard LOINC codes when possible

### Discharge Summaries
- Parse admission reason, procedures, medications
- Extract discharge diagnoses with ICD codes
- Identify care team and follow-up instructions
- Timeline reconstruction

### Medication Lists
- Parse drug names, dosages, frequencies
- Extract indication, prescriber, start dates
- Detect drug interactions and duplicates
- Standardize to generic names

### Clinical Notes
- Extract subjective/objective findings
- Identify assessment and plan sections
- Parse vital signs and physical exam
- Extract provider recommendations

## Privacy & Anonymization

### Auto-Anonymization Features
- Detect and redact names, addresses, phone numbers
- Replace dates with relative timeframes ("3 months ago")
- Anonymize provider names → roles ("Cardiologist")
- Generate consistent pseudonyms across documents

### Privacy Level Controls
```yaml
privacy_level: anonymous
auto_redact: true
preserve_clinical_context: true
```

## Integration Patterns

### With Base Health Skill
- Creates/updates health.md following EIR v1.1 spec
- Populates "Information Gaps & Follow-up Questions"
- Suggests skill attachments based on detected conditions

### With Condition Skills
- Auto-creates diabetes.md if diabetes detected
- Populates pregnancy.md if pregnancy-related content found
- Links condition files in health.md master record

## Advanced Features

### Multi-Document Intelligence
- Cross-reference information across documents
- Detect conflicts and highlight for review
- Build comprehensive timeline from fragments
- Merge duplicate information intelligently

### Quality Scoring
```markdown
### Type 2 Diabetes Mellitus
- **Source:** document_parsed (discharge_summary_2024.pdf)
- **Confidence:** High (explicit diagnosis stated)
- **Quality Score:** 85% (missing onset date)
```

### Structured Prompting
- Asks targeted follow-up questions
- "I found diabetes medication but no diagnosis date - when were you first diagnosed?"
- Guides users through information gaps systematically

## Error Handling & Edge Cases

- **Scanned documents**: OCR with confidence scoring
- **Handwritten notes**: Flag for manual review
- **Foreign languages**: Detect and warn about translation needs
- **Partial documents**: Extract what's available, note limitations

## Output Examples

### From Lab PDF → Health.md
```markdown
## Lab Results

### Hemoglobin A1C (2024-02-10)
- **Value:** 6.8% (↓ from 8.2%)
- **Reference Range:** <7.0% (ADA target)
- **Source:** document_parsed (lab_results_feb2024.pdf)
- **Confidence:** High
- **Clinical Significance:** Good glycemic control

## Unconfirmed Findings

### Possible Metformin Increase (document mention)
- **Type:** Medication change
- **Source:** document_parsed
- **Evidence:** "Increase Metformin to 1000mg BID" in provider notes
- **Action Needed:** Confirm current dosage with user
```

## Installation & Dependencies

```bash
# Install parsing libraries
pip install pypdf2 pytesseract pandas python-docx
pip install spacy transformers # For medical NLP
python -m spacy download en_core_web_sm

# Medical entity recognition
pip install medspacy scispacy
```

## Configuration

```yaml
# skills/eir-parser/config.yml
default_privacy_level: anonymous
auto_suggest_skills: true
confidence_threshold: 0.7
ocr_enabled: true
max_file_size_mb: 50

# Medical NLP settings
extract_medications: true
extract_conditions: true  
extract_lab_values: true
map_to_standard_codes: true
```

This skill transforms the messy reality of healthcare documents into clean, structured, agent-readable health records. Upload anything, get standardized health.md output!