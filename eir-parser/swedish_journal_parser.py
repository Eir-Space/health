#!/usr/bin/env python3
"""
Swedish Healthcare Journal Parser - Parse 1177.se journal exports to health.md
"""

import yaml
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class SwedishJournalParser:
    """Parse Swedish healthcare journal exports to EIR health.md format"""
    
    def __init__(self):
        self.extracted_data = {
            'demographics': {},
            'medications': [],
            'conditions': [],
            'lab_results': [],
            'vital_signs': [],
            'allergies': [],
            'providers': set(),
            'timeline': [],
            'visits': [],
            'procedures': []
        }
    
    def parse_journal(self, file_path: str) -> Dict:
        """Parse Swedish healthcare journal YAML export"""
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        
        # Extract metadata and demographics
        self._extract_demographics(data.get('metadata', {}))
        
        # Process all healthcare entries
        entries = data.get('entries', [])
        for entry in entries:
            self._process_entry(entry)
        
        return self.extracted_data
    
    def _extract_demographics(self, metadata: Dict):
        """Extract patient demographics from metadata"""
        patient = metadata.get('patient', {})
        
        # Calculate age from birth date
        birth_date = patient.get('birth_date', '')
        if birth_date:
            try:
                birth_year = int(birth_date[:4])
                current_year = datetime.now().year
                age = current_year - birth_year
                self.extracted_data['demographics']['age'] = age
                self.extracted_data['demographics']['birth_date'] = birth_date
            except:
                pass
        
        self.extracted_data['demographics']['name'] = patient.get('name', 'Patient')
        self.extracted_data['demographics']['personal_number'] = patient.get('personal_number', '')
        
        # Export info
        export_info = metadata.get('export_info', {})
        self.extracted_data['demographics']['data_span'] = export_info.get('date_range', {})
        self.extracted_data['demographics']['total_entries'] = export_info.get('total_entries', 0)
    
    def _process_entry(self, entry: Dict):
        """Process individual healthcare entry"""
        
        # Extract basic entry info
        entry_date = entry.get('date', 'Unknown')
        entry_type = entry.get('type', '')
        provider = entry.get('provider', {})
        content = entry.get('content', {})
        
        # Add to providers set
        if provider.get('name'):
            self.extracted_data['providers'].add(provider['name'])
        
        # Create timeline entry
        timeline_entry = {
            'date': entry_date,
            'type': entry_type,
            'provider': provider.get('name', 'Unknown'),
            'category': entry.get('category', ''),
            'summary': content.get('summary', ''),
            'details': content.get('details', ''),
            'responsible': entry.get('responsible_person', {}).get('name', '')
        }
        self.extracted_data['timeline'].append(timeline_entry)
        
        # Parse content for medical information
        details_text = content.get('details', '') + ' ' + ' '.join(content.get('notes', []))
        self._extract_medical_info_from_text(details_text, entry_date, provider.get('name', ''))
        
        # Categorize visit types
        if entry_type in ['Telefon­kontakt', 'Besök', 'Mottagningsbesök']:
            visit = {
                'date': entry_date,
                'type': entry_type,
                'provider': provider.get('name', ''),
                'reason': content.get('summary', ''),
                'responsible': entry.get('responsible_person', {})
            }
            self.extracted_data['visits'].append(visit)
    
    def _extract_medical_info_from_text(self, text: str, date: str, provider: str):
        """Extract medications, conditions, etc. from Swedish text"""
        
        text_lower = text.lower()
        
        # Common Swedish medication patterns
        swedish_med_patterns = [
            r'(alvedon|panodil|ipren|voltaren|omeprazol|simvastatin|metformin|lisinopril)',
            r'(antibiotika|penicillin|amoxicillin)',
            r'(insulin|diabetesmedicin)',
            r'(blodtrycksmedicin|ACE-hämmare)',
        ]
        
        for pattern in swedish_med_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                medication = {
                    'name': match.group(1).title(),
                    'mentioned_date': date,
                    'provider': provider,
                    'context': self._get_context(text, match.start(), 100),
                    'source': 'swedish_journal_parsed',
                    'confidence': 'Medium'
                }
                self.extracted_data['medications'].append(medication)
        
        # Swedish condition patterns
        swedish_condition_patterns = [
            r'(diabetes|diabetiker)',
            r'(högt blodtryck|hypertoni)',
            r'(högt kolesterol|hyperlipidemi)',
            r'(astma|allergi)',
            r'(depression|ångest)',
            r'(hjärtproblem|hjärtsjukdom)',
            r'(cancer|tumör)',
            r'(inflammation|infektion)',
        ]
        
        for pattern in swedish_condition_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                condition = {
                    'condition': match.group(1).title(),
                    'mentioned_date': date,
                    'provider': provider,
                    'context': self._get_context(text, match.start(), 100),
                    'source': 'swedish_journal_inferred',
                    'confidence': 'Low'  # Needs confirmation
                }
                self.extracted_data['conditions'].append(condition)
        
        # Lab value patterns (Swedish units)
        lab_patterns = [
            r'(HbA1c|A1c).*?(\d+\.?\d*)\s*(mmol/mol|%)',
            r'(blodsocker|glukos).*?(\d+\.?\d*)\s*(mmol/l|mg/dl)',
            r'(kolesterol).*?(\d+\.?\d*)\s*(mmol/l)',
            r'(blodtryck).*?(\d+/\d+)',
            r'(vikt).*?(\d+\.?\d*)\s*kg',
            r'(längd).*?(\d+)\s*cm',
        ]
        
        for pattern in lab_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                lab = {
                    'test': match.group(1).title(),
                    'value': match.group(2),
                    'units': match.group(3) if len(match.groups()) >= 3 else '',
                    'date': date,
                    'provider': provider,
                    'source': 'swedish_journal_parsed',
                    'confidence': 'Medium'
                }
                self.extracted_data['lab_results'].append(lab)
    
    def _get_context(self, text: str, position: int, context_chars: int = 100) -> str:
        """Get surrounding context for a match"""
        start = max(0, position - context_chars)
        end = min(len(text), position + context_chars)
        return text[start:end].replace('\n', ' ').strip()
    
    def generate_health_md(self, output_file="birger_health_from_journal.md") -> str:
        """Generate comprehensive health.md from Swedish journal data"""
        
        timestamp = datetime.now().isoformat()
        demographics = self.extracted_data['demographics']
        
        health_md = f"""---
health_md_version: "1.1"
record_id: "birger-swedish-journal-{datetime.now().strftime('%Y%m%d')}"
generated: "{timestamp}"
privacy_level: "identified"
last_updated: "{timestamp}"
data_sources: ["swedish_healthcare_journal", "1177_se_export"]
agent_compatible: true
provenance_policy: "required_for_agent_added_facts"
---

# Health Record - {demographics.get('name', 'Patient')}
*Compiled from Swedish Healthcare Journal (1177.se)*

## Demographics

- **Name:** {demographics.get('name', 'Not specified')}
- **Age:** {demographics.get('age', 'Not calculated')} (Born: {demographics.get('birth_date', 'Not specified')})
- **Personal Number:** {demographics.get('personal_number', 'Not specified')}
- **Data Span:** {demographics.get('data_span', {}).get('start', 'Unknown')} to {demographics.get('data_span', {}).get('end', 'Unknown')}
- **Total Healthcare Entries:** {demographics.get('total_entries', 0)}

## Current Medications (Inferred from Journal)

"""
        
        # Add medications found in journal
        unique_medications = {}
        for med in self.extracted_data['medications']:
            name = med['name']
            if name not in unique_medications:
                unique_medications[name] = med
        
        for med in unique_medications.values():
            health_md += f"""### {med['name']}

- **First Mentioned:** {med['mentioned_date']}
- **Provider:** {med['provider']}
- **Context:** {med['context'][:200]}...
- **Source:** {med['source']}
- **Confidence:** {med['confidence']}

"""
        
        # Add lab results if any
        if self.extracted_data['lab_results']:
            health_md += """## Lab Results (From Journal Mentions)

"""
            for lab in self.extracted_data['lab_results']:
                health_md += f"""### {lab['test']} ({lab['date']})

- **Value:** {lab['value']} {lab.get('units', '')}
- **Provider:** {lab['provider']}
- **Source:** {lab['source']}
- **Confidence:** {lab['confidence']}

"""
        
        # Add healthcare timeline
        health_md += """## Clinical Timeline (Last 10 Entries)

"""
        
        # Show recent timeline entries
        recent_timeline = sorted(self.extracted_data['timeline'], 
                               key=lambda x: x['date'], reverse=True)[:10]
        
        for entry in recent_timeline:
            health_md += f"""### {entry['date']}: {entry['type']}

- **Provider:** {entry['provider']}
- **Category:** {entry['category']}
- **Responsible:** {entry['responsible']}
- **Summary:** {entry['summary'][:150]}...

"""
        
        # Add care team
        health_md += """## Care Team (From Journal)

"""
        
        for provider in sorted(self.extracted_data['providers'])[:10]:  # Top 10 providers
            health_md += f"""### {provider}

- **Source:** swedish_healthcare_journal
- **Relationship:** Provider mentioned in healthcare entries

"""
        
        # Add unconfirmed findings
        health_md += """## Unconfirmed Findings

*Information inferred from Swedish healthcare journal - requires confirmation*

"""
        
        # Add inferred conditions
        unique_conditions = {}
        for cond in self.extracted_data['conditions']:
            name = cond['condition']
            if name not in unique_conditions:
                unique_conditions[name] = cond
        
        for condition in unique_conditions.values():
            health_md += f"""### {condition['condition']} (Journal Mention)
- **Type:** Potential health condition
- **First Mentioned:** {condition['mentioned_date']}
- **Provider:** {condition['provider']}
- **Context:** {condition['context'][:150]}...
- **Source:** {condition['source']}
- **Confidence:** {condition['confidence']}
- **Action Needed:** Confirm if this is an active/past condition

"""
        
        # Add information gaps
        health_md += """## Information Gaps & Follow-up Questions

### Medication Confirmation
- **Question:** Which medications mentioned in journal entries are currently active?
- **Why It Matters:** Accurate current medication list for safety
- **Status:** Open

### Condition Status
- **Question:** Which conditions mentioned are currently active vs. resolved?
- **Why It Matters:** Current health context for agents
- **Status:** Open

### Lab Result Interpretation
- **Question:** Recent lab values and trends for monitoring
- **Why It Matters:** Health tracking and goal setting
- **Status:** Open

### Allergy Information
- **Question:** Drug allergies and food allergies
- **Why It Matters:** Safety for medication recommendations
- **Status:** Open

"""
        
        # Add skill attachments based on detected content
        health_md += """## Skill Attachments

### health
- **Status:** Active
- **Reason:** Base health record management from comprehensive journal
- **Added By:** system

"""
        
        # Suggest skills based on inferred conditions
        condition_skills = {
            'diabetes': ['diabetes', 'diabetiker'],
            'cardiovascular': ['högt blodtryck', 'hypertoni', 'hjärtproblem'],
            'mental-health': ['depression', 'ångest']
        }
        
        for skill, keywords in condition_skills.items():
            if any(any(keyword in cond['condition'].lower() for keyword in keywords) 
                   for cond in self.extracted_data['conditions']):
                health_md += f"""### {skill}
- **Status:** Suggested
- **Reason:** Related conditions mentioned in journal entries
- **Added By:** agent

"""
        
        # Add active health contexts (confirmed items only)
        health_md += """## Active Health Contexts

*Add confirmed conditions here after user validation*

"""
        
        # Save file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(health_md)
        
        return health_md

def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 swedish_journal_parser.py <journal.yml>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        print("🇸🇪 Swedish Healthcare Journal Parser")
        print("=" * 40)
        print(f"📄 Parsing {file_path}...")
        
        parser = SwedishJournalParser()
        extracted_data = parser.parse_journal(file_path)
        
        print(f"✅ Extracted from {extracted_data['demographics'].get('total_entries', 0)} healthcare entries:")
        print(f"  📊 {len(extracted_data['medications'])} medication mentions")
        print(f"  🏥 {len(extracted_data['conditions'])} condition mentions")
        print(f"  🔬 {len(extracted_data['lab_results'])} lab value mentions")
        print(f"  👨‍⚕️ {len(extracted_data['providers'])} healthcare providers")
        print(f"  📅 {len(extracted_data['timeline'])} timeline entries")
        
        # Generate health.md
        output_file = f"birger_health_journal_{datetime.now().strftime('%Y%m%d')}.md"
        health_md = parser.generate_health_md(output_file)
        
        print(f"\\n🎯 Generated {output_file}")
        print(f"📋 Health record ready for agent use!")
        print(f"\\n⚠️  Next steps:")
        print(f"1. Review 'Unconfirmed Findings' section")
        print(f"2. Confirm which medications are currently active")
        print(f"3. Validate condition status (active/resolved)")
        print(f"4. Add missing information (allergies, family history)")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()