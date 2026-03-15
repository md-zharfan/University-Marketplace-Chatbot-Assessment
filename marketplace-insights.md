# Marketplace Domain Knowledge — UniMarket Support Chatbot

## Overview

This document analyses the key challenges, user needs, and domain-specific 
considerations that shaped the design of the UniMarket support chatbot. 
Understanding these factors is essential to building a chatbot that genuinely 
serves the student community rather than applying generic e-commerce patterns.

---

## 1. Common User Pain Points in Student Marketplaces

### Price Sensitivity
Students operate on tight budgets — most are looking for significant discounts 
over retail prices. This creates tension when sellers price items too high and 
buyers negotiate aggressively, sometimes to the point of harassment. The chatbot 
must be able to support sellers in asserting fair pricing while guiding buyers 
toward respectful negotiation.

### Trust Deficit Between Strangers
Unlike established platforms (Carousell, eBay), a new campus marketplace starts 
with no review history. Early users have no social proof to rely on, making 
them more vulnerable to scams. Trust-building features like university email 
verification, profile ratings, and verified student badges are critical — and 
the chatbot must reinforce these trust signals in every transaction interaction.

### Communication Friction
Many students — especially international students — may communicate in their 
first or second language. Misunderstandings around item condition, meetup time, 
or price are common and can escalate into disputes. The chatbot should encourage 
clear written confirmations before meetups and provide communication templates 
where helpful.

### No-Shows and Last-Minute Cancellations
One of the most cited frustrations on student marketplaces is arranging a meetup 
and having the other party not show up. This wastes time and erodes trust in the 
platform. The chatbot should set expectations around cancellation etiquette and 
provide a clear reporting path for repeat offenders.

### Unclear Item Condition Standards
Students listing items often use vague descriptors like "good condition" or 
"barely used" without photos or specific defect disclosures. This leads to 
disputes post-transaction. The chatbot should proactively encourage detailed 
descriptions and multiple photos when helping sellers create listings.

---

## 2. Safety and Trust Challenges Specific to Campus Communities

### Physical Proximity Risk
Unlike anonymous online marketplaces, campus transactions involve meeting someone 
who lives or studies nearby. A bad transaction experience doesn't just end online 
— the buyer and seller may run into each other again. This raises the stakes for 
disputes and makes harassment or stalking a more serious concern than on 
mainstream platforms.

### Scams Targeting New Students
Freshmen and international students unfamiliar with local norms are 
disproportionately targeted. Common scams include:
- **Advance payment scams**: Seller requests PayNow payment before meetup, 
  then disappears
- **Fake listings**: Popular items (e.g. graphing calculators, MacBooks) listed 
  at unrealistically low prices to collect deposits
- **Phishing links**: Fake "account verification" or "payment confirmation" 
  links sent via in-app messages

The chatbot must be trained to recognise these patterns and proactively warn 
users before they proceed with suspicious transactions.

### Academic Integrity Risks
A campus marketplace is uniquely vulnerable to academic dishonesty — selling 
completed assignments, past-year exam papers with answers, or project reports. 
These listings may not look obviously harmful but carry serious consequences 
for both buyer and seller. The chatbot must identify and block these proactively, 
even when framed innocuously ("selling my old notes").

### Shared Living Vulnerabilities
Students living in dorms share common spaces and personal information more 
freely than the general public. A bad actor on the platform has easier physical 
access to potential victims. The chatbot should always recommend public, 
high-traffic meetup locations (library lobby, canteen) and never suggest 
meeting in private residential areas.

---

## 3. Seasonal Patterns

Understanding seasonal demand helps the chatbot give more relevant, timely advice.

| Period | Driver | Common Items | Chatbot Implication |
|---|---|---|---|
| August / January | Semester start | Textbooks, calculators, laptops | High listing volume; emphasise photo quality and honest grading |
| October / April | Mid-terms | Study materials, stationery | Watch for academic integrity violations |
| November / May | Semester end | Furniture, appliances, kitchenware | Move-out surge; bulk listing support needed |
| May / June | Graduation | Everything — full room clearouts | Highest volume period; fast escalation paths needed |
| December | Year-end | Electronics, gifts, event tickets | Scam spike — increased vigilance on payment safety |

The chatbot should surface seasonal reminders proactively — for example, 
reminding sellers during graduation season to check prohibited items before 
bulk listing, or warning buyers in January about textbook edition scams.

---

## 4. Integration Needs with University Systems

### University Email Verification
The most critical trust layer is confirming that users are genuine students. 
Integration with university email systems (e.g. `@nus.edu.sg`, `@ntu.edu.sg`) 
ensures only enrolled students can access the platform. The chatbot should 
always direct unverified users to complete email verification before any 
transaction activity.

### Student ID Validation (Future)
A stronger trust layer would cross-reference matriculation numbers with the 
university's student registry. This prevents alumni or external parties from 
using expired student email addresses.

### Campus Directory / Building Access
Integration with campus maps and building access systems would allow the 
chatbot to recommend verified safe meetup locations — e.g. 24-hour study 
areas, security-monitored lobbies — rather than generic advice.

### Payment Systems
Local payment integration (PayNow, PayLah!) reduces friction and creates a 
paper trail for disputes. The chatbot should actively steer users toward 
traceable payment methods over cash, especially for higher-value transactions.

### Moderation & Reporting Backend
The chatbot's escalation pathways depend on a live ticketing or case management 
system. Integration with a moderation dashboard (e.g. Zendesk, custom internal 
tool) ensures flagged cases are actioned promptly rather than falling into 
an unmonitored inbox.

---

## 5. Chatbot-Specific Recommendations

Based on the above analysis, the following are the highest-priority requirements 
for the UniMarket chatbot beyond basic navigation support:

1. **Proactive scam detection** — flag suspicious transaction patterns before 
   users proceed, not after
2. **Seasonal content awareness** — surface relevant warnings and tips based 
   on time of year
3. **Multilingual friendliness** — simple, clear English that works for 
   non-native speakers; future multilingual support
4. **Fast escalation for safety** — zero tolerance for delays when physical 
   safety is at risk
5. **Academic integrity guardrails** — catch prohibited academic content even 
   when disguised as legitimate listings