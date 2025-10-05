# Azure + Unity Catalog IaC

## Prereqs
- `az login` and `az account set -s <SUB_ID>`
- Databricks workspace with Unity Catalog attached
- Databricks PAT (Personal Access Token)

## Configure
Create `terraform.tfvars`:
```hcl
prefix           = "retail"
location         = "canadacentral"
databricks_host  = "https://adb-<wsid>.<hash>.azuredatabricks.net"
databricks_token = "dapix-..."
uc_catalog       = "playground"
uc_schema        = "core"
uc_principal     = "data-engineers"   # optional
```

## Run
```bash
terraform init
terraform apply -auto-approve
```

## After apply
- External Location: see `abfss_url` output
- UC External Volume: `/Volumes/<catalog>/<schema>/v_raw`
- Store SP secret in Databricks Secrets or Key Vault

## Destroy
```bash
terraform destroy -auto-approve
```
