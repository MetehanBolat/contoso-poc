variable "location" {
  description = "The location where the resource group will be created."
  type        = string
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

variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
}

variable "identity_name" {
  description = "The name of the user-assigned managed identity."
  type        = string
}

variable "log_analytics_workspace_name" {
  description = "The name of the Log Analytics workspace."
  type        = string
}

variable "application_insights_name" {
  description = "The name of the Azure Application Insights resource."
  type        = string
}

variable "key_vault_name" {
  description = "The name of the Key Vault."
  type        = string
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

variable "nsg_name" {
  description = "The name of the network security group."
  type        = string
}

variable "vnet_name" {
  description = "The name of the virtual network."
  type        = string
}

variable "vnet_address_space" {
  description = "The address space for the virtual network."
  type        = string
}

variable "pe_subnet_name" {
  description = "The name of the private endpoint subnet."
  type        = string
}

variable "pe_subnet_address_space" {
  description = "The address space for the private endpoint subnet."
  type        = string
}

variable "app_subnet_name" {
  description = "The name of the application subnet."
  type        = string
}

variable "app_subnet_address_space" {
  description = "The address space for the application subnet."
  type        = string
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
  description = "The SKU name of the App Service plan. Use a consumption plan such as Y1 for the cheapest option."
  type        = string
}

variable "app_service_container_image" {
  description = "The container image reference for the App Service. Use the ACR login server prefix for private registry images."
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

variable "tags" {
  description = "A map of tags to assign to the resources."
  type        = map(string)
  default     = {}
}
