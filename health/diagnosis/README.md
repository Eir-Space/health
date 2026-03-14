# Active Diagnoses

**Purpose:** Track current medical conditions that actively affect daily functioning
**Scope:** Only include active diagnoses requiring ongoing management or accommodation
**Last Updated:** 2026-03-14

## Overview

This folder contains detailed information about current medical diagnoses that impact daily life, work, or activities. Unlike the broader body/state tracking system, this focuses specifically on formal diagnoses that require active management.

## Inclusion Criteria

### Include in This Folder:
- **Active conditions** requiring daily management
- **Injuries** affecting current function
- **Chronic conditions** requiring ongoing accommodation
- **Mental health diagnoses** impacting daily activities
- **Temporary conditions** with significant functional impact

### Do NOT Include:
- **Past/resolved conditions** with no current impact
- **Risk factors** without active symptoms (use family-history.md instead)
- **Minor issues** resolved within days
- **Preventive care** items (use main health tracking)

## Current Active Diagnoses

### 🤚 [Finger Joint Injury](./finger-joint-injury.md)
**Status:** Active - High impact on daily function
**Type:** Traumatic injury
**Onset:** 2026-03-14 (fall-related)
**Impact:** Work limitations, typing difficulties, grip strength reduction
**Management:** Daily rehabilitation exercises, ergonomic modifications
**Expected Duration:** 4-6 weeks

## File Structure Standards

### Required Sections for Each Diagnosis:
1. **Clinical Summary** - Medical description and current status
2. **Daily Functional Impact** - How it affects work/life activities
3. **Current Treatment Plan** - Active interventions and goals
4. **Monitoring Parameters** - Progress tracking measures
5. **Warning Signs** - When to seek medical attention
6. **Prognosis and Timeline** - Expected recovery course

### Naming Convention:
- Use descriptive, specific names: `finger-joint-injury.md`
- Include body area when relevant: `left-knee-arthritis.md`
- Use medical terminology when appropriate: `major-depression-episode.md`

## Integration with Main Health System

### Cross-References:
- **Diagnosis files** link to detailed body/state tracking
- **Active.md** summarizes current management needs from diagnoses
- **Rehabilitation protocols** reference specific diagnosis files
- **Provider communications** can reference diagnosis summaries

### Example Integration:
```markdown
## In active.md:
- See diagnosis/finger-joint-injury.md for complete clinical picture
- Daily exercises required from body/arms/rehabilitation/finger-rehab.md

## In finger injury diagnosis:
- Detailed tracking: body/arms/left/hand/fingers/pinky.md
- Exercise protocol: body/arms/rehabilitation/finger-rehab.md
- Mental health impact: state/stress/physical-stress.md
```

## Management Workflow

### For New Diagnoses:
1. **Create diagnosis file** with complete clinical picture
2. **Update active.md** with daily management needs
3. **Create/update** relevant body/state tracking files
4. **Establish** monitoring and progress tracking routine

### For Ongoing Management:
1. **Regular updates** to diagnosis file with progress
2. **Daily tracking** in relevant body/state files
3. **Weekly reviews** of management effectiveness
4. **Adjust protocols** based on healing/improvement

### For Resolution:
1. **Update diagnosis status** to "resolved"
2. **Remove from active.md** daily management
3. **Archive** to data folder or medical history
4. **Maintain** body/state tracking for reference

## Agent Integration

### For AI Health Support:
- **Load active diagnoses** to understand current limitations
- **Factor into responses** when discussing activities/work
- **Provide specific support** based on diagnosis management needs
- **Monitor progress** and suggest adjustments

### Example Agent Awareness:
```
User: "I want to exercise today"
Agent: "With your finger joint injury, let's plan exercises that work around your hand limitations and include your rehabilitation protocol..."
```

## Privacy and Medical Accuracy

### Important Notes:
- **Not medical records** - these are personal tracking documents
- **Complement professional care** - do not replace medical consultation
- **Share appropriately** - consider privacy when sharing with others
- **Update regularly** - keep information current and accurate

### Medical Professional Communication:
- These files can help **prepare for appointments**
- Provide **objective progress tracking** for providers
- **Support communication** of symptoms and functional impact
- **Should not replace** professional medical documentation

## Examples of Active Diagnoses

### Physical Conditions:
- Acute injuries requiring rehabilitation
- Chronic conditions needing daily management
- Post-surgical recovery with functional limitations
- Pain conditions affecting daily activities

### Mental Health Conditions:
- Active depression or anxiety episodes
- PTSD with current symptom management
- Eating disorders requiring ongoing support
- Substance abuse in recovery

### Chronic Conditions:
- Diabetes requiring daily monitoring
- Arthritis with activity modifications
- Migraines affecting work schedules
- Autoimmune conditions with flare management

---

*This diagnosis tracking system provides focused attention on conditions that actively impact daily life while integrating with the broader health tracking ecosystem.*