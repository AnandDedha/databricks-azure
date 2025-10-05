terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm   = { source = "hashicorp/azurerm",   version = "~> 3.118" }
    azuread   = { source = "hashicorp/azuread",   version = "~> 2.51" }
    databricks= { source = "databricks/databricks", version = "~> 1.42.0" }
    random    = { source = "hashicorp/random", version = "~> 3.6" }
  }
}

provider "azurerm" { features {} }
provider "azuread" {}
provider "databricks" {
  host  = var.databricks_host
  token = var.databricks_token
}

data "azurerm_client_config" "current" {}
