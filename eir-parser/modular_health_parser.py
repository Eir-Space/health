#!/usr/bin/env python3
"""
Modular Health Parser - Generate lightweight, modular health record structure
"""

import os
from datetime import datetime
from pathlib import Path
from robust_journal_parser import RobustJournalParser

class ModularHealthGenerator:
    """Generate modular health record structure"""
    
    def __init__(self, output_dir="health"):
        self.output_dir = Path(output_dir)
        self.data_dir = self.output_dir / "data"
        
    def generate_modular_structure(self, journal_file: str, patient_name: str = "Patient") -> None:
        """Generate complete modular health structure from journal"""
        
        # Create directory structure
        self.output_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        
        # Parse the journal
        parser = RobustJournalParser()
        extracted_data = parser.parse_journal(journal_file)
        
        # Copy source data
        self._copy_source_data(journal_file)
        
        # Generate modular files
        self._generate_main_health_md(extracted_data, patient_name)
        self._generate_family_history_md()
        self._generate_medications_md(extracted_data)
        self._generate_providers_md(extracted_data)
        self._generate_timeline_md(extracted_data)
        
        # Generate full backup in data folder
        full_health_md = parser.generate_health_md(str(self.data_dir / "full_health_record.md"))
        
        print(f"✅ Generated modular health structure in: {self.output_dir}")
        print(f"📁 Structure:")
        print(f"  📄 health.md (main overview)")
        print(f"  📄 family-history.md")
        print(f"  📄 medications.md") 
        print(f"  📄 providers.md")
        print(f"  📄 timeline.md")
        print(f"  📂 data/ (source files)")
    
    def _copy_source_data(self, journal_file: str):
        """Copy source data to data folder"""
        import shutil
        
        source_file = Path(journal_file)
        dest_file = self.data_dir / source_file.name
        shutil.copy2(source_file, dest_file)
    
    def _generate_main_health_md(self, extracted_data: dict, patient_name: str):
        """Generate lightweight main health.md file"""
        
        demographics = extracted_data['demographics']
        timestamp = datetime.now().strftime('%Y-%m-%d')
        
        content = f"""# Health Record - {patient_name}

**Overview:** Comprehensive health profile compiled from {demographics.get('total_entries', 'multiple')} healthcare entries
**Last Updated:** {timestamp}
**Data Sources:** [Healthcare Journal](./data/), User Input

## Core Information

- **Age:** {demographics.get('age', 'Not specified')} (Born: {demographics.get('birth_date', 'Not specified')})
- **Healthcare Span:** {demographics.get('data_span', {}).get('start', 'Unknown')} to {demographics.get('data_span', {}).get('end', 'Present')}
- **Primary Provider:** {self._get_primary_provider(extracted_data)}

## Health Components

### 👪 [Family History](./family-history.md)
**Key Risk Factors:**
- *[Family medical history and genetic risk factors]*
- **Action:** Review and update family history details

### 💊 [Medications](./medications.md)  
**Current Status:**
- {len(extracted_data['medications'])} medication mentions in records
- **Action:** Confirm current medication status

### 🏥 [Healthcare Providers](./providers.md)
**Care Team:**
- {len(extracted_data['providers'])} healthcare providers over time
- **Action:** Update current provider contact information

### 📅 [Timeline](./timeline.md)
**Recent Activity:**
- {len(extracted_data['timeline'])} healthcare interactions documented
- **Action:** Review recent healthcare activities

## Active Health Contexts

### Monitoring Needs
- *Based on extracted health data and family history*
- Regular health screenings recommended
- Preventive care coordination

## Quick Health Status

| Area | Status | Last Update | Notes |
|------|--------|-------------|-------|
| General Health | Monitor | {timestamp} | Based on healthcare journal |
| Medications | Review | {timestamp} | Confirm current usage |
| Providers | Update | {timestamp} | Verify contact information |

## Information Gaps

- [ ] Current medication list confirmation
- [ ] Recent lab results and vital signs
- [ ] Allergy information
- [ ] Current health symptoms/concerns
- [ ] Family medical history details

## Data Sources

- **Raw Data:** [`./data/`](./data/) - Original exports and documents
- **Full Record:** [`./data/full_health_record.md`](./data/full_health_record.md) - Complete parsed version

---

*This file serves as the main health overview. Detailed information is in the linked component files.*
"""
        
        with open(self.output_dir / "health.md", 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_family_history_md(self):
        """Generate template family history file"""
        
        content = """# Family History

**Risk Assessment:** To be documented based on family medical history
**Last Updated:** {timestamp}
**Source:** User input required

## Family Medical History

### Paternal Side

**Father**
- **Medical Conditions:** *[To be documented]*
- **Age/Status:** *[To be documented]*

**Paternal Grandfather**
- **Medical Conditions:** *[To be documented]*
- **Age at Events:** *[To be documented]*

**Paternal Grandmother**
- **Medical Conditions:** *[To be documented]*
- **Age at Events:** *[To be documented]*

### Maternal Side

**Mother**
- **Medical Conditions:** *[To be documented]*
- **Age/Status:** *[To be documented]*

**Maternal Grandfather**
- **Medical Conditions:** *[To be documented]*
- **Age at Events:** *[To be documented]*

**Maternal Grandmother**
- **Medical Conditions:** *[To be documented]*
- **Age at Events:** *[To be documented]*

## Risk Assessment

### Known Patterns
- *[Document any known family health patterns]*

### Clinical Implications
- *[Document screening recommendations based on family history]*

## Information Needed

- [ ] Complete family medical history
- [ ] Ages at onset for significant conditions
- [ ] Current health status of living family members
- [ ] Genetic conditions or syndromes
- [ ] Cause of death for deceased family members

---

*Family history significantly impacts health screening and prevention strategies.*
""".format(timestamp=datetime.now().strftime('%Y-%m-%d'))
        
        with open(self.output_dir / "family-history.md", 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_medications_md(self, extracted_data: dict):
        """Generate medications file from extracted data"""
        
        timestamp = datetime.now().strftime('%Y-%m-%d')
        
        content = f"""# Medications

**Current Status:** Needs confirmation and update
**Last Updated:** {timestamp}
**Sources:** Healthcare journal analysis

## Current Medications

*[To be confirmed with healthcare provider]*

## Medications Mentioned in Healthcare Records

"""
        
        # Add medications found in records
        unique_meds = {}
        for med in extracted_data['medications']:
            name = med['name']
            if name not in unique_meds:
                unique_meds[name] = []
            unique_meds[name].append(med)
        
        if unique_meds:
            for med_name, mentions in unique_meds.items():
                latest = max(mentions, key=lambda x: x['mentioned_date'])
                content += f"""### {med_name}
- **First Mentioned:** {mentions[0]['mentioned_date']}
- **Latest Mention:** {latest['mentioned_date']}
- **Total Mentions:** {len(mentions)}
- **Context:** {latest['context'][:100]}...
- **Status:** Requires confirmation

"""
        else:
            content += "*No medications detected in healthcare records*\n\n"
        
        content += """## Information Gaps

- [ ] Current daily medications
- [ ] As-needed medications  
- [ ] Vitamins and supplements
- [ ] Drug allergies and reactions
- [ ] Medication adherence status

## Safety Considerations

- Document all allergies and adverse reactions
- Review drug interactions for any current medications
- Consider medical history when prescribing new medications

---

*Maintain accurate medication list for healthcare provider consultations.*
"""
        
        with open(self.output_dir / "medications.md", 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_providers_md(self, extracted_data: dict):
        """Generate providers file from extracted data"""
        
        timestamp = datetime.now().strftime('%Y-%m-%d')
        
        content = f"""# Healthcare Providers

**Care Team Overview:** Based on {len(extracted_data['providers'])} healthcare providers in records
**Last Updated:** {timestamp}
**Source:** Healthcare journal analysis

## Current Active Providers

*[To be confirmed and updated]*

## Providers from Healthcare Records

"""
        
        # List providers from records
        providers = sorted(list(extracted_data['providers']))[:10]  # Top 10
        for provider in providers:
            if len(provider) > 10:  # Filter out very short entries
                content += f"""### {provider}
- **Source:** Healthcare records
- **Status:** Historical relationship
- **Contact Info:** *[To be updated]*

"""
        
        content += """## Provider Categories

### Primary Care
- *[Document current primary care provider]*

### Specialists  
- *[Document current specialist relationships]*

### Emergency Care
- *[Document preferred emergency providers]*

### Dental Care
- *[Document current dental provider]*

## Information Needed

- [ ] Current primary care provider contact information
- [ ] Active specialist relationships
- [ ] Preferred emergency care locations
- [ ] Insurance network considerations
- [ ] Provider communication preferences

---

*Maintain updated provider contact information for healthcare coordination.*
"""
        
        with open(self.output_dir / "providers.md", 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_timeline_md(self, extracted_data: dict):
        """Generate timeline file from extracted data"""
        
        timestamp = datetime.now().strftime('%Y-%m-%d')
        
        content = f"""# Healthcare Timeline

**Overview:** {len(extracted_data['timeline'])} documented healthcare interactions
**Last Updated:** {timestamp}
**Source:** Healthcare journal analysis

## Recent Healthcare Activity

"""
        
        # Show recent timeline entries
        recent_timeline = sorted([t for t in extracted_data['timeline'] if t['date'] != 'Unknown'], 
                               key=lambda x: x['date'], reverse=True)[:8]
        
        for entry in recent_timeline:
            content += f"""### {entry['date']}: {entry['type']}
- **Provider:** {entry['provider']}
- **Category:** {entry['category']}
- **Details:** {entry['details'][:150]}...

"""
        
        content += """## Healthcare Patterns

### Utilization Analysis
- Healthcare engagement over time
- Provider relationship patterns
- Emergency vs routine care usage

### Care Coordination
- Referral patterns between providers
- Communication between care team members
- Follow-up compliance

## Significant Events

*[Document major health events, diagnoses, procedures]*

## Future Healthcare Planning

### Upcoming Appointments
- *[Document scheduled appointments]*

### Screening Due Dates
- *[Document upcoming preventive care]*

### Follow-up Needs
- *[Document required follow-up care]*

---

*Healthcare timeline provides context for current health status and future planning.*
"""
        
        with open(self.output_dir / "timeline.md", 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _get_primary_provider(self, extracted_data: dict) -> str:
        """Extract likely primary provider from data"""
        
        providers = list(extracted_data['providers'])
        
        # Look for primary care patterns
        for provider in providers:
            if any(term in provider.lower() for term in ['vårdcentral', 'primary', 'family']):
                return provider
        
        return "To be determined"

def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 modular_health_parser.py <journal_file>")
        sys.exit(1)
    
    journal_file = sys.argv[1]
    patient_name = Path(journal_file).stem.replace('_health_journal', '').replace('_', ' ').title()
    
    try:
        print("🏗️  Generating Modular Health Structure")
        print("=" * 40)
        
        generator = ModularHealthGenerator()
        generator.generate_modular_structure(journal_file, patient_name)
        
        print(f"\\n🎯 Modular health structure ready!")
        print(f"📋 Main file: health/health.md")
        print(f"🔗 Component files: family-history.md, medications.md, providers.md, timeline.md")
        print(f"📁 Source data: health/data/")
        
        print(f"\\n📝 Next steps:")
        print(f"1. Review health/health.md for overview")
        print(f"2. Update health/family-history.md with family medical history")
        print(f"3. Confirm current medications in health/medications.md")
        print(f"4. Update provider information in health/providers.md")
        print(f"5. Review timeline in health/timeline.md")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()