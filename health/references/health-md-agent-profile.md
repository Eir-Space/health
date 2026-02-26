# Health.md Agent Profile (Canonical Sections)

Use this reference when reading or updating `health.md` records with the `health` skill.

## Goal

Keep health information portable across agents by storing:
- structured health facts
- active health contexts (for response adaptation)
- unconfirmed findings (for safety)
- skill attachments
- optional programs
- unanswered follow-up questions

## Canonical Agent-Facing Sections

### `## Active Health Contexts`
Store health contexts that should affect future answers immediately.

Examples:
- Pregnancy
- Type 2 Diabetes Mellitus
- Hypertension
- Breastfeeding

Recommended fields:
- `Status`
- `Type`
- `Source`
- `Confidence`
- `Last Confirmed`
- `Notes`

### `## Unconfirmed Findings`
Store inferred or uncertain findings that require confirmation.

Recommended fields:
- `Type`
- `Source`
- `Confidence`
- `Evidence`
- `Action Needed`
- `Do Not Treat As Confirmed`

### `## Skill Attachments`
Track which skills are active or suggested for this record.

Examples:
- `health`
- `pregnancy`
- `diabetes`

Recommended fields:
- `Status` (`suggested`, `active`, `disabled`)
- `Reason`
- `Added By`
- `Last Reviewed`

### `## Linked Health Files`
Index focused companion files for specific conditions or health events.

Examples:
- `pregnancy.md`
- `diabetes.md`

Recommended fields:
- `Type`
- `Skill`
- `Status` (`active`, `archived`, `planned`)
- `Reason`
- `Created`
- `Last Updated`

### `## Active Programs`
Store ongoing tracking/coaching workflows only when relevant and user-approved.

Recommended fields:
- `Status`
- `Linked Skill`
- `Inputs Requested`
- `Frequency`
- `Started`
- `Safety Notes`

### `## Information Gaps & Follow-up Questions`
Persist missing information so future agent turns can continue data collection.

Recommended fields:
- `Question`
- `Why It Matters`
- `Status` (`open`, `answered`, `deferred`)
- `Created By`
- `Created`

## Provenance Values (Recommended)

- `user_reported`
- `ehr`
- `ehr_export`
- `journal_inferred`
- `manual_entry`
- `clinician_verified`

## Confidence Values (Recommended)

- `low`
- `medium`
- `high`

## Safe Update Rules

1. Read the file before writing.
2. Update existing entries when possible instead of duplicating.
3. Store inferred findings in `Unconfirmed Findings` until confirmed.
4. Add provenance to agent-added facts.
5. Update frontmatter `last_updated` when writing changes.
6. Index focused condition/event files in `Linked Health Files` when created (for example `pregnancy.md`).
7. Ask short, high-value follow-up questions and persist them if unanswered.
