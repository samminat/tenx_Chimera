# Project Chimera: The Agentic Infrastructure Challenge

Source Code Overview - AI Influencer Agent System

**Version:** 1.0  
**Date:** 2026-02-05  
**Author:** Samson Solomon  

---

## 1. Overview
This `/src` folder contains the **implementation code** for the AI Influencer Agent System.  

> ⚠️ **Important:** No implementation should occur until all **SRS and contract files** in `/specs` are ratified.  
> This enforces Spec-Driven Development (SDD) discipline.

---

## 2. Folder Structure in `/src`

/src
/agents
influencer_agent/ # Implementation of Influencer Agent
research_agent/ # Implementation of Research Agent
generation_agent/ # Implementation of Generation Agent
safety_agent/ # Implementation of Safety Agent
supervisor_agent/ # Implementation of Supervisor Agent
/common # Shared utilities, helpers, data models
/config # Configuration files (YAML, JSON)


---

## 3. Implementation Notes
- Code should strictly adhere to **ratified SRS and contracts**.  
- Each agent should implement **its defined responsibilities, inputs/outputs, and failure behavior**.  
- Testing hooks should reference **acceptance tests** in `/tests`.  
- All external API calls should be configurable via `/config` and mockable for testing.  
- Logging and auditing must comply with **Safety Agent requirements**.

---

## 4. Skills / Requirements
To work in `/src`, developers should be familiar with:

### 4.1 Programming
- Python 3.11 or Node.js (depending on chosen runtime)  
- Object-Oriented and modular design  
- API integration and data parsing  

### 4.2 AI / Agent Design
- Multi-agent system patterns  
- State machines and task orchestration  
- Contract-driven development  

### 4.3 Tools
- Git for version control  
- CI/CD pipelines (GitHub Actions / GitLab)  
- Mocking and unit test frameworks  

### 4.4 Security & Compliance
- Secure API handling (keys, tokens, HTTPS)  
- GDPR and privacy compliance  
- Logging and audit trails  

---

## 5. Developer Guidance
- Always **consult `/specs` before writing code**.  
- Implement **one agent at a time** and verify against its **acceptance tests**.  
- All shared utilities go into `/common` for reusability.  
- Configuration should always be externalized in `/config` and never hard-coded.  

---

**End of Document**
