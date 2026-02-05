# Agent Patterns

## Purpose of This Document

This document defines the **agentic patterns** used in Project Chimera and explains **why agent patterns are required after architecture but before implementation**.

In Spec-Driven Development (SDD), agent patterns serve as the *behavioral blueprint* for autonomous systems. They bridge the gap between **high-level architecture** and **low-level agent contracts**.

Without explicit agent patterns:
- Agents become prompt-bound and brittle
- Responsibilities overlap or drift
- Scaling introduces hallucinations and unsafe behavior

Agent patterns make autonomy **intentional, auditable, and scalable**.

---

## Why Agent Patterns Come After Architecture

The sequence matters:

1. **Architecture Strategy** answers *"What are we building and why?"*
2. **Agent Patterns** answer *"How do autonomous entities cooperate safely?"*
3. **Agent Contracts** answer *"What is each agent allowed to do?"*
4. **Implementation** answers *"How do we execute the plan?"*

Agent patterns cannot be defined before architecture because:
- They depend on system boundaries (data, safety, deployment)
- They inherit non-functional requirements (scale, reliability, trust)
- They encode workflow topology (hierarchy, sequencing, escalation)

Conversely, writing agent contracts without patterns leads to **isolated agents** that cannot coordinate coherently.

---

## Selected Primary Pattern: Hierarchical Swarm

### Pattern Description

The **Hierarchical Swarm** pattern combines:
- Central orchestration (control, safety, intent)
- Specialized autonomous agents (research, generation, engagement)
- Escalation paths instead of peer chaos

This pattern mirrors real-world organizations and modern distributed systems.

### Why It Fits Project Chimera

Project Chimera aims to create **Autonomous AI Influencers**, which require:
- Consistent persona and intent
- Parallel content research and generation
- Strong safety and brand alignment

A flat swarm would:
- Drift in tone and goals
- Be difficult to audit
- Increase hallucination risk

A strict sequential chain would:
- Bottleneck creativity
- Reduce responsiveness to trends

Hierarchical Swarm balances **speed, creativity, and control**.

---

## Core Agent Roles in the Pattern

### 1. Influencer Orchestrator Agent (Root)

**Responsibilities:**
- Owns influencer identity and long-term goals
- Dispatches tasks to child agents
- Aggregates outputs
- Enforces workflow order

**Authority Level:** Highest

---

### 2. Research Agent (Specialist)

**Responsibilities:**
- Trend discovery
- Topic ideation
- Audience signal analysis

**Constraints:**
- Cannot generate publishable content
- Read-only access to historical data

---

### 3. Generation Agent (Specialist)

**Responsibilities:**
- Content drafting (text, image, video prompts)
- Style adherence
- Platform-specific formatting

**Constraints:**
- Cannot self-publish
- Must attach reasoning metadata

---

### 4. Safety Agent (Gatekeeper)

**Responsibilities:**
- Policy enforcement
- Brand safety
- Regulatory compliance
- Human escalation

**Constraints:**
- No creative authority
- Final approval gate

---

### 5. Engagement Agent (Optional – Phase 2)

**Responsibilities:**
- Comment analysis
- Reply drafting
- Sentiment tracking

**Constraints:**
- Cannot initiate posts
- Operates only on approved content

---

## Supporting Pattern: Human-in-the-Loop Safety Layer

### Pattern Description

Autonomy is **bounded**, not absolute.

The Human-in-the-Loop (HITL) pattern inserts a **manual approval checkpoint** when:
- Safety confidence is below threshold
- Content is controversial or ambiguous
- Platform or regulatory risk is detected

### Why This Pattern Is Mandatory

Pure autonomy fails in:
- Brand-sensitive environments
- Legal gray zones
- Early-stage systems

HITL ensures:
- Accountability
- Trust calibration
- Gradual autonomy expansion

---

## Anti-Patterns Explicitly Avoided

### ❌ Prompt-Only Agents
- No memory
- No contracts
- No accountability

### ❌ Fully Flat Swarms
- No authority
- High coordination cost
- Emergent failure modes

### ❌ Monolithic "God Agents"
- Impossible to test
- Unsafe
- Non-scalable

---

## Pattern-to-Contract Mapping (Next Step)

| Pattern Element | Contract File |
|----------------|---------------|
| Orchestrator | influencer_agent.srs.md |
| Research Agent | research_agent.contract.md |
| Generation Agent | generation_agent.contract.md |
| Safety Gate | safety_agent.contract.md |

---

## Ratification Checklist

This document is considered **ratified** when:
- [ ] Agent hierarchy is agreed
- [ ] Authority boundaries are accepted
- [ ] Safety gate is mandatory
- [ ] Anti-patterns are acknowledged

Once ratified, **agent contracts may be authored**.

---

> Rule: No agent implementation may begin until this document is ratified.
