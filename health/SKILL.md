---
name: health
description: Manage longitudinal health information in a `health.md` file. Use when a user wants to store, review, or update personal health information (symptoms, diagnoses, pregnancy status, diabetes, medications, labs, allergies, vitals, care plans), when parsing EHR/journal details into structured health context, when asking follow-up health questions to fill missing information, or when attaching condition skills (for example `pregnancy` or `diabetes`) based on the user's active health contexts.
---

# Health

## Overview

Use this skill as the base health-record workflow for agents. Read and update `health.md`, ask targeted follow-up questions, preserve provenance/confidence, and keep health context portable across agents via simple skill names like `health`, `pregnancy`, and `diabetes`.

## Core Workflow

Follow these steps in order unless the user asks for a narrower action.

### 1. Find or Create `health.md`

- Look for an existing `*.health.md` file first.
- If none exists, create `health.md` (or a user-requested filename) using the Health.md format.
- If multiple files exist, ask which file to update before writing.

### 2. Read Before Writing

- Parse the current record before adding new information.
- Prefer updating existing sections over duplicating entries.
- Preserve user-entered wording in notes, while normalizing key facts into structured bullets.

### 3. Add New Information Safely

- Write confirmed information into the appropriate clinical section and `Active Health Contexts` when it should affect future responses.
- Store inferred or uncertain findings in `Unconfirmed Findings`.
- Add provenance for agent-added facts (`user_reported`, `ehr_export`, `journal_inferred`, `clinician_verified`, etc.).
- Add confidence (`low`, `medium`, `high`) when relevant.
- Update `last_updated` in YAML frontmatter whenever the file changes.

### 4. Ask Follow-up Questions

- Ask short, high-value questions only when needed to improve safety or usefulness.
- Persist unanswered questions under `Information Gaps & Follow-up Questions`.
- Mark questions `answered` or remove/close them when resolved.
- Prioritize clarification for:
  - pregnancy status
  - medication changes
  - severe symptoms / red flags
  - new diagnoses
  - allergies

### 5. Attach Relevant Skills

- Ensure `health` is listed in `Skill Attachments` as active.
- If an active context exists (for example pregnancy or diabetes), add or suggest condition skills:
  - `pregnancy`
  - `diabetes`
- Use a discovery skill (for example `health-skill-finder`) when available to find additional relevant skills.

### 6. Offer Programs Only When Useful

- Use `Active Programs` only for ongoing workflows (for example glucose tracking).
- Do not activate intensive tracking without user agreement.
- Record requested inputs, frequency, and safety notes.

## Writing Rules for `health.md`

### Confirmed vs Unconfirmed

- Do not silently promote inferred diagnoses/conditions to confirmed facts.
- Example: A journal mention of pregnancy stays in `Unconfirmed Findings` until user confirmation or clinician verification.
- After confirmation, move the item to `Active Health Contexts` and update `Skill Attachments` accordingly.

### Health Contexts (Not Just Diagnoses)

Treat contexts like these as first-class modifiers for future health answers:
- pregnancy
- breastfeeding
- diabetes
- hypertension
- immunocompromised status

Store them in `Active Health Contexts` when they are active and relevant.

### Minimal Questions Strategy

- Prefer 1-3 clarifying questions per turn.
- Ask the question with the highest safety impact first.
- If the user declines, proceed with cautious, explicitly limited guidance.

## Interaction Patterns

### When User Says "I'm pregnant"

1. Add `Pregnancy` to `Active Health Contexts` with `Source: user_reported`
2. Add `pregnancy` to `Skill Attachments` (`Suggested` or `Active`)
3. Ask only essential follow-up questions (for example gestational age, urgent symptoms) if needed
4. Adapt future health answers to pregnancy-safe framing

### When User Uploads EHR or Journal Content

1. Extract facts into standard sections (medications, labs, history, timeline)
2. Mark source (`ehr_export`, `journal_inferred`, etc.)
3. Place uncertain findings in `Unconfirmed Findings`
4. Add follow-up questions for missing or ambiguous high-impact details
5. Attach condition skills based on confirmed active contexts

### When User Asks General Health Questions

- Use `Active Health Contexts` and current medications to adapt the response.
- Mention uncertainty when the record is incomplete.
- Suggest what information to add to `health.md` if it would materially improve guidance.

## Safety Boundaries

- Do not present the skill as a substitute for medical care.
- Escalate urgent symptoms to emergency/urgent care guidance instead of routine self-management.
- Confirm high-impact facts (pregnancy, medication changes, acute diagnoses, severe allergies) before treating them as confirmed.
- Keep advice conservative when context is incomplete.

## References

- Read `references/health-md-agent-profile.md` for canonical section names, provenance values, and update patterns.
