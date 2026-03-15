# Chatbot Update Process — UniMarket Support Chatbot

## Overview

As UniMarket evolves — new features, policy changes, seasonal campaigns — the 
chatbot prompt will need to be updated regularly. This document defines the 
end-to-end process for proposing, testing, approving, deploying, and rolling 
back prompt updates safely.

---

## Guiding Principles

- **No direct edits to production** — all changes go through version control
- **Test before deploy** — every update must pass golden tests before release
- **Human approval for policy changes** — safety and guideline updates require 
  sign-off from the moderation team
- **Fast rollback** — any failed deployment can be reverted in under 5 minutes

---

## Workflow Overview
```
[1. Propose] → [2. Branch & Edit] → [3. Automated Tests] → [4. Human Review] 
     → [5. Deploy] → [6. Monitor] → [7. Rollback if needed]
```

---

## Step-by-Step Process

### Step 1 — Propose a Change
Anyone on the team can raise a prompt update via a GitHub Issue using the 
**Prompt Change Request** template. The issue must include:
- What is changing and why
- Which test categories are likely affected
- Whether it involves safety/policy content (triggers mandatory human review)

### Step 2 — Branch & Edit
The developer creates a new branch from `main`:
```
git checkout -b prompt/update-prohibited-items-v1.2
```
Changes are made to `prompt.md`. The version number in the file header 
is bumped (e.g. v1.1 → v1.2).

### Step 3 — Automated Testing (CI Pipeline)
On every pull request, a GitHub Actions workflow automatically:
1. Runs all 48 golden test cases against the updated prompt
2. Checks that ≥ 90% of cases pass
3. Checks that 100% of `should_escalate: true` cases trigger escalation
4. Checks that 0 safety guardrail failures occur
5. Posts a test summary report as a PR comment

If any check fails → PR is blocked from merging.

### Step 4 — Human Review & Approval
- Standard updates (navigation, UX copy): 1 reviewer approval required
- Policy/safety updates: moderation team lead must approve
- Emergency hotfixes: fast-track with 1 approval + post-deploy review

### Step 5 — Deploy
On merge to `main`, the deployment workflow:
1. Tags the release (e.g. `v1.2.0`)
2. Archives the previous prompt version in `/versions/`
3. Pushes the updated prompt to the chatbot platform API
4. Sends a deployment notification to the team Slack channel

### Step 6 — Monitor
After deployment, monitor for 24 hours:
- Escalation rate (sudden spike = something went wrong)
- User satisfaction signals (thumbs down, re-opens)
- Any new safety-related reports

### Step 7 — Rollback
If issues are detected, rollback is triggered immediately:
```
git revert <commit-hash>
git push origin main
```
Or manually via the deployment dashboard to restore the previous 
archived prompt version. Target rollback time: < 5 minutes.

---

## Version Naming Convention

| Format | Example | Meaning |
|---|---|---|
| `vMAJOR.MINOR.PATCH` | `v1.2.0` | Standard versioning |
| Major | `v2.0.0` | Full prompt redesign |
| Minor | `v1.2.0` | New scenario or policy added |
| Patch | `v1.1.1` | Small wording fix or typo |

All versions are stored in `/versions/prompt-v{version}.md`.

---

## Change Approval Matrix

| Change Type | Example | Approver |
|---|---|---|
| Copy/tone update | Friendlier wording | Any team member |
| New scenario added | Graduation season flow | Team lead |
| Safety/policy change | New prohibited item | Moderation team lead |
| Emergency hotfix | Remove dangerous response | Any senior + post-review |

---

## Folder Structure for Version Control
```
university-marketplace-chatbot-assessment/
├── prompt.md                  ← current live prompt
├── versions/
│   ├── prompt-v1.0.0.md       ← archived versions
│   ├── prompt-v1.1.0.md
│   └── prompt-v1.2.0.md
├── test-cases.json            ← golden tests
├── automation-concept.py      ← CI/CD automation logic
└── .github/
    └── workflows/
        └── prompt-ci.yml      ← GitHub Actions workflow
```