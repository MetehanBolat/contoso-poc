# Contoso Helm chart

This chart deploys the **Contoso API** together with a **highly-available PostgreSQL** cluster (via the Bitnami `postgresql-ha` chart) on Kubernetes.

It is configured out of the box for local minikube development, but the same chart can be reused for other environments by supplying different `values-*.yaml` files.

## What's included

- **Contoso API** Deployment with 2 replicas, Service, HPA, PDB, ServiceAccount, ConfigMap and Secret.
- **PostgreSQL HA** from the `bitnami/postgresql-ha` dependency:
  - 2 PostgreSQL replicas with streaming replication (repmgr).
  - Pgpool-II connection pooler as the entry point for the API.
  - Persistent storage and automatic failover.

## Prerequisites

- Kubernetes cluster (minikube is used for local dev).
- `kubectl` configured for the cluster.
- [Helm 3](https://helm.sh/docs/intro/install/) installed.
- Docker installed and logged into Docker Hub.

## Quick start (minikube)

### 1. Build and push the API image

Use the helper scripts in `scripts/`:

```powershell
$env:DOCKERHUB_USERNAME = "your-dockerhub-username"
.\scripts\build-and-push.ps1 -Version "v2.0.0"
```

or with Bash:

```bash
export DOCKERHUB_USERNAME=your-dockerhub-username
./scripts/build-and-push.sh
# or
VERSION=v2.0.0 ./scripts/build-and-push.sh
```

### 2. Install the chart

```powershell
.\scripts\helm-install-local.ps1 -DockerHubUsername "your-dockerhub-username" -Version "v2.0.0"
```

or with Bash:

```bash
./scripts/helm-install-local.sh your-dockerhub-username v2.0.0
```

The scripts:

1. Run `helm dependency update` to download `postgresql-ha`.
2. Substitute your Docker Hub username/tag into `values-minikube.yaml`.
3. Install/upgrade the release in the `contoso-local` namespace.

### 3. Verify

```bash
kubectl get pods -n contoso-local -w
kubectl get hpa -n contoso-local
```

You should see:

- 2 API pods (`contoso-api-*`)
- 2 PostgreSQL pods (`postgres-postgresql-*`)
- 1 Pgpool pod (`postgres-pgpool-*`)

### 4. Access the API

```bash
minikube service contoso-api -n contoso-local
```

Then test:

- `http://<url>/health`
- `http://<url>/dbtest`
- `http://<url>/logs`

## Configuration

The main values file is `values.yaml`. Minikube-specific overrides are in `values-minikube.yaml`.

Key settings:

| Value | Description |
|-------|-------------|
| `image.repository` / `image.tag` | API image to deploy. |
| `replicaCount` / `autoscaling` | API replicas and HPA settings. |
| `postgresql.host` | Pgpool-II service DNS name (default `postgres-pgpool`). |
| `global.postgresql.password` | Password used by both the API and the HA PostgreSQL cluster. |
| `postgresql-ha.postgresql.replicaCount` | Number of PostgreSQL replicas. |
| `postgresql-ha.pgpool.replicaCount` | Number of Pgpool-II pods. |

### Change the database password

Edit `global.postgresql.password` in `values-minikube.yaml` (or pass `--set global.postgresql.password=...`). The same password is used for the API connection and the HA cluster.

## Private Docker Hub repositories

If your API image is in a private Docker Hub repo, create a pull secret and reference it in `values-minikube.yaml`:

```yaml
image:
  pullSecrets:
    - name: dockerhub-regcred
```

Create the secret:

```bash
kubectl create secret docker-registry dockerhub-regcred \
  --docker-server=docker.io \
  --docker-username=<your-username> \
  --docker-password=<your-token> \
  -n contoso-local
```

## Uninstall

```bash
helm uninstall contoso -n contoso-local
kubectl delete namespace contoso-local
```

## Notes

- `POSTGRES_SSLMODE` is set to `disable` for local minikube only. Do not use this in production.
- The HPA requires the metrics-server addon in minikube:
  ```bash
  minikube addons enable metrics-server
  ```
- The PostgreSQL `initdbScripts` create the `app_log` table automatically on first initialization.
