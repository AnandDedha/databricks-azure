resource "azuread_application" "app" {
  display_name = "${var.prefix}-sp"
}

resource "azuread_service_principal" "sp" {
  client_id = azuread_application.app.application_id
}

resource "azuread_application_password" "sp_secret" {
  application_object_id = azuread_application.app.object_id
  display_name          = "tf-secret"
  rotate_when_changed   = false
}

resource "azurerm_role_assignment" "blob_contrib" {
  scope                = azurerm_storage_account.sa.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azuread_service_principal.sp.object_id
}
