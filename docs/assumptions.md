- [Assumptions](#assumptions)
  - [Application \& Data](#application--data)
  - [Networking](#networking)
  - [Environments \& Operations](#environments--operations)
  - [Identity, Security \& Cost](#identity-security--cost)


# Assumptions

This document lists the assumptions made while designing and building the Contoso cloud proof-of-concept. Where an assumption materially affects risk, cost, or architecture, the corresponding trade-off is also referenced in [`architecture-summary.md`](./architecture-summary.md).

## Application & Data

- **The application is stateless.** The API keeps no session or file-based state on local disk; all persistent state lives in PostgreSQL. This allows App Service instances to be freely restarted, scaled, or replaced without a sticky-session or shared-storage requirement.
- Current data volumes and transaction rates are low enough that a single-node PostgreSQL Flexible Server (with zone-redundant HA in prod) satisfies the availability target, rather than requiring a distributed/multi-region database from day one.
- The existing on-prem PostgreSQL schema can be migrated as-is (lift of the data model), with no immediate need for schema redesign.
- No PII/regulated customer data is loaded into the **dev** environment; dev uses synthetic or anonymized data only, consistent with dev's more permissive network posture.

## Networking

- **No intranet/on-premises connectivity is required.** Contoso does not need a site-to-site VPN, ExpressRoute, or private hybrid link back to their existing on-prem environment for this first step — the API and database are fully cloud-native and reachable over the public internet (App Service) or via Azure-internal private endpoints (data plane). This lets the PoC avoid a VPN gateway/ExpressRoute circuit and its associated cost and lead time.
- **Contoso has provided the Azure virtual network address ranges to use.** The `10.250.250.0/24` (dev) and `10.250.100.0/24` (prod) ranges are assumed to be allocated/reserved by Contoso specifically for this workload and do not overlap with any other Contoso Azure or on-prem network — so no further IP address management (IPAM) coordination is required before deployment.
- A single VNet per environment, with two subnets (private endpoints + delegated app subnet), is sufficient; no hub-spoke topology or shared connectivity subscription exists yet for this workload to peer into.
- Public inbound access to the App Service endpoint (HTTPS only) is acceptable for this first step in both environments; a WAF/Front Door layer is deferred (see Next Steps in the architecture summary).

## Environments & Operations

- **Dev** and **prod** are sufficient as the first two environments; a dedicated **test/staging** tier is not required immediately but is expected to be added later without redesigning the module.
- Contoso will operate out of a single Azure subscription for this PoC; multi-subscription governance (management groups, landing zone) is out of scope for this first step.
- The team accepts **France Central** as the sole deployment region to satisfy EU data residency; multi-region disaster recovery is not required for this first step, provided backups/HA meet the RPO ≤ 1h / RTO ≤ 4h target within-region.
- Central log retention of 365 days in Log Analytics/Application Insights is an acceptable interpretation of the "≥ 12 months" audit requirement, with access restricted via Azure RBAC on the workspace.

## Identity, Security & Cost

- Azure AD (Entra ID) is the identity provider for CI/CD (GitHub OIDC federation) and for managed identities used by App Service to reach ACR, Key Vault, and PostgreSQL — no separate secrets manager or third-party IdP is required.
- Contoso leadership accepts the small/burstable SKUs chosen (App Service `P0v3`, PostgreSQL `B_Standard_B1ms` dev / `GP_Standard_D2s_v3` prod) as adequate for current load, understanding that vertical tier upgrades are the primary scaling lever.
- No formal compliance certification (e.g. ISO 27001, SOC 2 attestation of the Azure environment itself) is required as part of this PoC; Azure's own compliance posture is assumed sufficient for a first step, with a fuller compliance review expected before go-live with real customer data.
