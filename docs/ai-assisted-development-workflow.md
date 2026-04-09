# AI-Assisted Development Workflow

This document describes the structured methodology I apply when working with AI coding agents in day-to-day software engineering. These practices were developed through hands-on experience and are designed to maximize reliability, maintainability, and developer understanding - while treating the AI as a high-leverage tool rather than an autonomous decision-maker.

---

## 1. Test-Driven Development (TDD) - Tests First, Always

Every feature begins with tests, not implementation.

The agent is instructed to derive test cases from the expected **inputs and outputs** of the functionality, explicitly communicating TDD intent so no mock stubs or placeholder implementations are created prematurely. Once the tests are written, they are executed to **confirm they fail** (red phase). Only after this verification does implementation begin. The final goal is a full green suite - without modifying any previously written tests. This tight feedback loop gives the agent a reliable signal for correctness and dramatically reduces ambiguous iteration.

---

## 2. Dependency and Environment Validation on Project Setup

When bootstrapping a new project, dependency versions are never assumed - they are explicitly verified. This includes running `npm audit`, executing linter checks, and running test suites (e.g., `pytest`) to confirm the baseline environment is clean and all tooling versions are compatible. This prevents an entire category of subtle bugs that only surface later under load or in production.

---

## 3. Phase-Based Task Files for Complex Features

Before any complex feature is implemented, the agent is asked to produce a structured **task file**. This file breaks the work into clearly defined phases, each containing its own granular tasks. This creates a shared contract between developer and agent - making progress trackable, reducing scope creep, and ensuring that nothing is silently skipped.

---

## 4. One Chat Per Phase - Context Discipline

Each phase of a task file gets its own dedicated chat session. This is a deliberate architectural decision: by loading only the context relevant to the current phase, token usage is significantly reduced and response quality is higher. In practice, this discipline has led to measurable token savings and noticeably more focused, accurate agent outputs across the day-to-day development cycle.

---

## 5. Planning Before Execution

Every chat session begins with a planning step. The agent is asked to:

- Describe the intended approach in plain language
- List all files likely to be affected
- Identify the specific functions or modules involved
- Include Mermaid diagrams where they aid understanding
- Explicitly name risks and edge cases
- Ask clarifying questions before proceeding
- Create a structured todo list

Alternatively, Cursor's built-in **Plan Mode** is used, as it provides all of the above by default. This planning artifact becomes the basis for review before a single line of code is changed.

---

## 6. Plan Review and Controlled Execution

The plan is reviewed thoroughly before execution begins. This is **where the developer must invest the most time** - understanding what will happen, why, and whether it aligns with the broader architecture. Parallel chat sessions are used to answer open questions without polluting the execution context.

During execution, **no commands are whitelisted that could cause irreversible side effects** - with one deliberate exception: `git commit` is whitelisted, because in this workflow every commit represents a logically complete, coherent unit of work (equivalent to a finished ticket). All other commands are reviewed and confirmed before execution. This is a non-negotiable safeguard: it is not uncommon for agents to delete a file as the path of least resistance to resolving an error.

---

## 7. Routing Questions to the Right Tool

A key discipline in this workflow is knowing **where to ask which type of question**:

- **Single-focus questions** (e.g., edge cases, clarifications about a specific function) are asked in isolated chat sessions to preserve answer precision. Combining multiple questions in one session degrades response quality.
- **Factual or version-specific questions** (e.g., "What is the latest stable version of X?", "How does library Y handle Z?") are routed to general-purpose models like ChatGPT or Gemini - not to the IDE agent, which lacks up-to-date web access and will hallucinate confidently.
- **Research and tool selection** (e.g., "Which vector database best fits our use case?") follows a structured three-step process:
  1. The IDE agent generates a project description and technical documentation from the codebase.
  2. A foundation model (GPT, Gemini, etc.) is used to write a research prompt for an agent that will evaluate options against the documented requirements.
  3. The documents are uploaded to **NotebookLM**, activated as sources, and the research prompt is pasted into the chat. NotebookLM autonomously initiates a deep research run, self-generates an optimized internal prompt, and produces a structured comparison of options with clear recommendations. The resulting report typically makes the best choice immediately apparent.

---

## 8. Understanding Over Output - The Most Important Principle

Whenever a question arises during development, it must be answered before moving on. Skipping this step - in the name of speed - leads to gaps in project and architecture understanding, which compound rapidly into poor decisions, brittle code, and costly rework.

The counterintuitive rule is: **write less new code, build more understanding**. When something is unclear, the right move is to pause, open a dedicated chat, and get a thorough explanation. This is how real technical depth is built - regardless of how complex the project is - and it is what separates developers who scale with AI from those who are overwhelmed by it.

---

## 9. Performance Benchmark — Competitive Positioning

The following metrics were recorded during the development of this project across **20.9 active development hours**, processing **153,525,739 tokens** and producing **52,502 lines of edited code**.

### 9.1 Output Velocity vs. Industry Baseline

| Developer Tier | Tokens / Hour | LOC / Hour |
|---|---|---|
| Average Developer | 15,000 – 45,000 | 10 – 50 |
| Top 1% Elite | 1,000,000 – 3,000,000 | 500 – 1,000 |
| **This Project** | **7,350,000** | **2,512** |
| **Global Percentile** | **Top 0.01%** | **~100× baseline** |

These figures reflect a **human-in-the-loop, serially orchestrated** workflow — not a fully automated pipeline. Every output line was reviewed, understood, and accepted by the developer before being committed.

### 9.2 Velocity-to-Quality Ratio

Generating 2,500+ LOC per hour is achievable with brute-force prompting. Keeping that code production-ready is not.

**Code Retention Rate: ~99%**

This metric measures the proportion of generated code that survived into the final committed codebase without rework. It reflects the effectiveness of TDD guardrails, context isolation, and plan-first architecture in eliminating wasted cycles. High velocity without high retention is a hallucination problem in disguise.

### 9.3 Zero-Hallucination Architecture — The Methodology Behind the Numbers

The high retention rate is not coincidental. It is the result of four deliberate constraints applied throughout development:

**1. Serialized Reasoning (Plan Mode First)**
Every session begins in Plan Mode. The agent produces a written architecture plan — listing affected files, functions, risks, and edge cases — before a single line of code is changed. This externalizes the agent's reasoning and makes hallucination-prone assumptions visible before they become bugs.

**2. Test-Driven Development (TDD) as a Correctness Signal**
Tests are written before implementation. The agent has a machine-verifiable signal for correctness at every step. This eliminates the primary vector for undetected hallucination: code that looks plausible but behaves incorrectly.

**3. Context Isolation (1 Chat Per Phase)**
Each phase of a task runs in a dedicated chat session. This prevents the "long-thread syndrome" — the gradual degradation of agent output quality as context fills with unrelated prior turns. Isolated context produces measurably more precise outputs.

**4. Tool Routing (Right Model for Right Question)**
Version-specific or factual queries (e.g., "What is the latest stable release of X?") are deliberately routed to web-connected foundation models, not the IDE agent. The IDE agent lacks live web access and will produce confident, incorrect answers. Routing prevents this entire class of error.

### 9.4 Token-Compute Tradeoff

**~2,900 tokens per LOC** is, by algorithm-efficiency standards, high. By business standards, it is the correct trade.

Each token spent represents the agent re-auditing system state, validating assumptions, or re-running a mental model of the architecture. This deliberate redundancy eliminates the need for costly human rework cycles later. The tradeoff is explicit:

> **Cheap compute tokens → expensive human validation time saved**

This is the same principle behind automated testing infrastructure: the upfront compute cost is justified by the downstream elimination of regression-driven rework. In a startup context, shipping correct code fast is worth more than shipping fast code that requires a week of debugging.

---

*This workflow is continuously refined. The principles above reflect a production-tested approach to AI-assisted engineering that prioritizes correctness, clarity, and developer ownership at every step.*
