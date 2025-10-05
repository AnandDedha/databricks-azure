resource "azurerm_resource_group" "rg" {
  name     = coalesce(var.resource_group, "${var.prefix}-rg")
  location = var.location
}

resource "random_id" "suffix" { byte_length = 4 }

resource "azurerm_storage_account" "sa" {
  name                     = replace("${var.prefix}sa${random_id.suffix.hex}", "-", "")
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true
  min_tls_version          = "TLS1_2"
}

resource "azurerm_storage_data_lake_gen2_filesystem" "fs" {
  name               = "retail"
  storage_account_id = azurerm_storage_account.sa.id
}

resource "azurerm_storage_data_lake_gen2_path" "dirs" {
  for_each            = toset(["raw","bronze","silver","gold","_checkpoints"])
  path                = each.value
  filesystem_name     = azurerm_storage_data_lake_gen2_filesystem.fs.name
  storage_account_id  = azurerm_storage_account.sa.id
  resource            = "directory"
}
