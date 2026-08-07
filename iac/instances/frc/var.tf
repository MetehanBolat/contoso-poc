variable "subscription_id" {
  description = "The subscription ID where the resources will be created."
  type        = string
  #default     = "8486ac29-bcbd-4691-9ff6-52a901335eb0"
}

variable "environment" {
  description = "The environment for the resources."
  type        = string
  #default     = "dev"

  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "The environment must be one of 'dev' or 'prod'."
  }
}

variable "location" {
  description = "The location where the resource group will be created."
  type        = string
  default     = "francecentral"
}

variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
  #default     = "novabank-rg"
}

variable "identity_name" {
  description = "The name of the user-assigned managed identity."
  type        = string
  #default     = "novabank-id"
}

variable "log_analytics_workspace_name" {
  description = "The name of the Log Analytics workspace."
  type        = string
  #default     = "novabank-laws"
}

variable "application_insights_name" {
  description = "The name of the Azure Application Insights resource."
  type        = string
  #default     = "novabank-ai"
}

variable "nsg_name" {
  description = "The name of the network security group."
  type        = string
  #default     = "novabank-nsg"
}

variable "vnet_name" {
  description = "The name of the virtual network."
  type        = string
  #default     = "novabank-vnet"
}

variable "vnet_address_space" {
  description = "The address space for the virtual network."
  type        = string
  #default     = "10.0.0.0/16"
}

variable "pe_subnet_name" {
  description = "The name of the private endpoint subnet."
  type        = string
  #default     = "novabank-pe-subnet"
}

variable "pe_subnet_address_space" {
  description = "The address space for the private endpoint subnet."
  type        = string
  #default     = ""
}

variable "app_subnet_name" {
  description = "The name of the application subnet."
  type        = string
  #default     = "novabank-app-subnet"
}

variable "app_subnet_address_space" {
  description = "The address space for the application subnet."
  type        = string
  #default     = ""
}

variable "app_service_plan_name" {
  description = "The name of the App Service plan."
  type        = string
}

variable "app_service_name" {
  description = "The name of the container-based App Service."
  type        = string
}

variable "app_service_plan_sku_name" {
  description = "The SKU name of the App Service plan."
  type        = string
  default     = "F1"
}

variable "app_service_container_image" {
  description = "The container image reference for the App Service."
  type        = string
  default     = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
}

variable "container_registry_name" {
  description = "The name of the Azure Container Registry."
  type        = string
}

variable "container_registry_sku" {
  description = "The SKU of the Azure Container Registry."
  type        = string
  default     = "Basic"
}

variable "key_vault_name" {
  description = "The name of the Key Vault."
  type        = string
  #default     = "novabank-kv"
}

variable "postgres_server_name" {
  description = "The name of the PostgreSQL Flexible Server."
  type        = string
}

variable "postgres_server_sku" {
  description = "The SKU of the PostgreSQL Flexible Server."
  type        = string
  default     = "B_Standard_B1ms"
}

variable "postgres_database_name" {
  description = "The name of the PostgreSQL database."
  type        = string
}

variable "postgres_admin_login" {
  description = "The administrator login for the PostgreSQL Flexible Server."
  type        = string
  default     = "psqladmin"
}

variable "tags" {
  description = "A map of tags to assign to the resources."
  type        = map(string)
  default     = {}
}
