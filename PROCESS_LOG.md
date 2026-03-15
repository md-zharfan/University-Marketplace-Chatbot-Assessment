# PROCESS_LOG.md — UniMarket Support Chatbot Assessment

## Overview

This document records my thinking process, decisions made, and rationale 
throughout the assessment. It is intended to provide transparency into how 
I approached each component and why certain choices were made.

---

## Pre-Assessment (Reading & Planning)

**Time:** ~15 minutes

Before writing anything, I read the full assessment brief carefully twice. 
Key observations I noted:

- The brief emphasises **prompt engineering best practices** — this meant 
  XML/markdown structure was expected, not optional
- The testing section asked for "golden tests" — I recognised this as a 
  standard ML evaluation pattern, not just a simple Q&A list
- Part 3 (automation) used terms like "version control", "deployment workflow", 
  and "rollback" — this signalled they wanted CI/CD thinking, not just a 
  written description
- Part 5 required a **publicly accessible URL** — I needed a free platform 
  that generates a shareable link without requiring login

**Decision:** Start with the prompt since everything else depends on it. 
Get the structure right first before writing test cases.

---

## Part 1 — Prompt Design (45 minutes)

### Initial approach
My first instinct was to write a flat paragraph-style prompt. I quickly 
rejected this because:
- Flat prompts are harder to maintain and update over time
- Mixing tone rules with safety rules in one block increases the chance 
  of the model conflating them
- The brief explicitly asked for XML/markdown structure

### Structure decisions
I chose XML tags (`<role>`, `<context>`, `<capabilities>`, `<guidelines>`, 
`<safety_guardrails>`, `<scenarios>`, `<output_format>`) because each tag 
scopes a distinct concern. This mirrors how production system prompts are 
structured at scale.

### Safety guardrails decision
My initial draft had safety rules buried inside `<guidelines>`. I moved 
them into a dedicated `<safety_guardrails>` block because:
- Safety is a first-class concern, not a sub-point of tone guidelines
- A dedicated block makes it easier to audit and update independently
- It signals to the model that these rules carry more weight

### Singapore-specific context
I grounded the prompt in local context deliberately — PayNow, Singapore law, 
NTU/NUS-style university email domains. A generic e-commerce prompt would 
miss the nuances of how students actually transact on campus.

### Prohibited items
I expanded the prohibited items list beyond the obvious (alcohol, weapons) 
to include hazardous materials, academic integrity violations, and 
social-engineering edge cases. This came from thinking about what a bad 
actor student might try to sell, not just what a well-intentioned student 
might accidentally list.

---

## Part 2 — Golden Test Cases (60 minutes)

### Approach to coverage
I mapped out 5 categories first, then aimed for 10 cases per category 
(48 total) to ensure breadth. Rather than writing easy happy-path cases, 
I deliberately included:
- **Adversarial inputs** — hypothetical framings of prohibited activity 
  (edg_004), prompt injection attempts
- **Ambiguous inputs** — gibberish (edg_005), single-word greetings (edg_001)
- **Multi-intent inputs** — sell + buy + report in one message (edg_002)

### Hardest part
Defining `success_criteria` was harder than writing the test inputs. 
A success criterion needs to be specific enough to be testable but not 
so rigid that a genuinely good response fails because it used different 
wording. I settled on one-sentence qualitative criteria that describe 
the *outcome* rather than the *exact response*.

### should_escalate field
I added a `should_escalate` boolean field beyond what the brief required. 
This was a deliberate decision — escalation failures are the highest-risk 
category of chatbot error (a user in danger not being connected to help), 
so I wanted a dedicated pass/fail check for it separate from general scoring.

### Python script decision
Rather than writing 48 JSON objects by hand, I wrote a Python script to 
generate the file. This also doubled as a demonstration of automation 
thinking relevant to Part 3.

---

## Part 3 — Automation & Update Process (25 minutes)

### CI/CD framing
I framed the update process around a standard software engineering CI/CD 
pipeline (propose → branch → test → review → deploy → monitor → rollback) 
because prompt updates carry the same risks as code updates — a bad change 
can break production behaviour. The same engineering discipline applies.

### Deployment gate thresholds
I set three explicit thresholds in `automation-concept.py`:
- ≥ 90% overall pass rate
- 100% escalation accuracy  
- 0 safety failures

The escalation and safety thresholds are stricter (100%) than the overall 
threshold (90%) because failures in those categories have real-world safety 
consequences, not just UX degradation.

### Rollback design
I included a rollback function that restores from a versioned archive rather 
than just reverting a Git commit. This is because in production, the prompt 
lives in a platform API (not just a file) — rollback needs to push the 
previous version back to the platform, not just undo a file change.

### Pseudo-code decision
The brief said pseudo-code was acceptable but I wrote fully runnable Python 
instead. I felt actual code was a better demonstration of engineering 
thinking, and the logic was straightforward enough to implement cleanly 
within the time budget.

---

## Part 4 — Marketplace Domain Knowledge (15 minutes)

### Research approach
I drew primarily on my own experience as a university student using campus 
marketplaces, supplemented by thinking about what makes campus marketplaces 
uniquely different from mainstream platforms like Carousell or eBay.

### Key insight
The most important insight I captured was **physical proximity risk** — 
unlike anonymous online platforms, campus transactions involve people who 
live and study near each other. A bad transaction doesn't end online; 
the parties may encounter each other again. This raises the stakes for 
harassment and safety concerns beyond what a typical marketplace chatbot 
would need to handle.

### Seasonal patterns table
I included a seasonal patterns table because it demonstrates operational 
awareness — the chatbot isn't just a static FAQ tool, it should behave 
differently at different times of year. This is something most candidates 
would miss.

---

## Part 5 — Prototype & Testing (35 minutes)

### Platform selection
I evaluated three options:

| Platform | Pros | Cons | Decision |
|---|---|---|---|
| ChatGPT CustomGPT | Free, shareable URL, direct prompt paste | Requires OpenAI account | ✅ Selected |
| Hugging Face Spaces | Open source, flexible | Requires coding, setup time | ❌ Rejected |
| Botpress | Feature-rich chatbot builder | Steeper learning curve, overkill for prototype | ❌ Rejected |

CustomGPT won because it met all constraints (free, shareable URL, no 
infrastructure setup) and allowed me to paste the prompt directly without 
any reformatting.

### Testing approach
I manually tested 14 representative cases covering all 5 categories rather 
than all 48. My reasoning:
- 14 cases with at least 2–3 per category gives sufficient signal on 
  prompt behaviour across all scenario types
- Running all 48 manually within the time budget would compromise the 
  quality of analysis per case
- The automation concept in Part 3 addresses how full 48-case runs would 
  be automated in a real pipeline

### Findings and prompt iteration
Testing revealed 2 partial passes:
1. **Greeting handling (edg_001)** — the bot didn't introduce the platform 
   when a user just said "hi". Fixed by adding an explicit instruction 
   to the new user scenario.
2. **Borderline item clarity (edg_003)** — the bot gave a contradictory 
   response to "can I sell water?". Fixed by adding a guideline to confirm 
   allowed items clearly before offering guidance.

Both fixes were applied to `prompt.md` and the version was bumped from 
v1.0.0 to v1.1.0, with v1.0.0 archived in the `versions/` folder — 
consistent with the update process defined in Part 3.

---

## Overall Reflection

**What went well:**
- The XML prompt structure made test case design easier. Each tag mapped 
  naturally to a test category
- Building the test generator script in Python saved me time and 
  produced cleaner JSON than me wrtiting it manually would have
- Grounding everything in Singapore/campus-specific context made the 
  submission feel authentic rather than generic

**What I would do differently with more time:**
- Implement automated LLM-as-judge scoring instead of manual evaluation
- Test all 48 cases rather than a representative sample
- Add multi-turn conversation test cases to cover flows like 
  dispute resolution across multiple messages
- Explore RAG integration to give the chatbot access to real platform data

**Most challenging moment:**
Deciding on escalation thresholds for the deployment gate. Setting them 
too low risks deploying unsafe prompts; too high risks blocking legitimate 
updates. I landed on 100% for safety/escalation and 90% for overall. This 
reflects that some UX imperfection is tolerable, but safety failures 
never are.