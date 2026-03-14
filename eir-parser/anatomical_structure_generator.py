#!/usr/bin/env python3
"""
Anatomical Health Structure Generator - Create systematic body-based health tracking
"""

import os
from pathlib import Path
from datetime import datetime

class AnatomicalHealthGenerator:
    """Generate systematic body-based and mental health tracking structure"""
    
    def __init__(self, base_health_dir="health"):
        self.health_dir = Path(base_health_dir)
        self.body_dir = self.health_dir / "body"
        self.state_dir = self.health_dir / "state"
        
        # Anatomical structure definition
        self.body_structure = {
            "head": {
                "organs": ["brain", "eyes", "ears", "nose", "mouth", "jaw", "scalp"],
                "sides": ["left", "right"],
                "bilateral": ["eyes", "ears"]
            },
            "neck": {
                "organs": ["throat", "thyroid", "lymph-nodes", "cervical-spine"],
                "sides": [],
                "bilateral": []
            },
            "torso": {
                "areas": {
                    "chest": {
                        "organs": ["heart", "lungs", "ribs", "sternum", "thoracic-spine"],
                        "sides": ["left", "right"],
                        "bilateral": ["lungs", "ribs"]
                    },
                    "abdomen": {
                        "organs": ["stomach", "liver", "kidneys", "intestines", "pancreas", "spleen", "bladder"],
                        "sides": ["left", "right"], 
                        "bilateral": ["kidneys"]
                    }
                }
            },
            "arms": {
                "sides": ["left", "right"],
                "segments": {
                    "shoulder": ["joint", "muscles", "tendons"],
                    "upper-arm": ["humerus", "biceps", "triceps"],
                    "elbow": ["joint", "tendons"],
                    "forearm": ["radius", "ulna", "muscles"],
                    "wrist": ["joint", "tendons"],
                    "hand": {
                        "parts": ["palm", "thumb", "fingers", "knuckles"],
                        "fingers": ["index", "middle", "ring", "pinky"]
                    }
                }
            },
            "legs": {
                "sides": ["left", "right"],
                "segments": {
                    "hip": ["joint", "muscles"],
                    "upper-leg": ["femur", "quadriceps", "hamstring"],
                    "knee": ["joint", "patella", "ligaments"],
                    "lower-leg": ["tibia", "fibula", "calf", "shin"],
                    "ankle": ["joint", "tendons"],
                    "foot": {
                        "parts": ["heel", "arch", "ball", "toes"],
                        "toes": ["big-toe", "second", "third", "fourth", "fifth"]
                    }
                }
            },
            "back": {
                "regions": ["cervical", "thoracic", "lumbar", "sacral"],
                "organs": ["spine", "muscles", "nerves"]
            },
            "skin": {
                "regions": ["face", "scalp", "neck", "chest", "back", "arms", "legs"],
                "conditions": ["rashes", "moles", "scars", "lesions"]
            }
        }
        
        # Mental health and state structure
        self.state_structure = {
            "mood": ["depression", "anxiety", "irritability", "euphoria", "stability"],
            "cognitive": ["memory", "concentration", "decision-making", "processing-speed", "clarity"],
            "stress": ["work-stress", "personal-stress", "physical-stress", "financial-stress"],
            "sleep": ["quality", "duration", "patterns", "disturbances", "fatigue"],
            "energy": ["physical-energy", "mental-energy", "motivation", "stamina"],
            "social": ["relationships", "isolation", "communication", "support-system"],
            "behavioral": ["habits", "routines", "coping-mechanisms", "lifestyle"],
            "emotional": ["regulation", "expression", "processing", "stability"]
        }
    
    def generate_complete_structure(self):
        """Generate complete anatomical and mental health structure"""
        
        print("🏗️ Generating Systematic Health Tracking Structure")
        print("=" * 50)
        
        # Create main directories
        self.body_dir.mkdir(exist_ok=True)
        self.state_dir.mkdir(exist_ok=True)
        
        # Generate body structure
        self._generate_body_structure()
        
        # Generate mental health structure
        self._generate_state_structure()
        
        # Generate index files
        self._generate_body_index()
        self._generate_state_index()
        
        # Update main health.md to reference new structure
        self._update_main_health_file()
        
        print("\\n✅ Complete systematic health structure generated!")
        print("📊 Structure includes:")
        print(f"  🫀 Body: Anatomical organization by system and location")
        print(f"  🧠 Mental: Psychological and emotional state tracking")
        print(f"  📁 Empty template files ready for health data")
        
    def _generate_body_structure(self):
        """Generate anatomical body structure"""
        
        print("🫀 Generating Body Structure...")
        
        # Head structure
        self._create_head_structure()
        
        # Neck structure  
        self._create_neck_structure()
        
        # Torso structure
        self._create_torso_structure()
        
        # Arms structure
        self._create_limb_structure("arms")
        
        # Legs structure
        self._create_limb_structure("legs")
        
        # Back structure
        self._create_back_structure()
        
        # Skin structure
        self._create_skin_structure()
    
    def _create_head_structure(self):
        """Create head anatomical structure"""
        
        head_dir = self.body_dir / "head"
        head_dir.mkdir(exist_ok=True)
        
        organs = self.body_structure["head"]["organs"]
        bilateral = self.body_structure["head"]["bilateral"]
        
        for organ in organs:
            if organ in bilateral:
                # Create left/right for bilateral organs
                (head_dir / "left" / organ).mkdir(parents=True, exist_ok=True)
                (head_dir / "right" / organ).mkdir(parents=True, exist_ok=True)
                
                self._create_template_file(head_dir / "left" / organ / f"{organ}.md", f"Left {organ.title()}", "head")
                self._create_template_file(head_dir / "right" / organ / f"{organ}.md", f"Right {organ.title()}", "head")
            else:
                # Create single file for non-bilateral organs
                organ_dir = head_dir / organ
                organ_dir.mkdir(exist_ok=True)
                self._create_template_file(organ_dir / f"{organ}.md", organ.title(), "head")
    
    def _create_neck_structure(self):
        """Create neck anatomical structure"""
        
        neck_dir = self.body_dir / "neck"
        neck_dir.mkdir(exist_ok=True)
        
        organs = self.body_structure["neck"]["organs"]
        
        for organ in organs:
            organ_dir = neck_dir / organ
            organ_dir.mkdir(exist_ok=True)
            self._create_template_file(organ_dir / f"{organ}.md", organ.replace("-", " ").title(), "neck")
    
    def _create_torso_structure(self):
        """Create torso anatomical structure"""
        
        torso_dir = self.body_dir / "torso"
        torso_dir.mkdir(exist_ok=True)
        
        areas = self.body_structure["torso"]["areas"]
        
        for area_name, area_data in areas.items():
            area_dir = torso_dir / area_name
            area_dir.mkdir(exist_ok=True)
            
            for organ in area_data["organs"]:
                if organ in area_data["bilateral"]:
                    # Bilateral organs
                    (area_dir / "left" / organ).mkdir(parents=True, exist_ok=True)
                    (area_dir / "right" / organ).mkdir(parents=True, exist_ok=True)
                    
                    self._create_template_file(area_dir / "left" / organ / f"{organ}.md", f"Left {organ.title()}", f"torso/{area_name}")
                    self._create_template_file(area_dir / "right" / organ / f"{organ}.md", f"Right {organ.title()}", f"torso/{area_name}")
                else:
                    # Single organs
                    organ_dir = area_dir / organ
                    organ_dir.mkdir(exist_ok=True)
                    self._create_template_file(organ_dir / f"{organ}.md", organ.replace("-", " ").title(), f"torso/{area_name}")
    
    def _create_limb_structure(self, limb_type):
        """Create arm or leg structure"""
        
        limb_dir = self.body_dir / limb_type
        limb_dir.mkdir(exist_ok=True)
        
        limb_data = self.body_structure[limb_type]
        sides = limb_data["sides"]
        segments = limb_data["segments"]
        
        for side in sides:
            side_dir = limb_dir / side
            side_dir.mkdir(exist_ok=True)
            
            for segment_name, segment_data in segments.items():
                segment_dir = side_dir / segment_name
                segment_dir.mkdir(exist_ok=True)
                
                if isinstance(segment_data, list):
                    # Simple list of parts
                    for part in segment_data:
                        self._create_template_file(segment_dir / f"{part}.md", part.replace("-", " ").title(), f"{limb_type}/{side}/{segment_name}")
                elif isinstance(segment_data, dict):
                    # Complex structure (like hand/foot)
                    if "parts" in segment_data:
                        for part in segment_data["parts"]:
                            part_dir = segment_dir / part
                            part_dir.mkdir(exist_ok=True)
                            self._create_template_file(part_dir / f"{part}.md", part.replace("-", " ").title(), f"{limb_type}/{side}/{segment_name}")
                    
                    if "fingers" in segment_data:
                        fingers_dir = segment_dir / "fingers"
                        fingers_dir.mkdir(exist_ok=True)
                        for finger in segment_data["fingers"]:
                            self._create_template_file(fingers_dir / f"{finger}.md", finger.replace("-", " ").title(), f"{limb_type}/{side}/{segment_name}/fingers")
                    
                    if "toes" in segment_data:
                        toes_dir = segment_dir / "toes"
                        toes_dir.mkdir(exist_ok=True)
                        for toe in segment_data["toes"]:
                            self._create_template_file(toes_dir / f"{toe}.md", toe.replace("-", " ").title(), f"{limb_type}/{side}/{segment_name}/toes")
    
    def _create_back_structure(self):
        """Create back anatomical structure"""
        
        back_dir = self.body_dir / "back"
        back_dir.mkdir(exist_ok=True)
        
        regions = self.body_structure["back"]["regions"]
        organs = self.body_structure["back"]["organs"]
        
        for region in regions:
            region_dir = back_dir / region
            region_dir.mkdir(exist_ok=True)
            
            for organ in organs:
                self._create_template_file(region_dir / f"{region}-{organ}.md", f"{region.title()} {organ.title()}", f"back/{region}")
    
    def _create_skin_structure(self):
        """Create skin structure"""
        
        skin_dir = self.body_dir / "skin"
        skin_dir.mkdir(exist_ok=True)
        
        regions = self.body_structure["skin"]["regions"]
        conditions = self.body_structure["skin"]["conditions"]
        
        for region in regions:
            region_dir = skin_dir / region
            region_dir.mkdir(exist_ok=True)
            self._create_template_file(region_dir / f"{region}-skin.md", f"{region.title()} Skin", f"skin/{region}")
        
        conditions_dir = skin_dir / "conditions"
        conditions_dir.mkdir(exist_ok=True)
        
        for condition in conditions:
            self._create_template_file(conditions_dir / f"{condition}.md", condition.replace("-", " ").title(), "skin/conditions")
    
    def _generate_state_structure(self):
        """Generate mental health and state structure"""
        
        print("🧠 Generating Mental Health Structure...")
        
        for state_category, aspects in self.state_structure.items():
            category_dir = self.state_dir / state_category
            category_dir.mkdir(exist_ok=True)
            
            for aspect in aspects:
                self._create_state_template_file(category_dir / f"{aspect}.md", aspect.replace("-", " ").title(), state_category)
    
    def _create_template_file(self, file_path, title, location):
        """Create template file for body part"""
        
        content = f"""# {title}

**Location:** {location}
**Last Updated:** *Never*
**Status:** No issues documented

## Current Status

*No health issues or concerns documented for this area*

## History

*No historical health events documented*

## Notes

*Add any relevant health information, symptoms, conditions, or medical history related to {title.lower()}*

## Related Conditions

*Document any conditions affecting this area*

## Healthcare Providers

*List any specialists or providers specifically related to this area*

## Medications

*Document any medications specifically for conditions affecting this area*

---

*Template file - add relevant health information as needed*
"""
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_state_template_file(self, file_path, title, category):
        """Create template file for mental health state"""
        
        content = f"""# {title}

**Category:** {category.title()}
**Last Updated:** *Never*
**Current Status:** Not assessed

## Current State

*Document current status and recent patterns*

## Patterns & Triggers

*Identify patterns, triggers, or influencing factors*

## Coping Strategies

*Document effective coping mechanisms and strategies*

## Professional Support

*List any therapists, counselors, or mental health professionals*

## Medications

*Document any medications related to this mental health aspect*

## Timeline

*Track significant events, changes, or milestones*

## Goals

*Set and track mental health goals related to this area*

---

*Template file - add relevant mental health information as needed*
"""
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_body_index(self):
        """Generate body structure index"""
        
        content = f"""# Body Health Tracking

**Systematic anatomical health organization**
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}

## Organization System

This folder contains a systematic, anatomical approach to health tracking with dedicated files for each body area, organ, and system.

## Structure

### Head
- **Bilateral:** Eyes, Ears (left/right organization)
- **Single:** Brain, Nose, Mouth, Jaw, Scalp
- **Example:** `head/left/eyes/eyes.md`, `head/brain/brain.md`

### Neck  
- **Areas:** Throat, Thyroid, Lymph Nodes, Cervical Spine

### Torso
- **Chest:** Heart, Lungs (bilateral), Ribs (bilateral), Sternum, Thoracic Spine
- **Abdomen:** Stomach, Liver, Kidneys (bilateral), Intestines, Pancreas, Spleen, Bladder

### Arms (Left/Right)
- **Segments:** Shoulder → Upper Arm → Elbow → Forearm → Wrist → Hand
- **Hand Detail:** Palm, Thumb, Fingers (Index, Middle, Ring, Pinky)
- **Example:** `arms/left/hand/fingers/index.md`

### Legs (Left/Right)  
- **Segments:** Hip → Upper Leg → Knee → Lower Leg → Ankle → Foot
- **Foot Detail:** Heel, Arch, Ball, Toes (Big Toe, Second, Third, Fourth, Fifth)
- **Example:** `legs/right/foot/toes/big-toe.md`

### Back
- **Regions:** Cervical, Thoracic, Lumbar, Sacral
- **Components:** Spine, Muscles, Nerves

### Skin
- **Regions:** Face, Scalp, Neck, Chest, Back, Arms, Legs
- **Conditions:** Rashes, Moles, Scars, Lesions

## Usage Guidelines

### When to Use
- **Specific symptoms:** Document in exact anatomical location
- **Injuries:** Record in precise body area affected
- **Medical conditions:** Track by affected body system
- **Monitoring:** Regular health checks by body area

### File Naming
- Use anatomical accuracy: `left-shoulder.md`, not `shoulder-left.md`
- Be specific: `index-finger.md` rather than `finger.md`
- Use medical terminology when appropriate

### Cross-References
- Link related body areas when conditions affect multiple parts
- Reference main health record and timeline files
- Connect to relevant providers and medications

## Benefits

- **Precision:** Exact location tracking for symptoms and conditions
- **Organization:** Systematic approach to body health
- **Medical Communication:** Clear documentation for healthcare providers
- **Pattern Recognition:** Identify health patterns by body system

---

*This systematic approach enables precise health tracking and clear communication with healthcare providers.*
"""
        
        with open(self.body_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_state_index(self):
        """Generate mental health state index"""
        
        content = f"""# Mental Health & State Tracking

**Comprehensive psychological and emotional wellness monitoring**
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}

## Organization System

This folder provides systematic tracking of mental health states, emotional patterns, and psychological wellness across multiple dimensions.

## Structure

### Mood
- **Depression:** Symptoms, patterns, treatment
- **Anxiety:** Triggers, management, severity
- **Irritability:** Causes, frequency, impact
- **Euphoria:** Episodes, triggers, stability
- **Stability:** Overall mood regulation

### Cognitive
- **Memory:** Short-term, long-term, working memory
- **Concentration:** Focus, attention span, distractibility  
- **Decision-Making:** Process, confidence, outcomes
- **Processing Speed:** Mental agility, response time
- **Clarity:** Mental sharpness, confusion patterns

### Stress
- **Work Stress:** Job-related pressures, workload
- **Personal Stress:** Relationships, family, life events
- **Physical Stress:** Health, pain, fatigue impact
- **Financial Stress:** Economic pressures, security

### Sleep
- **Quality:** Sleep satisfaction, restfulness
- **Duration:** Sleep length, consistency
- **Patterns:** Sleep/wake schedule, regularity
- **Disturbances:** Insomnia, nightmares, interruptions
- **Fatigue:** Daytime tiredness, energy levels

### Energy
- **Physical Energy:** Stamina, vitality, exhaustion
- **Mental Energy:** Cognitive resources, mental fatigue
- **Motivation:** Drive, enthusiasm, goal pursuit
- **Stamina:** Endurance, persistence capacity

### Social
- **Relationships:** Quality, satisfaction, conflicts
- **Isolation:** Social withdrawal, loneliness
- **Communication:** Expression, listening, connection
- **Support System:** Available help, social network

### Behavioral
- **Habits:** Daily routines, health behaviors
- **Routines:** Structure, consistency, adaptation
- **Coping Mechanisms:** Stress management strategies
- **Lifestyle:** Activity patterns, self-care practices

### Emotional
- **Regulation:** Emotional control, stability
- **Expression:** Emotional communication, authenticity
- **Processing:** Working through emotions, understanding
- **Stability:** Emotional predictability, balance

## Usage Guidelines

### Regular Tracking
- **Daily:** Quick mood, energy, sleep quality checks
- **Weekly:** Comprehensive state review across categories
- **Monthly:** Pattern analysis and goal assessment
- **Quarterly:** Professional consultation and strategy review

### Documentation Tips
- **Be specific:** Note exact symptoms, triggers, contexts
- **Track patterns:** Look for recurring themes, cycles
- **Note interventions:** Record what helps or hinders
- **Monitor changes:** Document improvements or concerns

### Integration
- **Physical Health:** Connect mental state to physical symptoms
- **Life Events:** Relate states to circumstances, stressors
- **Treatment:** Track therapy, medication, intervention effects
- **Relationships:** Note social impacts and influences

## Benefits

- **Self-Awareness:** Understanding personal mental health patterns
- **Communication:** Clear information for mental health professionals
- **Progress Tracking:** Monitor improvement over time
- **Pattern Recognition:** Identify triggers and effective interventions
- **Holistic Health:** Integrate mental and physical wellness

---

*Mental health is as important as physical health - systematic tracking enables better self-care and professional treatment.*
"""
        
        with open(self.state_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _update_main_health_file(self):
        """Update main health.md to reference new structure"""
        
        main_health_file = self.health_dir / "health.md"
        
        if main_health_file.exists():
            # Read current content
            with open(main_health_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add sections for body and state tracking
            additional_content = """

## Systematic Health Tracking

### 🫀 [Body Health](./body/)
**Anatomical Organization:**
- Systematic tracking by body area, organ, and system
- Precise documentation for symptoms and conditions
- Left/right organization for bilateral body parts
- **Action:** Use for specific symptoms or conditions

### 🧠 [Mental Health & State](./state/)
**Psychological Wellness:**
- Comprehensive mental health state tracking
- Emotional patterns and behavioral monitoring
- Stress, sleep, mood, and cognitive tracking
- **Action:** Regular mental health self-assessment

"""
            
            # Insert before the "## Data Sources" section
            if "## Data Sources" in content:
                content = content.replace("## Data Sources", additional_content + "## Data Sources")
            else:
                content += additional_content
            
            # Write updated content
            with open(main_health_file, 'w', encoding='utf-8') as f:
                f.write(content)

def main():
    """Generate complete anatomical and mental health tracking structure"""
    
    generator = AnatomicalHealthGenerator()
    generator.generate_complete_structure()
    
    print("\\n🎯 Complete Health Tracking System Ready!")
    print("📁 Navigate to:")
    print("  📄 health/health.md - Main overview")
    print("  🫀 health/body/ - Anatomical health tracking")  
    print("  🧠 health/state/ - Mental health tracking")
    print("\\n💡 All template files created and ready for health data!")

if __name__ == "__main__":
    main()