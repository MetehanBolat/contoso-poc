module "nb-api" {

  source = "../../modules/nb-api"

  location    = var.location
  environment = var.environment

  resource_group_name = var.resource_group_name

  identity_name                = var.identity_name
  key_vault_name               = var.key_vault_name
  log_analytics_workspace_name = var.log_analytics_workspace_name
  application_insights_name    = var.application_insights_name
  nsg_name                     = var.nsg_name
  vnet_name                    = var.vnet_name
  vnet_address_space           = var.vnet_address_space
  pe_subnet_name               = var.pe_subnet_name
  pe_subnet_address_space      = var.pe_subnet_address_space
  app_subnet_name              = var.app_subnet_name
  app_subnet_address_space     = var.app_subnet_address_space
  app_service_plan_name        = var.app_service_plan_name
  app_service_name             = var.app_service_name
  app_service_plan_sku_name    = var.app_service_plan_sku_name
  app_service_container_image  = var.app_service_container_image
  container_registry_name      = var.container_registry_name
  container_registry_sku       = var.container_registry_sku
  postgres_server_name         = var.postgres_server_name
  postgres_server_sku          = var.postgres_server_sku
  postgres_database_name       = var.postgres_database_name
  postgres_admin_login         = var.postgres_admin_login

  tags = var.tags
}
