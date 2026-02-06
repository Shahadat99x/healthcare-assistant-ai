# THESIS_PLAN — Research Plan

## 1) Thesis statement
Build and evaluate a medical dialogue assistant that improves safety and factual grounding using RAG and explicit safety policies.

## 2) Research questions
1) Does RAG improve factuality and reduce hallucinations?
2) Do explicit safety guardrails reduce unsafe outputs and improve escalation accuracy?
3) (Optional) Does local navigation data improve task success for finding appropriate care options?

## 3) Methodology
- Implement baseline local LLM dialogue
- Add RAG over curated corpus (citations)
- Add safety policy engine
- Evaluate variants on fixed test set

## 4) Thesis outline (draft)
1. Introduction & motivation
2. Related work (dialogue systems, medical LLM risks, RAG)
3. System design (architecture, safety policy, corpus)
4. Experimental setup (dataset/prompts, rubric)
5. Results & discussion
6. Limitations, ethics, future work

## 5) Deliverables for defense
- working demo (web + API)
- evaluation results table + analysis
- architecture diagram + safety policy summary
