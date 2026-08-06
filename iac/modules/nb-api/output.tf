output "resource_group_name" {
  value = azurerm_resource_group.this.name
}

output "resource_group_id" {
  value = azurerm_resource_group.this.id
}

output "identity_name" {
  value = azurerm_user_assigned_identity.this.name
}

output "identity_id" {
  value = azurerm_user_assigned_identity.this.id
}

output "identity_principal_id" {
  value = azurerm_user_assigned_identity.this.principal_id
}

output "log_analytics_workspace_name" {
  value = azurerm_log_analytics_workspace.this.name
}

output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.this.id
}

output "log_analytics_workspace_key" {
  value     = azurerm_log_analytics_workspace.this.primary_shared_key
  sensitive = true
}

output "nsg_name" {
  value = module.nsg.name
}

output "nsg_id" {
  value = module.nsg.resource_id
}

output "vnet_name" {
  value = module.vnet.name
}

output "vnet_id" {
  value = module.vnet.resource_id
}

output "vnet_address_space" {
  value = module.vnet.address_spaces
}

output "key_vault_name" {
  value = module.kv.name
}

output "key_vault_id" {
  value = module.kv.resource_id
}

output "app_service_plan_name" {
  value = module.asp.name
}

output "app_service_plan_id" {
  value = module.asp.resource_id
}

output "app_service_name" {
  value = module.app_service.name
}

output "app_service_id" {
  value = module.app_service.resource_id
}

output "app_service_default_hostname" {
  value = module.app_service.resource_uri
}

output "container_registry_name" {
  value = module.acr.name
}

output "container_registry_id" {
  value = module.acr.resource_id
}

output "container_registry_login_server" {
  value = module.acr.login_server
}

output "postgresql_server_name" {
  value = module.psql.name
}

output "postgresql_server_id" {
  value = module.psql.resource_id
}

output "postgresql_admin_password" {
  value     = random_password.postgres_admin.result
  sensitive = true
}

