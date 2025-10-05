output "storage_account_name" { value = azurerm_storage_account.sa.name }
output "filesystem"          { value = azurerm_storage_data_lake_gen2_filesystem.fs.name }
output "abfss_url"           { value = "abfss://${azurerm_storage_data_lake_gen2_filesystem.fs.name}@${azurerm_storage_account.sa.name}.dfs.core.windows.net" }
output "sp_client_id"        { value = azuread_application.app.application_id }
output "sp_client_secret"    { value = azuread_application_password.sp_secret.value  sensitive = true }
output "uc_volume_path"      { value = "/Volumes/${var.uc_catalog}/${var.uc_schema}/v_raw" }
