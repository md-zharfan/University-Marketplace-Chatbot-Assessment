# Sample Chatbot — UniMarket Assistant

## Access URL
https://chatgpt.com/g/g-69b671c84da08191884833c170acb155-unimarket-assistant

---

## Platform Selected: ChatGPT CustomGPT (GPT Builder)

### Rationale
ChatGPT's GPT Builder was selected for the following reasons:

1. **Free to use** — no API costs or paid tier required for basic deployment
2. **Shareable public URL** — generates a stable link accessible to anyone 
   without a login, meeting the submission requirement
3. **Direct prompt injection** — the system prompt from `prompt.md` can be 
   pasted directly into the Instructions field with no reformatting needed
4. **No infrastructure setup** — no server, hosting, or coding required, 
   allowing focus on prompt quality over deployment complexity
5. **Built on GPT-5.2** — sufficiently capable model to test nuanced scenarios 
   including safety guardrails and escalation logic
   
---

## Testing Performed

A representative sample of 14 test cases was manually evaluated against the 
deployed prototype, covering all 5 categories from `test-cases.json`. 
Full results are documented in `testing-result.md`.

| Category | Cases Tested | ✅ Pass | ⚠️ Partial | ❌ Fail |
|---|---|---|---|---|
| Basic Navigation | 3 | 3 | 0 | 0 |
| Transaction Support | 3 | 3 | 0 | 0 |
| Safety & Guidelines | 3 | 3 | 0 | 0 |
| Escalation Triggers | 2 | 2 | 0 | 0 |
| Edge Cases | 3 | 1 | 2 | 0 |
| **Total** | **14** | **12** | **2** | **0** |

**Overall: 86% pass rate (12/14)**  
**Escalation accuracy: 100%**  
**Safety guardrail failures: 0**

Key findings:
- All safety and escalation cases passed without exception
- 2 partial passes in edge cases (greeting handling, borderline item clarity)
- Recommended prompt fixes documented in `testing-result.md`

---

## Assumptions

- Users are accessing the chatbot via a modern web browser
- The platform (ChatGPT) has access to GPT-4o as the underlying model
- University-specific details (email domain, emergency contacts) use 
  placeholder values and would be updated for real deployment
- The chatbot operates in a single-turn context — it has no memory of 
  previous conversations with the same user across sessions

---

## Limitations

1. **No real backend integration** — the chatbot cannot access actual listings, 
   user accounts, or transaction data; all guidance is generic
2. **No real escalation pathway** — escalation responses are simulated; in 
   production these would trigger a real ticketing system
3. **Model non-determinism** — responses may vary slightly between sessions 
   even for identical inputs
4. **CustomGPT context window** — very long conversations may cause the model 
   to lose earlier context
5. **Platform dependency** — the prototype depends on OpenAI's infrastructure; 
   any outage affects availability
6. **No multilingual support** — current prompt is English-only; international 
   students may need additional language support in future