# Policy-Aligned AI Support System (Case Study)

This repository contains a working prototype of a policy-aligned AI system designed to handle real-world customer support queries at scale.

The project was built as part of a Founder’s Office–style problem:
designing an AI agent that can take autonomous decisions while balancing user trust, operational cost, and platform policy constraints.

Although the case study uses a food-delivery marketplace as context, the underlying frameworks are applicable to:
- large consumer platforms,
- digital public infrastructure,
- grievance redressal systems,
- governance-facing AI applications.

---

## What This Project Demonstrates

- End-to-end AI decision-making under real constraints
- Prompt engineering beyond “chat quality” into judgment encoding
- Use of logs, metadata, and policy documents in AI reasoning
- Non-monetary resolution strategies to preserve trust
- Structured de-escalation of emotionally charged user interactions

---

## Repository Contents

- `system_prompt.py`  
  The core system prompt defining the AI’s role, tone, decision ladder, and policy alignment.

- `order_logs.py`  
  Simulated backend order metadata used by the AI to reason factually.

- `my_bot.py`  
  Core logic that ties user input, system prompt, and logs together.

- `streamlit_app.py`  
  A lightweight UI to manually test real-world support conversations.

---

## Why This Matters

Most AI demos focus on fluency.
Real systems must focus on:
- correctness,
- accountability,
- consistency,
- and cost discipline.

This project explores how those qualities can be encoded directly into AI behavior using structured prompts and decision frameworks.

---

## Disclaimer

This is a conceptual and educational project.
Company names are used only as illustrative examples.
No proprietary data or internal systems are used.
