# CPU-Only Course Ontology Builder Using a Small Language Model

## Project status

This three-member research project is in the **prototype implementation
phase**. Dataset loading, deterministic schema validation, heuristic evidence
gating, escalation storage, conservative canonicalization, evaluation
metrics, a CLI, and optional Ollama/Neo4j adapters are implemented. Real
research evaluation and CPU-only verification are still pending.

## Project description

The project will investigate a CPU-only course ontology builder that uses a
small language model to help organize course information into a structured
ontology. The implementation and evaluation work will be added in later
phases.

## Research objective

The research objective is to study a practical workflow for building a
course ontology with a small language model while emphasizing structured
schemas, evidence-based outputs, validation, and controlled escalation.
CPU-only inference is a project target, but it has not been configured or
verified in this setup phase.

## Technology stack

- Python 3.14
- Visual Studio Code
- Git and GitHub
- A Python virtual environment created with `venv`
- Ollama and Qwen3:4B (existing local installation; model configuration is a
  later phase)
- Neo4j Community Edition (a later phase)

The original environment setup did not install Ollama, Neo4j, or heavy
machine-learning dependencies. The prototype phase now declares lightweight
optional adapters for Ollama, Neo4j, and process-memory measurement in
`requirements.txt`.

## Project structure

```text
Course-Ontology-Builder/
├── data/
│   ├── raw/
│   ├── processed/
│   └── annotated/
├── prompts/
├── schemas/
├── src/
├── experiments/
│   ├── baseline/
│   ├── schema_validation/
│   ├── evidence_gate/
│   └── escalation/
├── results/
├── notebooks/
├── tests/
├── docs/
├── .vscode/
│   └── settings.json
├── requirements.txt
├── README.md
└── .gitignore
```

The runnable modules are under `src/`. The sample CSV is explicitly
illustrative and must not be used as research evaluation data.

## Quick start

From the repository root:

```powershell
.\.venv\Scripts\Activate.ps1
python -m unittest discover -s tests -v
python -m src smoke-test
python -m src validate-dataset data\raw\sample_courses.csv
```

The smoke test only validates loading and preprocessing. It does not claim
that extraction, semantic evidence verification, graph loading, or CPU-only
inference has been completed.

## Ontology and experiment conditions

The initial ontology is defined in `schemas/ontology.json`. It permits
Course, Topic, Prerequisite, LearningOutcome, Skill, Department, and
University, with only the documented relationship types. Conditions are:

- `baseline`: structured output without schema/evidence gating
- `schema_validation`: baseline plus deterministic ontology validation
- `evidence_gate`: schema validation plus evidence location and heuristic checks
- `escalation`: evidence gate plus a human review CSV queue

Run an experiment over prepared JSON extraction files with:

```powershell
python -m src run-experiment evidence_gate `
  --input data\raw\sample_courses.csv `
  --extractions results\extractions `
  --output results
```

Existing experiment output is never replaced unless `--overwrite` is
explicitly supplied. Manual annotation comparison is available with:

```powershell
python -m src evaluate --predicted results\evidence_gate\predictions.csv `
  --annotated data\annotated\ground_truth.csv
```

No precision, recall, F1, or paper result is generated without manual
annotations. Use `data\templates\annotation_template.csv` for ground truth.

## Ollama extraction

Ollama and `qwen3:4b` are optional runtime dependencies for extraction. The
adapter verifies the server and model without downloading anything. Configure
`OLLAMA_HOST` and `ONTOLOGY_MODEL` through environment variables, then use
`prompts\extraction_prompt.txt`. Raw responses and parsed JSON must be stored
separately for reproducibility. A local model does not prove CPU-only
execution; verify placement and utilization separately using system
monitoring.

## Optional Neo4j

Copy `.env.example` to `.env` and set real local Neo4j values only when
loading is being tested. `.env` is ignored and must never be committed.
Neo4j is not required for dataset validation, extraction preparation, or
evaluation scripts.

## Known limitations and research claims

The evidence gate currently performs deterministic evidence-location and
lexical-overlap checks. It is not semantic proof. The Neo4j adapter is
optional and requires a configured database. GPU utilization is not inferred
by the resource monitor. Larger-model comparison, real university data,
manual annotations, paper-ready results, and CPU-only verification remain
pending until measured in later experiments.

## Python 3.14 setup

Install Python 3.14 and confirm it is available:

```powershell
py -3.14 --version
```

From the project root, create a local virtual environment:

```powershell
py -3.14 -m venv .venv
```

Activate it in a Windows PowerShell terminal:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the venv interpreter directly or review
your local execution-policy settings with your administrator. Do not upload
`.venv`; every team member must create their own local environment.

Verify the environment:

```powershell
python --version
python -m pip --version
```

The Python executable and pip path should both point inside `.venv`.

## Running Python files

With the virtual environment activated, run a Python file from the project
root with:

```powershell
python path\to\file.py
```

Dependencies will be added to `requirements.txt` only after compatibility
testing in the next phase. Install them later with:

```powershell
python -m pip install -r requirements.txt
```

## GitHub collaboration

The repository owner should use the private GitHub repository
`CPU-Only-Course-Ontology-Builder-`, then invite the other two members under
**Settings > Collaborators**.

After the repository is created, the owner can connect this local repository
without changing its history:

```powershell
git remote add origin https://github.com/<OWNER>/CPU-Only-Course-Ontology-Builder-.git
git branch -M main
git add .
git commit -m "Set up development environment"
git push -u origin main
```

Only run the commit and push commands after the team has reviewed the files
and explicitly approved the initial commit.

Each member should clone the repository, create their own `.venv`, and select
that interpreter in VS Code:

```powershell
git clone https://github.com/<OWNER>/CPU-Only-Course-Ontology-Builder-.git
cd CPU-Only-Course-Ontology-Builder-
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

In VS Code, use **Python: Select Interpreter** and choose the interpreter at
`.venv\Scripts\python.exe`. Never share or upload a virtual environment,
credentials, API keys, passwords, or other local secrets.

Use the following routine to synchronize work:

```powershell
git pull --rebase origin main
git status
git add <files>
git commit -m "Describe the change"
git push origin main
```

Coordinate before pushing changes to shared branches. Use feature branches
and pull requests when the team wants review before merging.
