#!/usr/bin/env bash
# Build the Contoso API container image with Docker and push it to Docker Hub.
#
# Usage:
#   DOCKERHUB_USERNAME=myuser VERSION=v2.0.0 ./build-and-push.sh
set -euo pipefail

DOCKERHUB_USERNAME="${DOCKERHUB_USERNAME:-}"
VERSION="${VERSION:-latest}"
SOURCE_FOLDER="${SOURCE_FOLDER:-$(cd "$(dirname "$0")/../src/new-api" && pwd)}"

if [ -z "$DOCKERHUB_USERNAME" ]; then
    echo "Set the DOCKERHUB_USERNAME environment variable." >&2
    exit 1
fi

IMAGE="$DOCKERHUB_USERNAME/contoso-api:$VERSION"
LATEST="$DOCKERHUB_USERNAME/contoso-api:latest"

echo "Building $IMAGE with Docker ..."
docker build -t "$IMAGE" -f "$SOURCE_FOLDER/Dockerfile" "$SOURCE_FOLDER"
docker tag "$IMAGE" "$LATEST"

echo "Pushing images to Docker Hub ..."
docker login docker.io

docker push "$IMAGE"
docker push "$LATEST"

echo "Done. Image pushed: $IMAGE"
