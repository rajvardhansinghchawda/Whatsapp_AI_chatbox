---
phase: 3
plan: 1
wave: 1
---

# Plan 3.1: Verification & Polish

## Objective
Verify the end-to-end integration from WhatsApp webhook to Groq and back, and refine error handling for a production-ready feel.

## Context
- d:\firebox\chrome Download\chatbox\app\main.py
- d:\firebox\chrome Download\chatbox\app\webhook.py
- d:\firebox\chrome Download\chatbox\app\ai_agent.py
- .gsd/SPEC.md

## Tasks

<task type="auto">
  <name>Simulated End-to-End Test</name>
  <files>d:\firebox\chrome Download\chatbox\tests\test_e2e_sim.py</files>
  <action>
    - Create a test script that mocks the WhatsApp webhook payload.
    - Call the webhook logic (or use FastAPI's `TestClient`) to ensure the flow works: WhatsApp → Webhook → AI Agent (Groq) → Response.
    - Since I can't mock actual WhatsApp outgoing, I'll verify the internal call to the WhatsApp client is made.
  </action>
  <verify>python tests/test_e2e_sim.py</verify>
  <done>E2E simulation confirms that incoming messages trigger Groq and attempt to send a response.</done>
</task>

<task type="auto">
  <name>Refine Error Handling & Persona</name>
  <files>d:\firebox\chrome Download\chatbox\app\ai_agent.py</files>
  <action>
    - Ensure empty or invalid messages don't crash the agent.
    - Add explicit handling for "context length exceeded" with a clear cleanup strategy (already have a basic one, but can be more robust).
    - Double check that the persona doesn't bleed out (e.g., AI mentioning it's "Meta Llama").
  </action>
  <verify>python tests/test_groq.py</verify>
  <done>Agent handles edge cases gracefully and stays in persona.</done>
</task>

## Success Criteria
- [ ] E2E flow is verified via simulation.
- [ ] No regressions in hospital persona.
- [ ] Rate limits and context window issues are handled without crashing the app.
