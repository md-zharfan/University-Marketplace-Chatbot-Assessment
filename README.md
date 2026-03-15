# University-Marketplace-Chatbot-Assessment

# UniMarket Support Chatbot — Intern Assessment
**Assessment:** Systems Engineer: EPS GenAI Chatbot  
**Submitted by:** Mohammad Zharfan Bin Mohammad Nizam

---

## Introduction

This repository contains my submission for the UniMarket Support Chatbot 
take-home assessment. The goal was to design, test, and prototype a GenAI 
chatbot for a university campus peer-to-peer marketplace — where students 
can buy, sell, and trade items within their campus community.

My approach focused on building a **production-minded prompt** with real 
safety guardrails, a **structured testing methodology** with 48 golden test 
cases, and a **CI/CD-inspired automation concept** for managing prompt updates 
over time.

---

## Repository Structure
```
university-marketplace-chatbot-assessment/
├── README.md                   ← this file
├── prompt.md                   ← system prompt
├── prompt-analysis.md          ← design decision analysis
├── test-cases.json             ← 48 golden test cases
├── testing-framework.md        ← testing methodology documentation
├── testing-result.md           ← test results from prototype evaluation
├── update-process.md           ← prompt update workflow documentation
├── automation-concept.py       ← CI/CD pipeline automation script
├── marketplace-insights.md     ← domain knowledge analysis
├── Sample-Chatbot-info.md      ← prototype URL and rationale
└── PROCESS_LOG.md              ← thinking process documentation
```

---

## How to Review Each Component

| Component | File | What to look for |
|---|---|---|
| Prompt Design | `prompt.md` | XML structure, safety guardrails, scenario logic |
| Prompt Rationale | `prompt-analysis.md` | Design decisions and tradeoffs |
| Test Cases | `test-cases.json` | 48 cases across 5 categories |
| Testing Approach | `testing-framework.md` | Evaluation methodology and scoring rubric |
| Test Results | `testing-result.md` | Per-case results with pass/fail analysis |
| Update Workflow | `update-process.md` | Version control and CI/CD process |
| Automation Code | `automation-concept.py` | Pipeline logic with comments |
| Domain Knowledge | `marketplace-insights.md` | User pain points, safety, seasonality |
| Prototype | `Sample-Chatbot-info.md` | Live chatbot URL and limitations |
| Thinking Process | `PROCESS_LOG.md` | Decision log throughout the assessment |

---

## Live Prototype

🤖 **UniMarket Assistant (CustomGPT)**  
🔗 https://chatgpt.com/g/g-69b671c84da08191884833c170acb155-unimarket-assistant

Built on OpenAI's GPT Builder — free, no login required to chat, 
publicly accessible via the link above.

---

## Assumptions Made

1. **Platform is Singapore-based** — payment references (PayNow, PayLah!), 
   legal references (Singapore law), and university email domains reflect 
   a local NTU/NUS-style context
2. **Users are verified students** — the chatbot assumes university email 
   verification is already in place as a platform prerequisite
3. **No real backend exists** — the prototype has no access to actual listings, 
   user accounts, or transaction data; all guidance is simulated
4. **Single-turn interactions** — the chatbot handles each message 
   independently; persistent memory across sessions is out of scope
5. **Moderation team exists** — escalation pathways assume a human 
   moderation team is available during operating hours
6. **English as primary language** — the prompt is English-only; 
   multilingual support is noted as a future improvement

---

## Time Breakdown

| Component | Allocated | Actual |
|---|---|---|
| Part 1 — Prompt Design | 45 min | 45 min |
| Part 2 — Golden Test Cases | 60 min | 60 min |
| Part 3 — Automation & Update Process | 20 min | 25 min |
| Part 4 — Marketplace Domain Knowledge | 15 min | 15 min |
| Part 5 — Prototype & Testing | 30 min | 35 min |
| README + PROCESS_LOG | — | 20 min |
| **Total** | **2.5–3 hrs** | **~3.5 hrs** |

---

## Next Steps (If This Were a Real Project)

1. **Automate test evaluation** — replace manual scoring with an 
   LLM-as-judge pipeline that scores responses programmatically against 
   `test-cases.json`
2. **Expand test coverage** — grow from 48 to 200+ test cases including 
   multi-turn conversation flows and language variation tests
3. **Connect a real backend** — integrate with actual listing/user APIs 
   so the chatbot can reference real data (e.g. "your listing #1234")
4. **Add multilingual support** — serve international students in Mandarin, 
   Malay, Tamil, and other common campus languages
5. **Implement real escalation pipeline** — wire escalation triggers to a 
   live ticketing system (e.g. Zendesk) instead of simulated responses
6. **Monitor production metrics** — track escalation rate, user satisfaction, 
   and topic distribution to identify prompt gaps over time
7. **Seasonal prompt updates** — schedule prompt reviews aligned to academic 
   calendar (semester start, graduation, move-out periods)

---

## Personal Reflection — Most Challenging Component

The most challenging component was **Part 2: designing the golden test cases**. 
Writing 48 meaningful test cases required thinking beyond happy-path scenarios 
and anticipating how real students would interact with the chatbot — including 
edge cases like hypothetical framings of prohibited activity, multi-intent 
messages, and ambiguous inputs like gibberish or single-word greetings.

The harder challenge was defining `success_criteria` — not just what the 
chatbot should say, but what a genuinely good response looks like in one 
sentence. This forced me to think clearly about what "correct" means for 
each scenario, which in turn made the prompt design sharper.

---

## Three Alternative Approaches Considered

### 1. Flat prompt without XML structure
A simple paragraph-style prompt without XML tags was considered for its 
simplicity. This was rejected because structured tags create clear parsing 
boundaries for the model, reducing the risk of conflating tone rules with 
safety rules. The XML approach also makes the prompt easier to maintain 
and version-control as individual sections can be updated independently.

### 2. Few-shot prompting (example-based)
Including 10–15 worked examples of ideal responses was considered to 
improve consistency. This was rejected for this prototype because few-shot 
examples significantly increase token usage on every request, adding cost 
and latency at scale. It would be more appropriate as a fine-tuning 
strategy rather than a system prompt technique.

### 3. Retrieval-Augmented Generation (RAG)
Connecting the chatbot to a live knowledge base of platform policies, 
FAQs, and listing data via RAG was considered. This was rejected for the 
prototype scope as it requires backend infrastructure (vector database, 
embedding pipeline) beyond what a free/open-source prototype can support 
within the time constraint. It remains the recommended architecture for 
a production deployment.

---

## My Experience with University Marketplaces

As a university student, I've used campus marketplaces both as a buyer 
and seller, primarily for textbooks/notes at the start of semesters and 
calculators during move-out periods. From my experience, the biggest pain points 
are trust (not knowing if a seller is genuine), no-shows at meetups, and 
item condition mismatches between listing photos and reality. In addition, 
most marketplaces are usually not as regulated, and some may take advantage 
of this by selling prohibited items. 

These personal experiences directly shaped the chatbot design. The 
emphasis on safe meetup locations, the no-show handling flow, and the 
proactive scam detection guidance. The seasonal patterns section in 
`marketplace-insights.md` also reflects real observed behaviour around 
textbook spikes and graduation clearouts.