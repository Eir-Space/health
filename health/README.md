# Health Record Structure

**Lightweight, modular health record system**

## Overview

This health folder contains a modular approach to health record management, with the main overview file linking to specific component files for detailed information.

## Structure

```
health/
├── health.md           # Main overview (lightweight index)
├── family-history.md   # Family medical history & genetic risks
├── medications.md      # Current & historical medications
├── providers.md        # Healthcare provider relationships
├── timeline.md         # Healthcare events & visits
├── data/               # Raw source data & backups
│   ├── birger_health_journal.yml           # Original 1177.se export
│   └── birger_health_20260314_2325.md      # Full parsed record
└── README.md          # This file
```

## File Purposes

### 📄 Main Files

**`health.md`** - Primary health overview
- Quick health status summary
- Links to all component files
- Current health contexts
- Information gaps
- Last updated status

**`family-history.md`** - Family medical history
- Genetic risk factors
- Family health patterns
- Clinical implications for screening
- Risk assessment summary

**`medications.md`** - Medication management
- Current medications
- Historical medications
- Drug allergies and reactions
- Safety considerations

**`providers.md`** - Healthcare team
- Current active providers
- Historical provider relationships
- Contact information
- Care coordination notes

**`timeline.md`** - Healthcare chronology
- Recent healthcare activities
- Significant health events
- Healthcare utilization patterns
- Future planning

### 📂 Data Folder

**`data/`** - Source files and backups
- Original healthcare exports
- Full structured health records
- Document backups
- Raw data preservation

## Usage Patterns

### Daily Reference
- Check `health.md` for quick overview
- Review specific component files as needed

### Healthcare Visits
- Bring relevant component files
- Update information after visits
- Add new findings to appropriate files

### Health Planning
- Review `family-history.md` for risk factors
- Check `timeline.md` for due screenings
- Update `providers.md` with new relationships

## Maintenance

### Regular Updates
1. **After healthcare visits:** Update relevant component files
2. **New medications:** Add to `medications.md`
3. **Provider changes:** Update `providers.md`
4. **Family history changes:** Update `family-history.md`
5. **Timeline events:** Add to `timeline.md`

### File Relationships
- `health.md` links to all component files
- Component files reference each other when relevant
- `data/` folder preserves original sources

## Benefits

### Lightweight Structure
- Main file stays concise and scannable
- Detailed information in focused component files
- Easy to share specific sections with providers

### Modular Maintenance
- Update only relevant sections
- Easier to review and verify information
- Component files can be shared independently

### Source Preservation
- Original data preserved in `data/` folder
- Full structured record available as backup
- Ability to regenerate structure from source

## Agent Integration

This structure is designed to work well with AI agents:
- **health.md** provides quick context
- **Component files** offer detailed information when needed
- **Linked structure** allows agents to navigate relevant information
- **Source data** enables re-processing and updates

---

*This modular approach makes health information more manageable while maintaining comprehensive coverage.*