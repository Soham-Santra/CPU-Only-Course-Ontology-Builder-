# CPU-Only Course Ontology Builder Using a Small Language Model

## Project status

This three-member research project is currently in the **development
environment setup phase**. Course extraction, validation, evidence gating,
escalation, and graph construction have not been implemented yet.

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

No Ollama, model, Neo4j, or heavy machine-learning dependencies are installed
by this setup step.

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
├── .vscode/
│   └── settings.json
├── requirements.txt
├── README.md
└── .gitignore
```

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

The repository owner should create a **private** GitHub repository named
`Course-Ontology-Builder`, then invite the other two members under
**Settings > Collaborators**.

After the repository is created, the owner can connect this local repository
without changing its history:

```powershell
git remote add origin https://github.com/<OWNER>/Course-Ontology-Builder.git
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
git clone https://github.com/<OWNER>/Course-Ontology-Builder.git
cd Course-Ontology-Builder
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
