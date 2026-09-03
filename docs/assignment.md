# Contoso Cloud Migration Brief

**To:** Senior Cloud Architect  
**From:** Contoso CTO & Head of Engineering  
**Date:** 14 November 2025  
**Subject:** First step to the public cloud for our customer portal API

---

## 1. Who we are and what we are trying to solve

Contoso runs a small customer portal API on a single on-premises VM. The database is a co-located PostgreSQL instance, logs are written to local files only, and there is no meaningful separation between development and production. Deployments are manual.

We are a regulated business with EU data residency requirements. Our leadership has approved a first, low-risk move to the public cloud and wants a pragmatic proposal that can be demonstrated end to end.

### Current state

- **Compute:** one VM running the customer portal API.
- **Data:** PostgreSQL running on the same VM.
- **Logging:** local files only — no central audit or incident trail.
- **Environments:** a single live environment; no dev/prod separation.
- **Deployment:** manual, console-based steps.

### Constraints and targets

- **Regulated industry (financial services)**; data must stay in the **EU**.
- **Availability target:** ≥ 99.9%.
- **Recovery targets:** RPO ≤ 1 hour, RTO ≤ 4 hours.
- **Auditability:** application and infrastructure logs retained centrally for ≥ 12 months, with access restricted to authorized roles.
- **Cost:** choices must be defensible to leadership; no over-engineering.

## 2. What we need from the first step

We want a working proof-of-concept that proves the cloud direction is sound, not a production system. The first step should deliver:

- At least **dev** and **prod** environments in the cloud (**Azure or AWS** — you choose and justify).
- **Repeatable, automated deployments** with no console click-ops.
- **Central logging** for application behaviour and infrastructure events, retained long enough to satisfy audit requirements.
- A **simple, clean footprint** — no Kubernetes, no multi-region active-active, no service mesh at this stage.
- A clear **cost and scaling rationale** that leadership can understand and defend.

> Keep the solution open and reasonable. Choose cloud services and patterns that fit the constraints above, and focus on explaining **why** your direction makes sense rather than listing every possible component.

## 3. Deliverables

### 3.1 Management summary (max 3 pages)

A concise document — readable by non-technical leadership — covering:

- Business context and objectives
- Proposed cloud direction, with one simple architecture diagram
- Key decisions, explicit trade-offs, assumptions, and risks
- Cost posture and scaling path

### 3.2 Cloud proof-of-concept

A minimal, working deployment in the chosen cloud using **Infrastructure as Code**:

- One API or function
- A basic managed data store
- Central logging / observability
- Clear, repeatable deployment steps (CLI script or a small CI example)

### 3.3 Presentation (15–20 minutes + short demo)

Present the direction and the PoC to Contoso's CTO and Head of Engineering. Include:

- The situation and why the proposed direction fits
- A walkthrough of the architecture
- Live demo: deploy or call the PoC and show the logs
- Trade-offs, risks, and next steps

### 3.4 Practical use of AI

Show where an LLM genuinely helps in a cloud/IaC workflow. Minimal working examples are fine — the point is to demonstrate how context is fed to a model and how the response is used. Examples:

- **AI IaC reviewer:** flag missing tags, unintentional public endpoints, or diagnostic gaps before apply.
- **AI architecture explainer:** turn the technical design into a one-page, non-technical rationale.
- **AI log insights helper:** summarize app/infra logs and suggest likely next diagnostic steps.

## 4. What good looks like

We expect a senior architect to show:

- **Consultative thinking:** stakeholders, constraints, trade-offs, and risks are treated as first-class inputs.
- **Clear cloud direction:** a defensible choice of cloud provider and services, with a business justification.
- **Clean, reproducible engineering:** IaC that can be reviewed, re-run, and extended; no one-off manual steps.
- **Practical AI use:** not a buzzword, but a tool that saves time or improves quality in a specific step.
- **Honest communication:** scope cuts are explicit, with a clear statement of what would come next with more time.

## 5. Suggested repository structure

Submit a Git repository with at least:

```
/docs/
  architecture-summary.md    # management summary: context, direction, diagram, assumptions, risks
  assumptions.md
  timelog.md                 # rough time breakdown per part
/iac/                        # Bicep / Terraform / CDK code
/ai/                         # AI helper + short README
/demo/README.md              # how to deploy and test the PoC
/slides/                     # optional presentation
```

## 6. Practical notes

- List any assumptions in `/docs/assumptions.md`.
- Keep costs reasonable: small SKUs, autoscaling where applicable, no over-engineering.
- Keep the solution specific to the business case, but avoid locking into a single tooling stack unless justified.
- Slides are optional but strongly recommended.

If scope has to be cut due to time, be explicit about what is deferred and what you would do next.
