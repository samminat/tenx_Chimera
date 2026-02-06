# Project Chimera

**Project Chimera** is a spec-driven, agentic AI system designed to build **Autonomous AI Influencers** — digital entities capable of researching trends, generating multi‑modal content, and managing engagement with minimal human intervention.

This repository follows **Spec‑Driven Development (SDD)** using a *spec‑kit* style workflow, where **intent and specifications are the source of truth**, and code is treated as an implementation detail.

---

## 🎯 Project Vision

Most AI systems fail at scale because they rely on:

* Fragile prompts
* Implicit assumptions
* Unstructured agent behavior

**Chimera** takes a different approach:

> Intent is explicit.
> Agents are constrained.
> Infrastructure enforces correctness.

The goal is not just to generate content, but to build **trustworthy, scalable, autonomous AI entities**.

---

## 🧠 Core Principles (Spec‑Kit / SDD)

This repository enforces the following rules:

1. **Specifications are the source of truth**

   * All behavior must be defined in `/specs` before implementation.

2. **Architecture precedes agents**

   * System architecture and agent patterns are defined in `/research`.

3. **No code without ratified specs**

   * Changes in `/src` are invalid unless backed by a ratified spec.

4. **Git commits are ratification events**

   * Specs are approved and frozen through explicit Git commits.

Violating these rules means the system is no longer trustworthy.

---

## 📁 Repository Structure

```
/research
  architecture_strategy.md     # High‑level system architecture
  agent_patterns.md            # Agent coordination and hierarchy

/specs
  SPEC_INDEX.md                # Spec ledger and lifecycle
  influencer_agent.srs.md      # Root system intent (authority spec)
  research_agent.contract.md   # Research agent contract
  generation_agent.contract.md # Content generation agent contract
  safety_agent.contract.md     # Safety & human‑in‑the‑loop contract

/tests
  README.md                    # Test strategy (future)

/src
  (empty until specs are ratified)
```

---

## 🤖 Agent Architecture (High Level)

Chimera uses a **Hierarchical Swarm** pattern:

* A central **Influencer Orchestrator** owns identity and intent
* Specialized agents operate in parallel (Research, Generation)
* A dedicated **Safety Agent** enforces policy and escalates to humans

Human approval exists as a **bounded safety layer**, not a crutch.

---

## 🧪 Human‑in‑the‑Loop (Safety Layer)

Humans intervene only when:

* Safety confidence is below threshold
* Content touches regulatory or brand‑sensitive domains
* An agent requests escalation

This allows Chimera to scale autonomy **without sacrificing trust**.

---

## 🛠 Development Workflow

### Spec‑First Flow

1. Write or update a spec in `/specs`
2. Commit as:

   ```
   spec: describe change
   ```
3. Ratify when ready:

   ```
   ratify: spec name v1
   ```
4. Only then begin implementation in `/src`

### Commit Prefixes

| Prefix     | Meaning                |
| ---------- | ---------------------- |
| `arch:`    | Architecture decisions |
| `pattern:` | Agent patterns         |
| `spec:`    | Spec creation or edits |
| `ratify:`  | Spec approval          |
| `impl:`    | Implementation         |
| `test:`    | Tests                  |
| `chore:`   | Maintenance            |

---

## 🚧 Project Status

* ✅ Architecture defined
* ✅ Agent patterns defined
* 🚧 Agent specs in progress
* ⏸ Implementation intentionally deferred

---

## 📚 References & Inspiration

* *The Trillion Dollar AI Code Stack* — a16z
* OpenClaw — Agent Social Networks
* MoltBook — Social Media for Bots
* Project Chimera SRS Document

---

> **Rule:** If it isn’t in a spec, it doesn’t exist.

Welcome to Project Chimera.
# Project Chimera

**Project Chimera** is a spec-driven, agentic AI system designed to build **Autonomous AI Influencers** — digital entities capable of researching trends, generating multi‑modal content, and managing engagement with minimal human intervention.

This repository follows **Spec‑Driven Development (SDD)** using a *spec‑kit* style workflow, where **intent and specifications are the source of truth**, and code is treated as an implementation detail.

---

## 🎯 Project Vision

Most AI systems fail at scale because they rely on:

* Fragile prompts
* Implicit assumptions
* Unstructured agent behavior

**Chimera** takes a different approach:

> Intent is explicit.
> Agents are constrained.
> Infrastructure enforces correctness.

The goal is not just to generate content, but to build **trustworthy, scalable, autonomous AI entities**.

---

## 🧠 Core Principles (Spec‑Kit / SDD)

This repository enforces the following rules:

1. **Specifications are the source of truth**

   * All behavior must be defined in `/specs` before implementation.

2. **Architecture precedes agents**

   * System architecture and agent patterns are defined in `/research`.

3. **No code without ratified specs**

   * Changes in `/src` are invalid unless backed by a ratified spec.

4. **Git commits are ratification events**

   * Specs are approved and frozen through explicit Git commits.

Violating these rules means the system is no longer trustworthy.

---

## 📁 Repository Structure

```
/research
  architecture_strategy.md     # High‑level system architecture
  agent_patterns.md            # Agent coordination and hierarchy

/specs
  SPEC_INDEX.md                # Spec ledger and lifecycle
  influencer_agent.srs.md      # Root system intent (authority spec)
  research_agent.contract.md   # Research agent contract
  generation_agent.contract.md # Content generation agent contract
  safety_agent.contract.md     # Safety & human‑in‑the‑loop contract

/tests
  README.md                    # Test strategy (future)

/src
  (empty until specs are ratified)
```

---

## 🤖 Agent Architecture (High Level)

Chimera uses a **Hierarchical Swarm** pattern:

* A central **Influencer Orchestrator** owns identity and intent
* Specialized agents operate in parallel (Research, Generation)
* A dedicated **Safety Agent** enforces policy and escalates to humans

Human approval exists as a **bounded safety layer**, not a crutch.

---

## 🧪 Human‑in‑the‑Loop (Safety Layer)

Humans intervene only when:

* Safety confidence is below threshold
* Content touches regulatory or brand‑sensitive domains
* An agent requests escalation

This allows Chimera to scale autonomy **without sacrificing trust**.

---

## 🛠 Development Workflow

### Spec‑First Flow

1. Write or update a spec in `/specs`
2. Commit as:

   ```
   spec: describe change
   ```
3. Ratify when ready:

   ```
   ratify: spec name v1
   ```
4. Only then begin implementation in `/src`

### Commit Prefixes

| Prefix     | Meaning                |
| ---------- | ---------------------- |
| `arch:`    | Architecture decisions |
| `pattern:` | Agent patterns         |
| `spec:`    | Spec creation or edits |
| `ratify:`  | Spec approval          |
| `impl:`    | Implementation         |
| `test:`    | Tests                  |
| `chore:`   | Maintenance            |

---

## 🚧 Project Status

* ✅ Architecture defined
* ✅ Agent patterns defined
* 🚧 Agent specs in progress
* ⏸ Implementation intentionally deferred

---

## 📚 References & Inspiration

* *The Trillion Dollar AI Code Stack* — a16z
* OpenClaw — Agent Social Networks
* MoltBook — Social Media for Bots
* Project Chimera SRS Document

---

> **Rule:** If it isn’t in a spec, it doesn’t exist.

Welcome to Project Chimera.
