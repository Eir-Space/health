#!/usr/bin/env python3
"""
Robust Swedish Healthcare Journal Parser - Handle various export formats
"""

import re
import json
from datetime import datetime
from typing import Dict, List

class RobustJournalParser:
    """Parse Swedish healthcare journals with flexible format handling"""
    
    def __init__(self):
        self.extracted_data = {
            'demographics': {},
            'medications': [],
            'conditions': [],
            'lab_results': [],
            'providers': set(),
            'timeline': [],
            'visits': []
        }
    
    def parse_journal(self, file_path: str) -> Dict:
        """Parse Swedish healthcare journal with flexible format handling"""
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract basic info with regex
        self._extract_patient_info(content)
        self._extract_healthcare_entries(content)
        self._extract_providers(content)
        
        return self.extracted_data
    
    def _extract_patient_info(self, content: str):
        """Extract patient demographics"""
        
        # Extract name
        name_match = re.search(r'name:\s*["\']([^"\']+)["\']', content)
        if name_match:
            self.extracted_data['demographics']['name'] = name_match.group(1)
        
        # Extract birth date and calculate age
        birth_match = re.search(r'birth_date:\s*["\'](\d{4}-\d{2}-\d{2})["\']', content)
        if birth_match:
            birth_date = birth_match.group(1)
            self.extracted_data['demographics']['birth_date'] = birth_date
            
            try:
                birth_year = int(birth_date[:4])
                current_year = datetime.now().year
                age = current_year - birth_year
                self.extracted_data['demographics']['age'] = age
            except:
                pass
        
        # Extract personal number
        personal_match = re.search(r'personal_number:\s*["\']([^"\']+)["\']', content)
        if personal_match:
            self.extracted_data['demographics']['personal_number'] = personal_match.group(1)
        
        # Extract total entries
        total_match = re.search(r'total_entries:\s*(\d+)', content)
        if total_match:
            self.extracted_data['demographics']['total_entries'] = int(total_match.group(1))
        
        # Extract date range
        start_match = re.search(r'start:\s*["\']([^"\']+)["\']', content)
        end_match = re.search(r'end:\s*["\']([^"\']+)["\']', content)
        if start_match and end_match:
            self.extracted_data['demographics']['data_span'] = {
                'start': start_match.group(1),
                'end': end_match.group(1)
            }
    
    def _extract_healthcare_entries(self, content: str):
        """Extract healthcare entries and timeline"""
        
        # Find all entry blocks
        entry_pattern = r'id:\s*["\']entry_\d+["\'].*?(?=id:\s*["\']entry_|$)'
        entries = re.finditer(entry_pattern, content, re.DOTALL)
        
        for entry_match in entries:
            entry_text = entry_match.group(0)
            self._process_single_entry(entry_text)
    
    def _process_single_entry(self, entry_text: str):
        """Process individual healthcare entry"""
        
        # Extract basic entry information
        date_match = re.search(r'date:\s*["\']([^"\']*)["\']', entry_text)
        type_match = re.search(r'type:\s*["\']([^"\']*)["\']', entry_text)
        category_match = re.search(r'category:\s*["\']([^"\']*)["\']', entry_text)
        
        date = date_match.group(1) if date_match else 'Unknown'
        entry_type = type_match.group(1) if type_match else 'Unknown'
        category = category_match.group(1) if category_match else 'Unknown'
        
        # Extract provider info
        provider_name = 'Unknown'
        provider_matches = re.findall(r'name:\s*["\']([^"\']*vårdcentral[^"\']*|[^"\']*sjukhus[^"\']*|[^"\']*klinik[^"\']*)["\']', entry_text)
        if provider_matches:
            provider_name = provider_matches[0]
            self.extracted_data['providers'].add(provider_name)
        
        # Extract responsible person
        responsible_match = re.search(r'role:\s*["\']([^"\']*)["\']', entry_text)
        responsible = responsible_match.group(1) if responsible_match else ''
        
        # Extract content details
        details_matches = re.findall(r'details:\s*["\']([^"\']*)["\']', entry_text)
        details = ' '.join(details_matches) if details_matches else ''
        
        # Create timeline entry
        timeline_entry = {
            'date': date,
            'type': entry_type,
            'category': category,
            'provider': provider_name,
            'responsible': responsible,
            'details': details[:300] + '...' if len(details) > 300 else details
        }
        self.extracted_data['timeline'].append(timeline_entry)
        
        # Extract medical information from text
        full_text = entry_text + ' ' + details
        self._extract_medical_info_from_swedish_text(full_text, date, provider_name)
    
    def _extract_providers(self, content: str):
        """Extract all healthcare providers mentioned"""
        
        # Swedish provider patterns
        provider_patterns = [
            r'vårdcentral[^"\']*',
            r'sjukhus[^"\']*',
            r'universitetssjukhus[^"\']*',
            r'klinik[^"\']*',
            r'mottagning[^"\']*',
            r'folktandvård[^"\']*'
        ]
        
        for pattern in provider_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                provider = match.group(0).strip()
                if len(provider) > 5:  # Avoid short matches
                    self.extracted_data['providers'].add(provider)
    
    def _extract_medical_info_from_swedish_text(self, text: str, date: str, provider: str):
        """Extract medical information from Swedish healthcare text"""
        
        text_lower = text.lower()
        
        # Swedish medication patterns
        med_patterns = [
            r'(alvedon|panodil|ipren|voltaren|treo)',  # Pain relief
            r'(omeprazol|losec|nexium)',               # PPI
            r'(simvastatin|atorvastatin)',             # Statins
            r'(metformin|insulin)',                    # Diabetes
            r'(lisinopril|enalapril|losartan)',        # Blood pressure
            r'(warfarin|apixaban)',                    # Anticoagulants
            r'(sertralin|citalopram|fluoxetin)',       # Antidepressants
            r'(antibiotika|penicillin|amoxicillin)',   # Antibiotics
        ]
        
        for pattern in med_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                medication = {
                    'name': match.group(1).title(),
                    'mentioned_date': date,
                    'provider': provider,
                    'context': self._get_context(text, match.start(), 80),
                    'source': 'swedish_journal_inferred',
                    'confidence': 'Medium'
                }
                # Avoid duplicates
                if not any(med['name'] == medication['name'] and med['mentioned_date'] == date 
                          for med in self.extracted_data['medications']):
                    self.extracted_data['medications'].append(medication)
        
        # Swedish condition/diagnosis patterns
        condition_patterns = [
            r'(diabetes|diabetiker)',
            r'(hypertoni|högt blodtryck)',
            r'(hyperlipidemi|högt kolesterol)',
            r'(astma|allergi)',
            r'(depression|ångest|nedstämdhet)',
            r'(hjärtproblem|hjärtkärlsjukdom)',
            r'(artrit|ledvärk)',
            r'(migrän|huvudvärk)',
            r'(sömnproblem|insomni)',
            r'(nefrit|njurproblem)',
            r'(genetisk|ärftlig)',
        ]
        
        for pattern in condition_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                condition = {
                    'condition': match.group(1).title(),
                    'mentioned_date': date,
                    'provider': provider,
                    'context': self._get_context(text, match.start(), 100),
                    'source': 'swedish_journal_inferred',
                    'confidence': 'Low'  # Requires confirmation
                }
                # Avoid duplicates
                if not any(cond['condition'] == condition['condition'] and cond['mentioned_date'] == date 
                          for cond in self.extracted_data['conditions']):
                    self.extracted_data['conditions'].append(condition)
        
        # Lab/measurement patterns
        lab_patterns = [
            r'(blodtryck).*?(\d+/\d+)',
            r'(vikt).*?(\d+\.?\d*)\s*kg',
            r'(längd).*?(\d+)\s*cm',
            r'(puls).*?(\d+)',
            r'(temperatur).*?(\d+\.?\d*)',
        ]
        
        for pattern in lab_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                lab = {
                    'test': match.group(1).title(),
                    'value': match.group(2),
                    'date': date,
                    'provider': provider,
                    'source': 'swedish_journal_parsed',
                    'confidence': 'Medium'
                }
                self.extracted_data['lab_results'].append(lab)
    
    def _get_context(self, text: str, position: int, context_chars: int = 100) -> str:
        """Get surrounding context"""
        start = max(0, position - context_chars)
        end = min(len(text), position + context_chars)
        return text[start:end].replace('\\n', ' ').strip()
    
    def generate_health_md(self, output_file="birger_health_parsed.md") -> str:
        """Generate comprehensive health.md"""
        
        timestamp = datetime.now().isoformat()
        demographics = self.extracted_data['demographics']
        
        health_md = f"""---
health_md_version: "1.1"
record_id: "birger-moell-swedish-journal"
generated: "{timestamp}"
privacy_level: "identified"
last_updated: "{timestamp}"
data_sources: ["swedish_healthcare_journal_1177", "robust_parser"]
agent_compatible: true
provenance_policy: "required_for_agent_added_facts"
---

# Health Record - {demographics.get('name', 'Birger Moell')}
*Compiled from 25 Years of Swedish Healthcare Data (1177.se)*

## Demographics

- **Name:** {demographics.get('name', 'Birger Moell')}
- **Age:** {demographics.get('age', 'Not calculated')} (Born: {demographics.get('birth_date', '1986-02-28')})
- **Personal Number:** {demographics.get('personal_number', 'Protected')}
- **Healthcare Data Span:** {demographics.get('data_span', {}).get('start', '2001')} to {demographics.get('data_span', {}).get('end', '2026')}
- **Total Healthcare Entries:** {demographics.get('total_entries', '43+')} entries over 25 years

## Clinical Timeline (Recent Entries)

"""
        
        # Show recent timeline entries
        recent_timeline = sorted([t for t in self.extracted_data['timeline'] if t['date'] != 'Unknown'], 
                               key=lambda x: x['date'], reverse=True)[:8]
        
        for entry in recent_timeline:
            health_md += f"""### {entry['date']}: {entry['type']}

- **Category:** {entry['category']}
- **Provider:** {entry['provider']}
- **Details:** {entry['details']}

"""
        
        # Add medications section
        if self.extracted_data['medications']:
            health_md += """## Medication Mentions (Require Confirmation)

*Medications mentioned in healthcare records - current status needs verification*

"""
            
            # Group by medication name
            unique_meds = {}
            for med in self.extracted_data['medications']:
                name = med['name']
                if name not in unique_meds:
                    unique_meds[name] = []
                unique_meds[name].append(med)
            
            for med_name, mentions in unique_meds.items():
                latest_mention = max(mentions, key=lambda x: x['mentioned_date'])
                health_md += f"""### {med_name}

- **First Mentioned:** {mentions[0]['mentioned_date']}
- **Latest Mention:** {latest_mention['mentioned_date']}
- **Total Mentions:** {len(mentions)}
- **Recent Provider:** {latest_mention['provider']}
- **Context:** {latest_mention['context'][:150]}...
- **Source:** {latest_mention['source']}
- **Confidence:** {latest_mention['confidence']}

"""
        
        # Add lab results
        if self.extracted_data['lab_results']:
            health_md += """## Vital Signs & Measurements

"""
            for lab in self.extracted_data['lab_results'][-10:]:  # Last 10
                health_md += f"""### {lab['test']} ({lab['date']})

- **Value:** {lab['value']}
- **Provider:** {lab['provider']}
- **Source:** {lab['source']}

"""
        
        # Add care team
        health_md += """## Care Team (From 25 Years of Records)

"""
        
        for provider in sorted(list(self.extracted_data['providers']))[:15]:
            health_md += f"""### {provider}

- **Source:** swedish_healthcare_journal
- **Relationship:** Provider mentioned in healthcare records

"""
        
        # Add unconfirmed findings
        health_md += """## Unconfirmed Findings

*Medical conditions mentioned in 25 years of healthcare records - require confirmation*

"""
        
        # Group conditions
        unique_conditions = {}
        for cond in self.extracted_data['conditions']:
            name = cond['condition']
            if name not in unique_conditions:
                unique_conditions[name] = []
            unique_conditions[name].append(cond)
        
        for cond_name, mentions in unique_conditions.items():
            latest_mention = max(mentions, key=lambda x: x['mentioned_date'])
            health_md += f"""### {cond_name} (Multiple Journal Mentions)
- **Type:** Potential health condition
- **First Mentioned:** {mentions[0]['mentioned_date']}
- **Latest Mention:** {latest_mention['mentioned_date']}
- **Total Mentions:** {len(mentions)}
- **Recent Context:** {latest_mention['context'][:150]}...
- **Source:** {latest_mention['source']}
- **Confidence:** {latest_mention['confidence']}
- **Action Needed:** Confirm if this is an active condition

"""
        
        # Information gaps
        health_md += """## Information Gaps & Follow-up Questions

### Current Medication Status
- **Question:** Which medications mentioned in 25 years of records are currently active?
- **Why It Matters:** Accurate medication list for safety and drug interactions
- **Status:** Open

### Active vs Resolved Conditions  
- **Question:** Which conditions mentioned are currently active vs. historical?
- **Why It Matters:** Current health status for agent decision-making
- **Status:** Open

### Recent Lab Results
- **Question:** Current lab values, vital signs, and health metrics
- **Why It Matters:** Health monitoring and trend analysis
- **Status:** Open

### Allergies and Adverse Reactions
- **Question:** Drug allergies, food allergies, adverse medication reactions
- **Why It Matters:** Safety for medication and dietary recommendations
- **Status:** Open

### Family Medical History
- **Question:** Genetic conditions mentioned (clinical genetics visits noted)
- **Why It Matters:** Risk assessment and screening recommendations
- **Status:** Open

"""
        
        # Skill attachments
        health_md += """## Skill Attachments

### health
- **Status:** Active
- **Reason:** Comprehensive 25-year health record available
- **Added By:** system

### swedish-healthcare
- **Status:** Suggested
- **Reason:** Swedish healthcare system navigation and terminology
- **Added By:** agent

"""
        
        # Suggest condition-specific skills
        condition_keywords = {
            'diabetes': ['diabetes', 'diabetiker'],
            'cardiovascular': ['hypertoni', 'hjärtproblem', 'blodtryck'],
            'mental-health': ['depression', 'ångest'],
            'genetics': ['genetisk', 'ärftlig', 'klinisk genetik']
        }
        
        for skill, keywords in condition_keywords.items():
            if any(any(keyword in cond['condition'].lower() for keyword in keywords) 
                   for cond in self.extracted_data['conditions']):
                health_md += f"""### {skill}
- **Status:** Suggested
- **Reason:** Related conditions mentioned in healthcare history
- **Added By:** agent

"""
        
        # Active health contexts (empty until confirmed)
        health_md += """## Active Health Contexts

*Add confirmed conditions here after user validation*

### Example Format (After Confirmation):
```
### Type 2 Diabetes Mellitus
- **Status:** Active  
- **Type:** Chronic condition
- **Source:** user_confirmed
- **Confidence:** High
- **Last Confirmed:** [Date]
```

"""
        
        # Save file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(health_md)
        
        return health_md

def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 robust_journal_parser.py <journal_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        print("🇸🇪 Robust Swedish Healthcare Journal Parser")
        print("=" * 50)
        print(f"📄 Parsing {file_path}...")
        
        parser = RobustJournalParser()
        extracted_data = parser.parse_journal(file_path)
        
        print(f"\\n✅ Successfully parsed healthcare journal!")
        print(f"📊 Extracted from 25 years of healthcare data:")
        print(f"  👤 Patient: {extracted_data['demographics'].get('name', 'Unknown')}")
        print(f"  📅 Age: {extracted_data['demographics'].get('age', 'Unknown')}")
        print(f"  📋 Total entries: {extracted_data['demographics'].get('total_entries', 'Unknown')}")
        print(f"  💊 Medication mentions: {len(extracted_data['medications'])}")
        print(f"  🏥 Condition mentions: {len(extracted_data['conditions'])}")
        print(f"  🔬 Measurements: {len(extracted_data['lab_results'])}")
        print(f"  👨‍⚕️ Healthcare providers: {len(extracted_data['providers'])}")
        print(f"  📅 Timeline entries: {len(extracted_data['timeline'])}")
        
        # Generate health.md
        output_file = f"birger_health_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        health_md = parser.generate_health_md(output_file)
        
        print(f"\\n🎯 Generated comprehensive health record: {output_file}")
        print(f"📋 Ready for agent use with 25 years of structured healthcare data!")
        
        print(f"\\n⚠️  Important next steps:")
        print(f"1. Review 'Unconfirmed Findings' - confirm active conditions")
        print(f"2. Update 'Medication Mentions' - which are currently taken?")
        print(f"3. Add current health status and recent lab results")
        print(f"4. Fill in missing info (allergies, family history)")
        print(f"5. Move confirmed items to 'Active Health Contexts'")
        
        print(f"\\n🚀 This health.md now provides agents with unprecedented")
        print(f"   longitudinal health context spanning 25 years!")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()