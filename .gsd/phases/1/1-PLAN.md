---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Foundation & Setup

## Objective
Initialize the environment for Groq integration by installing the SDK and updating the configuration files.

## Context
- .gsd/SPEC.md
- d:\firebox\chrome Download\chatbox\requirements.txt
- d:\firebox\chrome Download\chatbox\app\config.py
- d:\firebox\chrome Download\chatbox\.env

## Tasks

<task type="auto">
  <name>Install Groq SDK</name>
  <files>d:\firebox\chrome Download\chatbox\requirements.txt</files>
  <action>
    - Remove `google-generativeai` from `requirements.txt`.
    - Add `groq` to `requirements.txt`.
    - Run `pip install -r requirements.txt`.
  </action>
  <verify>pip show groq</verify>
  <done>groq package is installed and google-generativeai is removed.</done>
</task>

<task type="auto">
  <name>Update Configuration</name>
  <files>d:\firebox\chrome Download\chatbox\app\config.py</files>
  <action>
    - Replace `GOOGLE_API_KEY: str` with `GROQ_API_KEY: str` in the `Settings` class.
    - Update `model_config` to ensure it continues to load from `.env`.
  </action>
  <verify>python -c "from app.config import settings; print(settings.GROQ_API_KEY)"</verify>
  <done>config.py is updated to use GROQ_API_KEY and successfully reads it from .env.</done>
</task>

## Success Criteria
- [ ] `groq` library is installed.
- [ ] `app/config.py` correctly validates and loads `GROQ_API_KEY`.
