data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "this" {
  name     = var.resource_group_name
  location = var.location

  tags = merge(local.tags, {
    "service-name" = "novabank-api"
  })
}

resource "azurerm_user_assigned_identity" "this" {
  name                = var.identity_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location

  tags = merge(local.tags, {
    "service-name" = var.identity_name
  })
}

module "acr" {
  source  = "Azure/avm-res-containerregistry-registry/azurerm"
  version = "0.7.0"

  enable_telemetry              = false
  location                      = azurerm_resource_group.this.location
  name                          = var.container_registry_name
  resource_group_name           = azurerm_resource_group.this.name
  sku                           = var.container_registry_sku
  public_network_access_enabled = var.environment == "dev" ? true : false
  export_policy_enabled         = true
  admin_enabled                 = false
  zone_redundancy_enabled       = var.environment == "dev" ? false : true

  diagnostic_settings = {
    sendToLogAnalytics = {
      name                           = "sendToLogAnalytics"
      workspace_resource_id          = module.laws.resource.id
      log_analytics_destination_type = "Dedicated"
    }
  }

  role_assignments = {
    acr_pull_user_assigned_identity = {
      role_definition_id_or_name = "AcrPull"
      principal_id               = azurerm_user_assigned_identity.this.principal_id
    }
    acr_pull_current_client = {
      role_definition_id_or_name = "AcrPull"
      principal_id               = data.azurerm_client_config.current.object_id
    }
    acr_push_current_client = {
      role_definition_id_or_name = "AcrPush"
      principal_id               = data.azurerm_client_config.current.object_id
    }
  }

  private_endpoints = {
    default = {
      subnet_resource_id            = module.vnet.subnets["subnet0"].resource_id
      private_dns_zone_resource_ids = [module.pdns-acr.resource_id]
    }
  }

  tags = merge(local.tags, {
    "service-name" = var.container_registry_name
  })
}

module "asp" {
  source  = "Azure/avm-res-web-serverfarm/azurerm"
  version = "2.0.8"

  enable_telemetry       = false
  location               = azurerm_resource_group.this.location
  name                   = var.app_service_plan_name
  os_type                = "Linux"
  parent_id              = azurerm_resource_group.this.id
  sku_name               = var.app_service_plan_sku_name
  zone_balancing_enabled = true
  # Enable this for high availability. Only works on premium tier.
  worker_count = 1

  diagnostic_settings = {
    sendToLogAnalytics = {
      name                           = "sendToLogAnalytics"
      workspace_resource_id          = module.laws.resource.id
      log_analytics_destination_type = "Dedicated"
    }
  }

  tags = merge(local.tags, {
    "service-name" = var.app_service_plan_name
  })
}

module "app_service" {
  source  = "Azure/avm-res-web-site/azurerm"
  version = "0.22.0"

  enable_telemetry              = false
  location                      = azurerm_resource_group.this.location
  name                          = var.app_service_name
  parent_id                     = azurerm_resource_group.this.id
  service_plan_resource_id      = module.asp.resource_id
  https_only                    = true
  public_network_access_enabled = var.environment == "dev" ? true : false
  virtual_network_subnet_id     = module.vnet.subnets["subnet1"].resource_id
  #vnet_route_all_traffic        = var.environment == "dev" ? false : true

  managed_identities = {
    system_assigned            = false
    user_assigned_resource_ids = [azurerm_user_assigned_identity.this.id]
  }

  key_vault_reference_identity = azurerm_user_assigned_identity.this.id

  site_config = {
    always_on                                     = true #var.environment == "dev" ? false : true
    use_32_bit_worker                             = true
    ftps_state                                    = "FtpsOnly"
    http2_enabled                                 = true
    linux_fx_version                              = "DOCKER|${module.acr.login_server}/${var.app_service_container_image}"
    minimum_tls_version                           = "1.2"
    container_registry_use_managed_identity       = true
    container_registry_managed_identity_client_id = azurerm_user_assigned_identity.this.client_id
  }

  app_settings = {
    WEBSITES_PORT                         = "8080"
    DOCKER_REGISTRY_SERVER_URL            = "https://${module.acr.login_server}"
    POSTGRES_HOST                         = "${var.postgres_server_name}.postgres.database.azure.com"
    POSTGRES_PORT                         = "5432"
    POSTGRES_DB                           = var.postgres_database_name
    POSTGRES_USER                         = var.postgres_admin_login
    POSTGRES_PASSWORD                     = random_password.postgres_admin.result
    POSTGRES_SSLMODE                      = "disable"
    APPLICATIONINSIGHTS_CONNECTION_STRING = azurerm_application_insights.this.connection_string
    APPINSIGHTS_INSTRUMENTATIONKEY        = azurerm_application_insights.this.instrumentation_key
  }

  connection_strings = {
    postgres = {
      type  = "PostgreSQL"
      value = "Host=${var.postgres_server_name}.postgres.database.azure.com;Port=5432;Database=${var.postgres_database_name};Username=${var.postgres_admin_login};Password=${random_password.postgres_admin.result};SslMode=Disable"
    }
  }

  diagnostic_settings = {
    sendToLogAnalytics = {
      name                           = "sendToLogAnalytics"
      workspace_resource_id          = module.laws.resource.id
      log_analytics_destination_type = "Dedicated"
    }
  }

  tags = merge(local.tags, {
    "service-name" = var.app_service_name
  })
}

resource "random_password" "postgres_admin" {
  length           = 24
  override_special = "_%@"
  special          = true
}

module "psql" {
  source  = "Azure/avm-res-dbforpostgresql-flexibleserver/azurerm"
  version = "0.2.3"

  enable_telemetry             = false
  location                     = azurerm_resource_group.this.location
  name                         = var.postgres_server_name
  resource_group_name          = azurerm_resource_group.this.name
  geo_redundant_backup_enabled = var.environment == "dev" ? false : true

  diagnostic_settings = {
    sendToLogAnalytics = {
      name                           = "sendToLogAnalytics"
      workspace_resource_id          = module.laws.resource.id
      log_analytics_destination_type = "Dedicated"
    }
  }

  backup_retention_days = var.environment == "dev" ? 7 : 35

  administrator_login    = var.postgres_admin_login
  administrator_password = random_password.postgres_admin.result

  public_network_access_enabled = var.environment == "dev" ? true : false
  server_version                = 16
  sku_name                      = var.postgres_server_sku
  storage_mb                    = 32768
  auto_grow_enabled             = var.environment == "dev" ? false : true
  high_availability             = var.environment == "dev" ? null : { "mode" : "ZoneRedundant" }
  ## %99.99 SLA for zone redundant, %99.9 for single zone.
  zone = 1

  private_endpoints = {
    default = {
      subnet_resource_id            = module.vnet.subnets["subnet0"].resource_id
      private_dns_zone_resource_ids = [module.pdns-psql.resource_id]
    }
  }

  databases = {
    default = {
      name      = var.postgres_database_name
      charset   = "UTF8"
      collation = "en_US.utf8"
    }
  }

  tags = merge(local.tags, {
    "service-name" = var.postgres_server_name
  })
}

module "kv" {
  source  = "Azure/avm-res-keyvault-vault/azurerm"
  version = "0.10.2"

  tenant_id           = data.azurerm_client_config.current.tenant_id
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  name                = var.key_vault_name

  enable_telemetry = false

  diagnostic_settings = {
    sendToLogAnalytics = {
      name                           = "sendToLogAnalytics"
      workspace_resource_id          = module.laws.resource.id
      log_analytics_destination_type = "Dedicated"
    }
  }
  enabled_for_deployment          = true
  enabled_for_template_deployment = true
  enabled_for_disk_encryption     = false
  purge_protection_enabled        = var.environment == "dev" ? false : true

  network_acls = {
    default_action = "Allow"
    bypass         = "AzureServices"
  }

  role_assignments = {
    deployment_user_secrets = {
      role_definition_id_or_name = "Key Vault Secrets User"
      principal_id               = azurerm_user_assigned_identity.this.principal_id
    }
    deployment_principal = {
      role_definition_id_or_name = "Key Vault Administrator"
      principal_id               = data.azurerm_client_config.current.object_id
    }
  }

  wait_for_rbac_before_secret_operations = {
    create = "60s"
  }

  secrets = {
    postgre-user = {
      name = "postgre-user"
    }
    postgre-pass = {
      name = "postgre-pass"
    }
  }

  secrets_value = {
    postgre-user = var.postgres_admin_login
    postgre-pass = random_password.postgres_admin.result
  }

  public_network_access_enabled = var.environment == "dev" ? true : false

  private_endpoints = {
    default = {
      subnet_resource_id            = module.vnet.subnets["subnet0"].resource_id
      private_dns_zone_resource_ids = [module.pdns-kv.resource_id]
    }
  }

  tags = merge(local.tags, {
    "service_name" = var.key_vault_name
  })
}
