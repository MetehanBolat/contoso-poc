module "laws" {
  source  = "Azure/avm-res-operationalinsights-workspace/azurerm"
  version = "0.5.1"

  enable_telemetry    = false
  location            = azurerm_resource_group.this.location
  name                = var.log_analytics_workspace_name
  resource_group_name = azurerm_resource_group.this.name
  tags = merge(local.tags, {
    "service-name" = var.log_analytics_workspace_name
  })

  monitor_private_link_scope = {
    pe1 = {
      name        = "law_pl_scope"
      resource_id = azurerm_resource_group.this.id
    }
  }

  monitor_private_link_scoped_service_name = "law_pl_service"

  private_endpoints = {
    default = {
      subnet_resource_id          = module.vnet.subnets["subnet0"].resource_id
      network_interface_name      = "nic1"
      private_dns_zone_group_name = "dnslinktovnet"
    }
  }

  role_assignments = {
    log_analytics_contributor_user_assigned_identity = {
      role_definition_id_or_name = "Log Analytics Contributor"
      principal_id               = azurerm_user_assigned_identity.this.principal_id
    }
  }
}

resource "azurerm_application_insights" "this" {
  name                = var.application_insights_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  application_type    = "other"
  workspace_id        = module.laws.resource.id
  retention_in_days   = 365
}
