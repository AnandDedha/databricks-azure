variable "prefix"         { type = string  default = "retail" }
variable "location"       { type = string  default = "canadacentral" }
variable "resource_group" { type = string  default = null }

variable "databricks_host"  { type = string  description = "https://adb-<wsid>.<hash>.azuredatabricks.net" }
variable "databricks_token" { type = string  sensitive = true }

variable "uc_catalog" { type = string  default = "playground" }
variable "uc_schema"  { type = string  default = "core" }

variable "uc_principal" { type = string  default = null }  # e.g., "data-engineers"
