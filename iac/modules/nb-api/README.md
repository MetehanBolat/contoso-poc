<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
| ---- | ------- |
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.15.8, < 2.0.0 |
| <a name="requirement_azurerm"></a> [azurerm](#requirement\_azurerm) | ~> 4.0 |
| <a name="requirement_random"></a> [random](#requirement\_random) | ~> 3.0 |

## Providers

| Name | Version |
| ---- | ------- |
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | ~> 4.0 |
| <a name="provider_random"></a> [random](#provider\_random) | ~> 3.0 |

## Modules

| Name | Source | Version |
| ---- | ------ | ------- |
| <a name="module_acr"></a> [acr](#module\_acr) | Azure/avm-res-containerregistry-registry/azurerm | 0.7.0 |
| <a name="module_app_service"></a> [app\_service](#module\_app\_service) | Azure/avm-res-web-site/azurerm | 0.22.0 |
| <a name="module_asp"></a> [asp](#module\_asp) | Azure/avm-res-web-serverfarm/azurerm | 2.0.8 |
| <a name="module_kv"></a> [kv](#module\_kv) | Azure/avm-res-keyvault-vault/azurerm | 0.10.2 |
| <a name="module_laws"></a> [laws](#module\_laws) | Azure/avm-res-operationalinsights-workspace/azurerm | 0.5.1 |
| <a name="module_nsg"></a> [nsg](#module\_nsg) | Azure/avm-res-network-networksecuritygroup/azurerm | 0.5.1 |
| <a name="module_pdns-acr"></a> [pdns-acr](#module\_pdns-acr) | Azure/avm-res-network-privatednszone/azurerm | 0.3.2 |
| <a name="module_pdns-kv"></a> [pdns-kv](#module\_pdns-kv) | Azure/avm-res-network-privatednszone/azurerm | 0.3.2 |
| <a name="module_pdns-laws"></a> [pdns-laws](#module\_pdns-laws) | Azure/avm-res-network-privatednszone/azurerm | 0.3.2 |
| <a name="module_pdns-laws-ods"></a> [pdns-laws-ods](#module\_pdns-laws-ods) | Azure/avm-res-network-privatednszone/azurerm | 0.3.2 |
| <a name="module_pdns-laws-oms"></a> [pdns-laws-oms](#module\_pdns-laws-oms) | Azure/avm-res-network-privatednszone/azurerm | 0.3.2 |
| <a name="module_pdns-psql"></a> [pdns-psql](#module\_pdns-psql) | Azure/avm-res-network-privatednszone/azurerm | 0.3.2 |
| <a name="module_psql"></a> [psql](#module\_psql) | Azure/avm-res-dbforpostgresql-flexibleserver/azurerm | 0.2.3 |
| <a name="module_vnet"></a> [vnet](#module\_vnet) | Azure/avm-res-network-virtualnetwork/azurerm | 0.19.0 |

## Resources

| Name | Type |
| ---- | ---- |
| [azurerm_application_insights.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/application_insights) | resource |
| [azurerm_resource_group.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/resource_group) | resource |
| [azurerm_user_assigned_identity.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/user_assigned_identity) | resource |
| [random_password.postgres_admin](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/password) | resource |
| [azurerm_client_config.current](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/client_config) | data source |

## Inputs

| Name | Description | Type | Default | Required |
| ---- | ----------- | ---- | ------- | :------: |
| <a name="input_app_service_container_image"></a> [app\_service\_container\_image](#input\_app\_service\_container\_image) | The container image reference for the App Service. Use the ACR login server prefix for private registry images. | `string` | `"mcr.microsoft.com/azuredocs/aci-helloworld:latest"` | no |
| <a name="input_app_service_name"></a> [app\_service\_name](#input\_app\_service\_name) | The name of the container-based App Service. | `string` | n/a | yes |
| <a name="input_app_service_plan_name"></a> [app\_service\_plan\_name](#input\_app\_service\_plan\_name) | The name of the App Service plan. | `string` | n/a | yes |
| <a name="input_app_service_plan_sku_name"></a> [app\_service\_plan\_sku\_name](#input\_app\_service\_plan\_sku\_name) | The SKU name of the App Service plan. Use a consumption plan such as Y1 for the cheapest option. | `string` | n/a | yes |
| <a name="input_app_subnet_address_space"></a> [app\_subnet\_address\_space](#input\_app\_subnet\_address\_space) | The address space for the application subnet. | `string` | n/a | yes |
| <a name="input_app_subnet_name"></a> [app\_subnet\_name](#input\_app\_subnet\_name) | The name of the application subnet. | `string` | n/a | yes |
| <a name="input_application_insights_name"></a> [application\_insights\_name](#input\_application\_insights\_name) | The name of the Azure Application Insights resource. | `string` | n/a | yes |
| <a name="input_container_registry_name"></a> [container\_registry\_name](#input\_container\_registry\_name) | The name of the Azure Container Registry. | `string` | n/a | yes |
| <a name="input_container_registry_sku"></a> [container\_registry\_sku](#input\_container\_registry\_sku) | The SKU of the Azure Container Registry. | `string` | `"Basic"` | no |
| <a name="input_environment"></a> [environment](#input\_environment) | The environment for the resources. | `string` | n/a | yes |
| <a name="input_identity_name"></a> [identity\_name](#input\_identity\_name) | The name of the user-assigned managed identity. | `string` | n/a | yes |
| <a name="input_key_vault_name"></a> [key\_vault\_name](#input\_key\_vault\_name) | The name of the Key Vault. | `string` | n/a | yes |
| <a name="input_location"></a> [location](#input\_location) | The location where the resource group will be created. | `string` | n/a | yes |
| <a name="input_log_analytics_workspace_name"></a> [log\_analytics\_workspace\_name](#input\_log\_analytics\_workspace\_name) | The name of the Log Analytics workspace. | `string` | n/a | yes |
| <a name="input_nsg_name"></a> [nsg\_name](#input\_nsg\_name) | The name of the network security group. | `string` | n/a | yes |
| <a name="input_pe_subnet_address_space"></a> [pe\_subnet\_address\_space](#input\_pe\_subnet\_address\_space) | The address space for the private endpoint subnet. | `string` | n/a | yes |
| <a name="input_pe_subnet_name"></a> [pe\_subnet\_name](#input\_pe\_subnet\_name) | The name of the private endpoint subnet. | `string` | n/a | yes |
| <a name="input_postgres_admin_login"></a> [postgres\_admin\_login](#input\_postgres\_admin\_login) | The administrator login for the PostgreSQL Flexible Server. | `string` | `"psqladmin"` | no |
| <a name="input_postgres_database_name"></a> [postgres\_database\_name](#input\_postgres\_database\_name) | The name of the PostgreSQL database. | `string` | n/a | yes |
| <a name="input_postgres_server_name"></a> [postgres\_server\_name](#input\_postgres\_server\_name) | The name of the PostgreSQL Flexible Server. | `string` | n/a | yes |
| <a name="input_postgres_server_sku"></a> [postgres\_server\_sku](#input\_postgres\_server\_sku) | The SKU of the PostgreSQL Flexible Server. | `string` | n/a | yes |
| <a name="input_resource_group_name"></a> [resource\_group\_name](#input\_resource\_group\_name) | The name of the resource group. | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | A map of tags to assign to the resources. | `map(string)` | `{}` | no |
| <a name="input_vnet_address_space"></a> [vnet\_address\_space](#input\_vnet\_address\_space) | The address space for the virtual network. | `string` | n/a | yes |
| <a name="input_vnet_name"></a> [vnet\_name](#input\_vnet\_name) | The name of the virtual network. | `string` | n/a | yes |

## Outputs

| Name | Description |
| ---- | ----------- |
| <a name="output_app_service_default_hostname"></a> [app\_service\_default\_hostname](#output\_app\_service\_default\_hostname) | n/a |
| <a name="output_app_service_id"></a> [app\_service\_id](#output\_app\_service\_id) | n/a |
| <a name="output_app_service_name"></a> [app\_service\_name](#output\_app\_service\_name) | n/a |
| <a name="output_app_service_plan_id"></a> [app\_service\_plan\_id](#output\_app\_service\_plan\_id) | n/a |
| <a name="output_app_service_plan_name"></a> [app\_service\_plan\_name](#output\_app\_service\_plan\_name) | n/a |
| <a name="output_container_registry_id"></a> [container\_registry\_id](#output\_container\_registry\_id) | n/a |
| <a name="output_container_registry_login_server"></a> [container\_registry\_login\_server](#output\_container\_registry\_login\_server) | n/a |
| <a name="output_container_registry_name"></a> [container\_registry\_name](#output\_container\_registry\_name) | n/a |
| <a name="output_identity_id"></a> [identity\_id](#output\_identity\_id) | n/a |
| <a name="output_identity_name"></a> [identity\_name](#output\_identity\_name) | n/a |
| <a name="output_identity_principal_id"></a> [identity\_principal\_id](#output\_identity\_principal\_id) | n/a |
| <a name="output_key_vault_id"></a> [key\_vault\_id](#output\_key\_vault\_id) | n/a |
| <a name="output_key_vault_name"></a> [key\_vault\_name](#output\_key\_vault\_name) | n/a |
| <a name="output_log_analytics_workspace_id"></a> [log\_analytics\_workspace\_id](#output\_log\_analytics\_workspace\_id) | n/a |
| <a name="output_log_analytics_workspace_key"></a> [log\_analytics\_workspace\_key](#output\_log\_analytics\_workspace\_key) | n/a |
| <a name="output_log_analytics_workspace_name"></a> [log\_analytics\_workspace\_name](#output\_log\_analytics\_workspace\_name) | n/a |
| <a name="output_nsg_id"></a> [nsg\_id](#output\_nsg\_id) | n/a |
| <a name="output_nsg_name"></a> [nsg\_name](#output\_nsg\_name) | n/a |
| <a name="output_postgresql_admin_password"></a> [postgresql\_admin\_password](#output\_postgresql\_admin\_password) | n/a |
| <a name="output_postgresql_server_id"></a> [postgresql\_server\_id](#output\_postgresql\_server\_id) | n/a |
| <a name="output_postgresql_server_name"></a> [postgresql\_server\_name](#output\_postgresql\_server\_name) | n/a |
| <a name="output_resource_group_id"></a> [resource\_group\_id](#output\_resource\_group\_id) | n/a |
| <a name="output_resource_group_name"></a> [resource\_group\_name](#output\_resource\_group\_name) | n/a |
| <a name="output_vnet_address_space"></a> [vnet\_address\_space](#output\_vnet\_address\_space) | n/a |
| <a name="output_vnet_id"></a> [vnet\_id](#output\_vnet\_id) | n/a |
| <a name="output_vnet_name"></a> [vnet\_name](#output\_vnet\_name) | n/a |
<!-- END_TF_DOCS -->