#Requires -Version 7
<#
.SYNOPSIS
    Build the Contoso API container image with Docker and push it to Docker Hub.

.EXAMPLE
    .\build-and-push.ps1 -DockerHubUsername "myuser" -Version "v2.0.0"

.EXAMPLE
    $env:DOCKERHUB_USERNAME = "myuser"
    .\build-and-push.ps1
#>
param(
    [string]$DockerHubUsername = $env:DOCKERHUB_USERNAME,
    [string]$Version = "latest",
    [string]$SourceFolder = (Resolve-Path "$PSScriptRoot/../src/new-api").Path
)

if (-not $DockerHubUsername) {
    throw "Please set the DOCKERHUB_USERNAME environment variable or pass -DockerHubUsername."
}

$image = "$DockerHubUsername/contoso-api:$Version"
$latest = "$DockerHubUsername/contoso-api:latest"

Write-Host "Building $image with Docker ..."
docker build -t $image -f "$SourceFolder/Dockerfile" "$SourceFolder"
docker tag $image $latest

Write-Host "Pushing images to Docker Hub ..."
docker login docker.io

docker push $image
docker push $latest

Write-Host "Done. Image pushed: $image"
