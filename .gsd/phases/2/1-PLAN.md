---
phase: 2
plan: 1
wave: 1
---

# Plan 2.1: Agent Migration

## Objective
Migrate the AI Agent logic in `app/ai_agent.py` from Google Gemini to Groq Cloud using the `llama-3.1-8b-instant` model.

## Context
- .gsd/SPEC.md
- d:\firebox\chrome Download\chatbox\app\ai_agent.py
- d:\firebox\chrome Download\chatbox\app\config.py

## Tasks

<task type="auto">
  <name>Refactor AI Agent Implementation</name>
  <files>d:\firebox\chrome Download\chatbox\app\ai_agent.py</files>
  <action>
    - Replace `google.generativeai` with `groq`.
    - Initialize `Groq` client using `settings.GROQ_API_KEY`.
    - Update `get_response` method:
        - Use `client.chat.completions.create`.
        - Pass the system instruction from `settings.SYSTEM_PROMPT`.
        - Implement message history/session handling compatible with Chat Completions API.
        - Handle Groq specific response structure and errors.
  </action>
  <verify>python -m app.ai_agent (if it has a main block) or run a test script</verify>
  <done>AIAgent class uses Groq SDK and returns responses from llama-3.1-8b-instant.</done>
</task>

<task type="auto">
  <name>Add Smoke Test for Groq</name>
  <files>d:\firebox\chrome Download\chatbox\tests\test_groq.py</files>
  <action>
    - Create a minimal test script that initializes `AIAgent` and tries to get a response.
    - Ensure it prints the response to verify connectivity.
  </action>
  <verify>python tests/test_groq.py</verify>
  <done>Test script successfully demonstrates AIAgent working with Groq.</done>
</task>

## Success Criteria
- [ ] `app/ai_agent.py` is fully migrated to Groq.
- [ ] AI agent maintains the hospital persona.
- [ ] Chat sessions continue to work (basic history support).
