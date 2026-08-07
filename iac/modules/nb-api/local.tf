locals {
  tags = merge(var.tags, {
    instance    = "nb-api"
    environment = var.environment
    location    = var.location
    managedBy   = "terraform"
    deployedBy  = "MetehanBolat\\novabank-poc"
  })

  postgres_host                = "${var.postgres_server_name}.postgres.database.azure.com"
  postgres_database_name       = var.postgres_database_name
  postgres_user_secret_uri     = "https://${var.key_vault_name}.vault.azure.net/secrets/postgre-user"
  postgres_password_secret_uri = "https://${var.key_vault_name}.vault.azure.net/secrets/postgre-pass"
}
