# Databricks Retail Lakehouse (Azure) — End-to-End Data Engineering

This repo demonstrates a production-ready Databricks data engineering project using a **Retail Orders** domain, the **Medallion Architecture** (Bronze → Silver → Gold), **Unity Catalog**, and **Azure ADLS Gen2** storage. It includes both a **Delta Live Tables** pipeline and a **Workflows (Jobs + Notebooks)** path, plus **Terraform** to provision Azure resources and UC objects.

## Quick Start (Vibe Coding on Azure)
1) Create or choose a UC catalog & schema (defaults used below: `playground.core`).  
2) (Option A) Use a UC **managed Volume** for fastest start.  
3) (Option B) Use **ADLS Gen2 external location** via Terraform in `iac/terraform/azure`.

### Run the "vibe" notebook
- Import `notebooks/vibe_azure_quickstart.py` as a Python notebook.
- Run top to bottom to generate test data, ingest Bronze (Auto Loader), shape Silver, and build Gold facts.

## Orchestration Options
- **Delta Live Tables**: `notebooks/dlt_pipeline.py`
- **Workflows**: `jobs/retail_workflow.json`

## Governance
- **Unity Catalog** tables in `retail_*` or `playground.core`.
- Example grants in `sql/grants_uc.sql`.

## Tests
- Minimal PySpark unit test in `tests/test_silver_orders.py` (uses `chispa`).

## CI/CD
- `.github/workflows/ci_cd.yaml` runs `pytest` and (optionally) deploys the Workflow via Databricks CLI.

## Azure IaC (Terraform)
- `iac/terraform/azure` provisions: ADLS Gen2 storage, SP/RBAC, UC Storage Credential, External Location, and an External Volume.
- After `terraform apply`, check outputs and plug into notebooks or DLT pipeline config.

---

### Repo Layout
```
notebooks/
  01_bronze_ingest_orders_autoloader.py
  02_silver_transformations.py
  03_gold_marts.sql
  dlt_pipeline.py
  vibe_azure_quickstart.py
  utils/io.py

sql/
  grants_uc.sql

jobs/
  retail_workflow.json

tests/
  test_silver_orders.py

.github/workflows/
  ci_cd.yaml

docs/
  runbook.md

iac/terraform/azure/
  main.tf, variables.tf, storage.tf, identity.tf, databricks.tf, outputs.tf, README.md

requirements-dev.txt
pyproject.toml
.gitignore
```

## Push to GitHub
```bash
# inside the repo folder
git init
git add .
git commit -m "Initial commit: Databricks Retail Lakehouse (Azure)"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```
