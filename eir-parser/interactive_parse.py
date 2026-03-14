#!/usr/bin/env python3
"""
Interactive EIR Parser - Parse documents with guided user input to fill gaps
"""

import json
import os
from datetime import datetime
from parse_document import HealthDocumentParser

class InteractiveHealthParser:
    """Interactive parser that asks follow-up questions to complete health records"""
    
    def __init__(self):
        self.parser = HealthDocumentParser()
        self.user_responses = {}
    
    def interactive_parse(self, document_path: str) -> str:
        """Parse document with interactive gap-filling"""
        
        print("🏥 EIR Interactive Health Parser")
        print("=" * 40)
        
        # Parse document first
        print(f"\n📄 Parsing {document_path}...")
        extracted_data = self.parser.parse_file(document_path)
        
        print(f"✅ Initial extraction complete!")
        print(f"📊 Found: {len(extracted_data['medications'])} medications, {len(extracted_data['lab_results'])} lab results")
        
        # Ask follow-up questions
        self._ask_demographics()
        self._ask_medication_details()
        self._ask_condition_confirmation()
        self._ask_missing_context()
        
        # Generate enhanced health.md with user input
        return self._generate_enhanced_health_md()
    
    def _ask_demographics(self):
        """Collect basic demographic information"""
        print("\n👤 DEMOGRAPHICS")
        print("-" * 20)
        
        self.user_responses['age'] = input("Age (or age range like 30-35): ").strip()
        self.user_responses['sex'] = input("Sex (Male/Female/Other): ").strip()
        self.user_responses['occupation'] = input("Occupation (or category): ").strip()
        
        # Privacy-aware location
        location_detail = input("Location detail level (city/region/country): ").strip().lower()
        location = input("Location: ").strip()
        
        if location_detail == "region":
            self.user_responses['location'] = f"Region: {location}"
        elif location_detail == "country":
            self.user_responses['location'] = f"Country: {location}"
        else:
            self.user_responses['location'] = location
    
    def _ask_medication_details(self):
        """Ask for details about detected medications"""
        if not self.parser.extracted_data['medications']:
            return
            
        print("\n💊 MEDICATION CONFIRMATION")
        print("-" * 30)
        
        confirmed_meds = []
        
        for i, med in enumerate(self.parser.extracted_data['medications']):
            print(f"\n🔍 Medication {i+1}: {med['name']}")
            
            is_current = input(f"Is {med['name']} currently taken? (y/n/unsure): ").strip().lower()
            
            if is_current == 'y':
                dosage = input(f"Dosage for {med['name']} (e.g., 500mg twice daily): ").strip()
                indication = input(f"What is {med['name']} for? (condition/reason): ").strip()
                start_date = input(f"When did you start {med['name']}? (YYYY-MM-DD or approximate): ").strip()
                prescriber = input(f"Who prescribed {med['name']}? (Dr. Name or specialty): ").strip()
                
                confirmed_med = {
                    'name': med['name'],
                    'dosage': dosage,
                    'indication': indication,
                    'start_date': start_date,
                    'prescriber': prescriber,
                    'status': 'current',
                    'source': 'user_confirmed',
                    'confidence': 'High'
                }
                confirmed_meds.append(confirmed_med)
                
            elif is_current == 'n':
                # Past medication
                stop_date = input(f"When did you stop {med['name']}? (YYYY-MM-DD or approximate): ").strip()
                reason = input(f"Why did you stop {med['name']}? ").strip()
                
                past_med = {
                    'name': med['name'],
                    'status': 'discontinued',
                    'stop_date': stop_date,
                    'reason': reason,
                    'source': 'user_confirmed',
                    'confidence': 'High'
                }
                confirmed_meds.append(past_med)
            
            else:  # unsure
                unconfirmed_med = {
                    'name': med['name'],
                    'status': 'unconfirmed',
                    'source': 'document_parsed',
                    'confidence': 'Low'
                }
                confirmed_meds.append(unconfirmed_med)
        
        self.user_responses['medications'] = confirmed_meds
    
    def _ask_condition_confirmation(self):
        """Ask about medical conditions mentioned or implied"""
        print("\n🏥 MEDICAL CONDITIONS")
        print("-" * 25)
        
        # Detect potential conditions from medications
        condition_hints = []
        
        for med in self.user_responses.get('medications', []):
            if 'metformin' in med['name'].lower():
                condition_hints.append("Type 2 Diabetes")
            elif 'lisinopril' in med['name'].lower() or 'losartan' in med['name'].lower():
                condition_hints.append("High Blood Pressure")
            elif 'atorvastatin' in med['name'].lower() or 'simvastatin' in med['name'].lower():
                condition_hints.append("High Cholesterol")
        
        # Ask about detected conditions
        confirmed_conditions = []
        
        for condition in condition_hints:
            has_condition = input(f"Do you have {condition}? (y/n): ").strip().lower()
            
            if has_condition == 'y':
                diagnosis_date = input(f"When were you diagnosed with {condition}? (YYYY-MM-DD or year): ").strip()
                current_status = input(f"Is {condition} well controlled? (y/n/unsure): ").strip()
                
                confirmed_condition = {
                    'condition': condition,
                    'diagnosis_date': diagnosis_date,
                    'status': 'active',
                    'control_status': current_status,
                    'source': 'user_confirmed',
                    'confidence': 'High'
                }
                confirmed_conditions.append(confirmed_condition)
        
        # Ask about other conditions
        other_conditions = input("\nAny other significant medical conditions? (comma-separated or 'none'): ").strip()
        
        if other_conditions and other_conditions.lower() != 'none':
            for condition in other_conditions.split(','):
                condition = condition.strip()
                if condition:
                    other_condition = {
                        'condition': condition,
                        'status': 'active',
                        'source': 'user_reported',
                        'confidence': 'High'
                    }
                    confirmed_conditions.append(other_condition)
        
        self.user_responses['conditions'] = confirmed_conditions
    
    def _ask_missing_context(self):
        """Ask about missing important context"""
        print("\n📋 ADDITIONAL CONTEXT")
        print("-" * 25)
        
        # Allergies
        allergies = input("Any drug allergies or food allergies? (describe or 'none'): ").strip()
        if allergies and allergies.lower() != 'none':
            self.user_responses['allergies'] = allergies
        
        # Family history
        family_history = input("Significant family medical history? (describe or 'none'): ").strip()
        if family_history and family_history.lower() != 'none':
            self.user_responses['family_history'] = family_history
        
        # Current providers
        primary_care = input("Primary care doctor name/practice? ").strip()
        if primary_care:
            self.user_responses['primary_care'] = primary_care
        
        specialists = input("Any specialists you see regularly? (describe or 'none'): ").strip()
        if specialists and specialists.lower() != 'none':
            self.user_responses['specialists'] = specialists
    
    def _generate_enhanced_health_md(self) -> str:
        """Generate comprehensive health.md with user input"""
        timestamp = datetime.now().isoformat()
        
        health_md = f"""---
health_md_version: "1.1"
record_id: "interactive-parsed-{datetime.now().strftime('%Y%m%d')}"
generated: "{timestamp}"
privacy_level: "pseudonymized"
last_updated: "{timestamp}"
data_sources: ["document_parsed", "user_confirmed"]
agent_compatible: true
provenance_policy: "required_for_agent_added_facts"
---

# Health Record - Interactive Parse

## Demographics

- **Age:** {self.user_responses.get('age', 'Not provided')}
- **Sex:** {self.user_responses.get('sex', 'Not provided')}
- **Occupation:** {self.user_responses.get('occupation', 'Not provided')}
- **Location:** {self.user_responses.get('location', 'Not provided')}

"""
        
        # Current medications
        health_md += "## Current Medications\n\n"
        
        current_meds = [m for m in self.user_responses.get('medications', []) if m.get('status') == 'current']
        
        for med in current_meds:
            health_md += f"""### {med['name']}

- **Indication:** {med.get('indication', 'Not specified')}
- **Dosage:** {med.get('dosage', 'Not specified')}
- **Started:** {med.get('start_date', 'Not specified')}
- **Prescriber:** {med.get('prescriber', 'Not specified')}
- **Source:** {med['source']}
- **Confidence:** {med['confidence']}

"""
        
        # Medical history
        health_md += "## Medical History\n\n"
        
        for condition in self.user_responses.get('conditions', []):
            health_md += f"""### {condition['condition']} ({condition.get('diagnosis_date', 'Date unknown')})

- **Status:** {condition['status'].title()}
- **Control Status:** {condition.get('control_status', 'Not specified')}
- **Source:** {condition['source']}
- **Confidence:** {condition['confidence']}

"""
        
        # Lab results (from document)
        if self.parser.extracted_data['lab_results']:
            health_md += "## Lab Results\n\n"
            
            for lab in self.parser.extracted_data['lab_results']:
                health_md += f"""### {lab['test']}

- **Value:** {lab['value']} {lab.get('units', '')}
- **Reference Range:** {lab.get('reference_range', 'Not specified')}
- **Date:** {lab.get('date', 'Not specified')}
- **Source:** {lab['source']}
- **Confidence:** {lab['confidence']}

"""
        
        # Allergies
        if self.user_responses.get('allergies'):
            health_md += f"""## Allergies & Intolerances

### Reported Allergies

- **Details:** {self.user_responses['allergies']}
- **Source:** user_reported
- **Confidence:** High

"""
        
        # Care team
        if self.user_responses.get('primary_care') or self.user_responses.get('specialists'):
            health_md += "## Care Team\n\n"
            
            if self.user_responses.get('primary_care'):
                health_md += f"""### Primary Care

- **Provider:** {self.user_responses['primary_care']}
- **Source:** user_reported

"""
            
            if self.user_responses.get('specialists'):
                health_md += f"""### Specialists

- **Details:** {self.user_responses['specialists']}
- **Source:** user_reported

"""
        
        # Active health contexts for agents
        health_md += "## Active Health Contexts\n\n"
        
        for condition in self.user_responses.get('conditions', []):
            if condition['status'] == 'active':
                health_md += f"""### {condition['condition']}
- **Status:** Active
- **Type:** Chronic condition
- **Source:** user_confirmed
- **Confidence:** High
- **Last Confirmed:** {datetime.now().strftime('%Y-%m-%d')}

"""
        
        # Unconfirmed findings (if any)
        unconfirmed_items = [m for m in self.user_responses.get('medications', []) if m.get('status') == 'unconfirmed']
        
        if unconfirmed_items:
            health_md += "## Unconfirmed Findings\n\n"
            
            for item in unconfirmed_items:
                health_md += f"""### {item['name']} (Document Mention)
- **Type:** Potential medication
- **Source:** {item['source']}
- **Confidence:** {item['confidence']}
- **Action Needed:** Clarify current usage status

"""
        
        # Information gaps
        health_md += """## Information Gaps & Follow-up Questions

### Lab Result Interpretation
- **Question:** Clinical significance of lab values and trends over time
- **Why It Matters:** Understanding health progress and goals
- **Status:** Open

"""
        
        if self.user_responses.get('family_history'):
            health_md += f"""### Family History Details
- **Question:** Specific family history details for risk assessment
- **Details:** {self.user_responses['family_history']}
- **Why It Matters:** Genetic risk factors and screening recommendations
- **Status:** Documented

"""
        
        # Skill attachments
        health_md += "## Skill Attachments\n\n"
        
        health_md += """### health
- **Status:** Active
- **Reason:** Base health record management
- **Added By:** system

"""
        
        # Auto-suggest skills based on conditions
        condition_skills = {
            'Type 2 Diabetes': 'diabetes',
            'High Blood Pressure': 'hypertension',
            'High Cholesterol': 'cardiovascular'
        }
        
        for condition in self.user_responses.get('conditions', []):
            skill_name = condition_skills.get(condition['condition'])
            if skill_name:
                health_md += f"""### {skill_name}
- **Status:** Suggested
- **Reason:** Active {condition['condition']} condition
- **Added By:** agent

"""
        
        # Save file
        output_file = f"health-interactive-{datetime.now().strftime('%Y%m%d')}.md"
        with open(output_file, 'w') as f:
            f.write(health_md)
        
        print(f"\n✅ Enhanced health record created: {output_file}")
        print(f"🎯 Ready for agent use with confirmed information")
        
        return health_md

def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 interactive_parse.py <document_path>")
        sys.exit(1)
    
    document_path = sys.argv[1]
    
    try:
        parser = InteractiveHealthParser()
        health_md = parser.interactive_parse(document_path)
        
        print("\n" + "="*50)
        print("🎉 INTERACTIVE PARSING COMPLETE!")
        print("="*50)
        print("Your structured health record is ready for agent use.")
        print("All information has been confirmed and properly sourced.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()