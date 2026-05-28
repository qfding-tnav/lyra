# AI Agent Workflow System

An AI-driven multi-agent workflow system for automated software engineering tasks.

This project implements a Planner → Generator → Evaluator → Healer workflow using independent AI agents and GitHub Actions automation.

---

# Project Overview

The system is designed around a modular agent architecture:

* **Planner Agent**
  Creates implementation plans and task breakdowns.

* **Generator Agent**
  Generates source code and related artifacts.

* **Evaluator Agent**
  Validates generated code through tests, checks, or evaluations.

* **Healer Agent**
  Attempts to automatically fix failed implementations or evaluations.

The workflow is orchestrated through GitHub Actions pipelines.

---

# Directory Structure

```text
.
├── .github/
│   └── workflows/      # CI/CD pipelines for individual agent execution
├── agents/             # Core logic for the autonomous agents
│   ├── skills/         # Reusable tools and capabilities for agents
│   ├── evaluator.py    # Tests and validates generated code
│   ├── generator.py    # Writes the actual source code and tests
│   ├── healer.py       # Debugs and fixes failing code based on evaluation
│   └── planner.py      # Breaks down user prompts into actionable steps
├── artifacts/          # The output directory for generated software
│   ├── src/            # Generated source code (e.g., converter.py)
│   └── tests/          # Generated unit tests (e.g., test_converter.py)
├── config/             # System and agent configuration files
├── sandbox/            # Isolated environment for safely executing code
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
```

---

# Components

## `agents/`

Contains the core AI agent implementations.

| File           | Description                        |
| -------------- | ---------------------------------- |
| `planner.py`   | Generates execution plans          |
| `generator.py` | Produces implementation code       |
| `evaluator.py` | Runs evaluation and validation     |
| `healer.py`    | Repairs failed outputs             |
| `skills/`      | Shared reusable agent capabilities |

---

## `artifacts/`

Stores generated outputs and evaluation artifacts.

Example:

```text
artifacts/
├── src/
└── tests/
```

Typical contents:

* Generated source code
* Test cases
* Evaluation results
* Debug outputs

---

## `.github/workflows/`

GitHub Actions automation workflows.

| Workflow        | Purpose                     |
| --------------- | --------------------------- |
| `planner.yml`   | Executes planning stage     |
| `generator.yml` | Executes code generation    |
| `evaluator.yml` | Executes validation/testing |
| `healer.yml`    | Executes automatic repair   |

---

## `sandbox/`

Temporary execution environment for experiments, testing, and isolated runs.

---

## `config/`

Configuration files for:

* Models
* Runtime settings
* Environment variables
* Agent parameters

---

# Workflow Architecture

```text
Planner
   ↓
Generator
   ↓
Evaluator
   ↓
Healer (if evaluation fails)
```

The system supports iterative improvement loops:

```text
Plan → Generate → Evaluate → Heal → Re-evaluate
```

---

# Installation

## Requirements

* Python 3.11+
* Git
* GitHub Actions (optional)

---

## Setup

```bash
git clone <repository-url>
cd <project-name>

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

# License

MIT License
