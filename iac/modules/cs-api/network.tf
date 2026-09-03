module "nsg" {
  source  = "Azure/avm-res-network-networksecuritygroup/azurerm"
  version = "0.5.1"

  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  enable_telemetry    = false
  name                = var.nsg_name

  diagnostic_settings = {
    sendToLogAnalytics = {
      name                           = "sendToLogAnalytics"
      workspace_resource_id          = module.laws.resource.id
      log_analytics_destination_type = "Dedicated"
    }
  }

  tags = merge(var.tags, {
    "service-name" = var.nsg_name
  })
}

module "vnet" {
  source  = "Azure/avm-res-network-virtualnetwork/azurerm"
  version = "0.19.0"

  #ddos_protection_plan = {
  #  id = azurerm_network_ddos_protection_plan.this.id
  #  # due to resource cost
  #  enable = false
  #}

  diagnostic_settings = {
    sendToLogAnalytics = {
      name                           = "sendToLogAnalytics"
      workspace_resource_id          = module.laws.resource.id
      log_analytics_destination_type = "Dedicated"
    }
  }

  encryption = {
    enabled     = true
    enforcement = "AllowUnencrypted"
  }

  location         = azurerm_resource_group.this.location
  parent_id        = azurerm_resource_group.this.id
  address_space    = [var.vnet_address_space]
  enable_telemetry = false
  name             = var.vnet_name

  subnets = {
    subnet0 = {
      name             = var.pe_subnet_name
      address_prefixes = [var.pe_subnet_address_space]
    }
    subnet1 = {
      name                            = var.app_subnet_name
      address_prefixes                = [var.app_subnet_address_space]
      default_outbound_access_enabled = false
      delegations = [{
        name = "Microsoft.Web.serverFarms"
        service_delegation = {
          name = "Microsoft.Web/serverFarms"
        }
      }]
      network_security_group = {
        id = module.nsg.resource_id
      }
    }
  }

  tags = merge(var.tags, {
    "service-name" = var.vnet_name
  })
}
