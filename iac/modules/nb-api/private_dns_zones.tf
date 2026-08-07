module "pdns-kv" {
  source  = "Azure/avm-res-network-privatednszone/azurerm"
  version = "0.3.2"

  enable_telemetry = false

  domain_name         = "privatelink.vaultcore.azure.net"
  resource_group_name = azurerm_resource_group.this.name
  virtual_network_links = {
    default = {
      vnetlinkname = "link-${var.vnet_name}-kv"
      vnetid       = module.vnet.resource_id
    }
  }

  tags = merge(local.tags, {
    "service-name" = var.key_vault_name
  })
}

module "pdns-psql" {
  source  = "Azure/avm-res-network-privatednszone/azurerm"
  version = "0.3.2"

  enable_telemetry = false

  domain_name         = "privatelink.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.this.name
  virtual_network_links = {
    default = {
      vnetlinkname = "link-${var.vnet_name}-psql"
      vnetid       = module.vnet.resource_id
    }
  }

  tags = merge(local.tags, {
    "service-name" = var.postgres_server_name
  })
}

module "pdns-acr" {
  source  = "Azure/avm-res-network-privatednszone/azurerm"
  version = "0.3.2"

  enable_telemetry = false

  domain_name         = "privatelink.azurecr.io"
  resource_group_name = azurerm_resource_group.this.name
  virtual_network_links = {
    default = {
      vnetlinkname = "link-${var.vnet_name}-acr"
      vnetid       = module.vnet.resource_id
    }
  }

  tags = merge(local.tags, {
    "service-name" = var.container_registry_name
  })
}

module "pdns-laws" {
  source  = "Azure/avm-res-network-privatednszone/azurerm"
  version = "0.3.2"

  enable_telemetry = false

  domain_name         = "privatelink.monitor.azure.com"
  resource_group_name = azurerm_resource_group.this.name
  virtual_network_links = {
    default = {
      vnetlinkname = "link-${var.vnet_name}-laws"
      vnetid       = module.vnet.resource_id
    }
  }

  tags = merge(local.tags, {
    "service-name" = var.log_analytics_workspace_name
  })
}

module "pdns-laws-ods" {
  source  = "Azure/avm-res-network-privatednszone/azurerm"
  version = "0.3.2"

  enable_telemetry = false

  domain_name         = "privatelink.ods.opinsights.azure.com"
  resource_group_name = azurerm_resource_group.this.name
  virtual_network_links = {
    default = {
      vnetlinkname = "link-${var.vnet_name}-laws-ods"
      vnetid       = module.vnet.resource_id
    }
  }

  tags = merge(local.tags, {
    "service-name" = var.log_analytics_workspace_name
  })
}

module "pdns-laws-oms" {
  source  = "Azure/avm-res-network-privatednszone/azurerm"
  version = "0.3.2"

  enable_telemetry = false

  domain_name         = "privatelink.oms.opinsights.azure.com"
  resource_group_name = azurerm_resource_group.this.name
  virtual_network_links = {
    default = {
      vnetlinkname = "link-${var.vnet_name}-laws-oms"
      vnetid       = module.vnet.resource_id
    }
  }

  tags = merge(local.tags, {
    "service-name" = var.log_analytics_workspace_name
  })
}
