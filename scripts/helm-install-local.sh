#!/usr/bin/env bash
# Install or upgrade the Contoso Helm chart on minikube.
#
# Usage:
#   DOCKERHUB_USERNAME=myuser API_TAG=v2.0.0 POSTGRES_PASSWORD=Secret123! ./helm-install-local.sh
set -euo pipefail

DOCKERHUB_USERNAME="${DOCKERHUB_USERNAME:-}"
API_TAG="${API_TAG:-latest}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-}"
RELEASE_NAME="${RELEASE_NAME:-contoso}"
NAMESPACE="${NAMESPACE:-contoso-local}"
CHART_PATH="${CHART_PATH:-$(cd "$(dirname "$0")/../helm/contoso" && pwd)}"

if [ -z "$DOCKERHUB_USERNAME" ]; then
    echo "Set the DOCKERHUB_USERNAME environment variable." >&2
    exit 1
fi
if [ -z "$POSTGRES_PASSWORD" ]; then
    echo "Set the POSTGRES_PASSWORD environment variable." >&2
    exit 1
fi

VALUES_TEMPLATE="$CHART_PATH/values-minikube.yaml"
TEMP_VALUES=$(mktemp)
trap 'rm -f "$TEMP_VALUES"' EXIT

sed \
    -e "s|__DOCKERHUB_USERNAME__|$DOCKERHUB_USERNAME|g" \
    -e "s|__API_TAG__|$API_TAG|g" \
    -e "s#change-me#$POSTGRES_PASSWORD#g" \
    "$VALUES_TEMPLATE" > "$TEMP_VALUES"

echo "Updating Helm dependencies ..."
helm dependency update "$CHART_PATH"

echo "Installing/upgrading Helm release '$RELEASE_NAME' in namespace '$NAMESPACE' ..."
helm upgrade --install "$RELEASE_NAME" "$CHART_PATH" \
    -n "$NAMESPACE" --create-namespace \
    -f "$TEMP_VALUES"

echo "Done. Run 'kubectl get pods -n $NAMESPACE' to watch the rollout."
