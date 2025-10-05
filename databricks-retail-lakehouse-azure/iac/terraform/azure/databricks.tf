resource "databricks_catalog" "catalog" {
  name    = var.uc_catalog
  comment = "Retail demo catalog"
}

resource "databricks_schema" "schema" {
  name         = var.uc_schema
  catalog_name = databricks_catalog.catalog.name
  comment      = "Core schema"
}

resource "databricks_storage_credential" "cred" {
  name = "${var.prefix}_az_sp_cred"
  azure_service_principal {
    client_id     = azuread_application.app.application_id
    client_secret = azuread_application_password.sp_secret.value
    tenant_id     = data.azurerm_client_config.current.tenant_id
  }
}

resource "databricks_external_location" "ext" {
  name            = "${var.prefix}_ext"
  url             = "abfss://${azurerm_storage_data_lake_gen2_filesystem.fs.name}@${azurerm_storage_account.sa.name}.dfs.core.windows.net"
  credential_name = databricks_storage_credential.cred.name
  comment         = "Retail external location"
}

resource "databricks_volume" "v_raw" {
  name             = "v_raw"
  catalog_name     = databricks_catalog.catalog.name
  schema_name      = databricks_schema.schema.name
  volume_type      = "EXTERNAL"
  storage_location = "${databricks_external_location.ext.url}/raw"
  depends_on       = [databricks_external_location.ext]
}

resource "databricks_grants" "ext_grants" {
  count = var.uc_principal == null ? 0 : 1
  external_location = databricks_external_location.ext.id
  grant { principal = var.uc_principal  privileges = ["READ_FILES", "WRITE_FILES"] }
}

resource "databricks_grants" "vol_grants" {
  count = var.uc_principal == null ? 0 : 1
  volume = databricks_volume.v_raw.id
  grant { principal = var.uc_principal  privileges = ["READ_VOLUME", "WRITE_VOLUME"] }
}
