# Time Log

Rough overview of time spent on the NovaBank cloud proof-of-concept, per the assessment's submission guidelines.

| Date       | Area                   | Activity                                                                                                                                                                                                                                                     | Time Spent |
| ---------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- |
| 2026-08-07 | Infrastructure as Code | Designed and wrote the `nb-api` Terraform module (VNet/NSG, App Service + Plan, ACR, PostgreSQL Flexible Server, Key Vault, Log Analytics + App Insights, private DNS zones/endpoints) and the `dev`/`prod` instance configuration (`.tfvars`, `.tfbackend`) | 2h 00m     |
| 2026-08-07 | CI/CD Pipelines        | Built and tested the GitHub Actions workflows: container image build/push to ACR, Terraform plan (PR) and apply (main), OIDC federated login, end-to-end validation against dev                                                                              | 1h 00m     |
| 2026-08-07 | Documentation          | Wrote `architecture-summary.md`, `assumptions.md`, and the root `README.md`; aligned direction with CloudNation's 6D model                                                                                                                                   | 1h 00m     |

**Total logged: 4h 00m**

> This is a rough, self-reported breakdown as requested in the assignment (Section 7). It does not include time spent on the original assessment brief review or incidental context-switching.
