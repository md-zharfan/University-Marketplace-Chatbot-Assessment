# Prompt Analysis

## Design Decisions

The prompt is structured using XML-style tags (`<role>`, `<context>`, `<capabilities>`, 
`<guidelines>`, `<safety_guardrails>`, `<scenarios>`, `<output_format>`) to create 
clearly separated, parseable sections. This mirrors how modern LLMs process layered 
instructions — each tag scopes a distinct concern, reducing the chance of the model 
conflating tone rules with capability limits or safety rules. The `<capabilities>` 
block explicitly states what the chatbot cannot do (access real accounts, process 
refunds, make binding dispute decisions), which reduces hallucination risk and sets 
honest expectations for users.

## Safety & Guardrail Design

A dedicated `<safety_guardrails>` section was added as a first-class component rather 
than burying safety rules within general guidelines. This covers four distinct 
prohibited item categories — alcohol/substances, weapons, hazardous materials, and 
illegal goods — each with tailored example responses. Critically, the "Hard Limits" 
subsection addresses prompt injection and social engineering attempts (e.g. roleplay 
framing, "just curious" deflections), which are realistic attack vectors on a 
student-facing chatbot. Escalation triggers are explicit and threshold-based 
(e.g. disputes above $200 SGD, any mention of weapons or drugs) to minimise 
ambiguity for the model and ensure human oversight for high-stakes situations.

## University & Singapore-Specific Context

The prompt is grounded in real student behaviour rather than generic e-commerce 
patterns. Context includes Singapore-specific payment methods (PayNow), local legal 
references (Singapore law), campus meetup norms (dorm lobbies, canteens), and 
academic calendar seasonality (textbook spikes, move-out periods). The scenario 
system handles four distinct user personas — new users, buyers, sellers, and users 
in dispute — with tailored response strategies for each. This prevents the chatbot 
from applying a one-size-fits-all response to very different situations, improving 
both accuracy and user experience.