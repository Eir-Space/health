# Health System Skill

**Comprehensive health tracking and rehabilitation support for agents**

## Overview

This skill provides agents with the ability to:
- Track health information using systematic anatomical organization
- Provide rehabilitation exercise guidance and reminders
- Monitor active health conditions requiring ongoing support
- Integrate physical and mental health tracking
- Coordinate healthcare information across providers

## Core Components

### Health Record Structure
```
health/
├── health.md              # Main overview and navigation
├── active.md             # Current issues requiring agent support
├── family-history.md     # Genetic risk factors and family patterns
├── medications.md        # Current and historical medications
├── providers.md          # Healthcare team and relationships
├── timeline.md           # Healthcare chronology and events
├── body/                 # Anatomical health tracking (140+ files)
├── state/                # Mental health and psychological tracking
└── data/                 # Source documents and backups
```

### Anatomical Organization
- **Systematic body tracking** by anatomical location
- **Bilateral organization** for paired organs/limbs (left/right)
- **Granular detail** down to individual fingers, toes, teeth
- **Organ system integration** across multiple body areas

### Mental Health Integration
- **Comprehensive psychological tracking** across 8 domains
- **Mood, cognitive, stress, sleep** monitoring
- **Social, behavioral, emotional** pattern tracking
- **Energy and motivation** assessment

## Agent Integration Features

### Active Health Support
**File:** `health/active.md`
- Current health issues requiring ongoing attention
- Daily exercise and rehabilitation protocols  
- Progress tracking and milestone goals
- Warning signs and escalation triggers

### Rehabilitation Guidance
**Example:** Finger injury rehabilitation
- **Phase-based exercise protocols** (healing → mobilization → strengthening)
- **Daily exercise schedules** with specific instructions
- **Progress monitoring** with objective measures
- **Professional consultation triggers**

### Conversational Context
Agents can provide contextualized responses based on:
- Active health conditions and limitations
- Current rehabilitation needs
- Family health risk factors
- Medication considerations

## Usage Patterns

### For Users
1. **Document health events** in precise anatomical locations
2. **Track active conditions** requiring ongoing support  
3. **Follow rehabilitation protocols** with agent guidance
4. **Monitor progress** with systematic tracking

### For Agents
1. **Load active health context** from `active.md`
2. **Provide daily exercise reminders** based on current needs
3. **Track progress** and adjust recommendations
4. **Escalate concerns** when warning signs appear

## Example: Finger Injury Support

### Initial Documentation
**Location:** `health/body/arms/left/hand/fingers/pinky.md`
```markdown
**Status:** ACTIVE ISSUE - Joint pain following fall
**Location:** Joint area between left pinky and ring finger
**Rehabilitation:** See finger-rehab.md for exercise protocol
```

### Active Support
**Added to:** `health/active.md`
```markdown
### Left Hand Finger Injury (HIGH PRIORITY)
**Daily Support Needed:**
- Exercise reminders: 3-4 times per day
- Progress tracking: Pain levels, range of motion
- Activity modifications: Ergonomic awareness
```

### Agent Behavior
- **Morning:** "Ready for your finger exercises? Let's start with gentle range of motion."
- **Midday:** "How's your hand feeling? Remember to take typing breaks."
- **Evening:** "Time for rehab protocol. Rate your pain level today (1-10)."

## Rehabilitation Exercise Integration

### Exercise Protocols
**Location:** `health/body/[area]/rehabilitation/`
- **Structured phases** (healing → mobilization → strengthening)
- **Specific instructions** with frequency and duration
- **Progress milestones** with objective measures
- **Warning signs** for medical consultation

### Daily Scheduling
**Morning Routine:**
- Heat therapy preparation
- Gentle range of motion exercises
- Pain level assessment

**Throughout Day:**
- Activity modification reminders
- Ergonomic positioning checks
- Break reminders for repetitive activities

**Evening Protocol:**
- Full rehabilitation exercise set
- Cold therapy if needed
- Progress documentation

## Health Risk Integration

### Family History Awareness
From `health/family-history.md`:
- **Cardiovascular disease pattern** (multiple strokes, heart attack)
- **Enhanced screening recommendations**
- **Prevention strategy guidance**

### Active Monitoring
Agents can provide:
- **Blood pressure awareness** based on family history
- **Lifestyle coaching** for cardiovascular prevention
- **Screening reminders** for enhanced surveillance

## Mental Health Support

### State Monitoring
From `health/state/` files:
- **Mood tracking** (depression, anxiety, stability)
- **Stress management** (work, personal, physical stress)
- **Sleep quality** monitoring and improvement
- **Cognitive function** tracking

### Integrated Approaches
- **Physical-mental connections** (pain affecting mood)
- **Stress impact** on physical healing
- **Sleep quality** affecting recovery

## Installation & Setup

### Prerequisites
- Agent system with file access capabilities
- Ability to read/write markdown files
- Scheduling/reminder capabilities (optional)

### Initial Setup
1. Create `health/` folder structure
2. Run anatomical structure generator
3. Document current health status in appropriate files
4. Configure `active.md` with current issues
5. Set agent to reference `active.md` for daily context

### Agent Configuration
```yaml
health_skill:
  active_health_file: "health/active.md"
  reminder_frequency: "daily"
  exercise_check_times: ["morning", "midday", "evening"]
  escalation_triggers: ["severe_pain", "no_improvement"]
```

## Medical Integration

### Provider Communication
- **Precise documentation** for medical consultations
- **Shareable files** for specific conditions
- **Progress tracking** for provider review
- **Symptom chronology** with detailed records

### Medication Coordination
- **Condition-specific medications** tracked by body area
- **Drug interaction awareness** across conditions
- **Adherence monitoring** and reminder support

## Safety Features

### Warning Sign Detection
- **Pain level monitoring** with escalation thresholds
- **Symptom progression** tracking
- **Functional decline** assessment
- **Medical consultation triggers**

### Professional Oversight
- **Complement, not replace** professional medical care
- **Clear escalation pathways** for concerning symptoms
- **Provider contact information** readily available
- **Emergency situation recognition**

## Benefits

### For Users
- **Systematic health organization** with precise tracking
- **Daily rehabilitation support** with exercise guidance
- **Progress monitoring** with objective measures
- **Comprehensive health picture** integrating all aspects

### For Agents
- **Rich health context** for appropriate responses
- **Actionable support protocols** for active conditions
- **Progress tracking** capabilities
- **Safety awareness** with escalation triggers

### For Healthcare Providers
- **Detailed documentation** of patient concerns
- **Objective progress tracking** between visits
- **Comprehensive health picture** across systems
- **Patient engagement** in rehabilitation and self-care

---

*This skill creates a comprehensive health support system enabling agents to provide appropriate, contextual health guidance while maintaining appropriate safety boundaries.*