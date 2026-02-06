# PRD — Healthcare Assistant AI (Product Requirements)

## 1) Problem
Users often don’t know what to do next when they feel unwell. Generic chatbots can hallucinate medical facts and cannot reliably provide **local, up-to-date service navigation**.

## 2) Product goal
Provide a **safe** multi-turn symptom triage conversation that:
- asks relevant follow-up questions,
- gives **urgency guidance** (self-care vs GP vs urgent vs emergency),
- grounds statements in **trusted sources** (citations),
- optionally recommends **local facilities** (Bucharest MVP data).

## 3) Target users
- Primary: students / residents who need guidance on “what to do next”
- Secondary: thesis evaluators and recruiters (portfolio demo)

## 4) Scope (MVP)
### Must-have
- Web chat UI (WhatsApp-like)
- Safety: red-flag escalation + refusal policy + disclaimers
- RAG: retrieve from curated medical corpus + show citations
- Evaluation mode: baseline vs RAG vs RAG+Safety

### Nice-to-have
- Local navigation: specialty recommendation + 2–3 facility results (Bucharest sample data)
- Conversation summary export (symptoms + next steps)

## 5) Non-goals
- Diagnosis or treatment plans
- Prescriptions/dosage instructions
- Emergency replacement (always instruct to call emergency services)

## 6) User experience requirements
- Clear “Not medical diagnosis” notice and emergency instruction (112).
- Visible **Urgency Badge** in UI.
- **Sources panel** showing retrieved citations.
- Short, calm, actionable responses; asks questions before giving guidance when uncertain.

## 7) Success criteria
- Demo works locally end-to-end (web → API → model → response).
- RAG+Safety reduces unsafe/hallucinated outputs vs baseline on evaluation set.
- UI displays urgency + citations correctly.

## 8) Out of scope for MVP (explicit)
- Accounts, login, payments
- Full doctor schedules / real-time appointment booking integration
- Live crawling/scraping
