resource "azurerm_private_dns_zone" "acr" {
  name                = "privatelink.azurecr.io"
  resource_group_name = azurerm_resource_group.this.name

  tags = merge(local.tags, {
    "service-name" = var.container_registry_name
  })
}

resource "azurerm_private_dns_zone" "kv" {
  name                = "privatelink.vaultcore.azure.net"
  resource_group_name = azurerm_resource_group.this.name

  tags = merge(local.tags, {
    "service-name" = var.key_vault_name
  })
}

resource "azurerm_private_dns_zone" "psql" {
  name                = "privatelink.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.this.name

  tags = merge(local.tags, {
    "service-name" = var.postgres_server_name
  })
}

resource "azurerm_private_dns_zone_virtual_network_link" "kv" {
  name                  = "link-${var.vnet_name}-kv"
  resource_group_name   = azurerm_resource_group.this.name
  private_dns_zone_name = azurerm_private_dns_zone.kv.name
  virtual_network_id    = module.vnet.resource_id
  registration_enabled  = false

  tags = merge(local.tags, {
    "service-name" = var.vnet_name
  })
}

resource "azurerm_private_dns_zone_virtual_network_link" "psql" {
  name                  = "link-${var.vnet_name}-psql"
  resource_group_name   = azurerm_resource_group.this.name
  private_dns_zone_name = azurerm_private_dns_zone.psql.name
  virtual_network_id    = module.vnet.resource_id
  registration_enabled  = false

  tags = merge(local.tags, {
    "service-name" = var.vnet_name
  })
}

resource "azurerm_private_dns_zone_virtual_network_link" "acr" {
  name                  = "link-${var.vnet_name}-acr"
  resource_group_name   = azurerm_resource_group.this.name
  private_dns_zone_name = azurerm_private_dns_zone.acr.name
  virtual_network_id    = module.vnet.resource_id
  registration_enabled  = false

  tags = merge(local.tags, {
    "service-name" = var.vnet_name
  })
}
