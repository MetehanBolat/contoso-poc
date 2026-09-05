#Requires -Version 7
<#
.SYNOPSIS
    Install or upgrade the Contoso Helm chart on minikube.

.EXAMPLE
    .\helm-install-local.ps1 -DockerHubUsername "myuser" -Version "v2.0.0" -PostgresPassword "Secret123!"

.EXAMPLE
    $env:DOCKERHUB_USERNAME = "myuser"
    $env:API_TAG = "v2.0.0"
    $env:POSTGRES_PASSWORD = "Secret123!"
    .\helm-install-local.ps1
#>
param(
    [string]$DockerHubUsername = $env:DOCKERHUB_USERNAME,
    [string]$Version = ($env:API_TAG ?? "latest"),
    [string]$PostgresPassword = $env:POSTGRES_PASSWORD,
    [string]$ReleaseName = "contoso",
    [string]$Namespace = "contoso-local",
    [string]$ChartPath = (Resolve-Path "$PSScriptRoot/../helm/contoso").Path
)

if (-not $DockerHubUsername) {
    throw "Please set the DOCKERHUB_USERNAME environment variable or pass -DockerHubUsername."
}
if (-not $PostgresPassword) {
    throw "Please set the POSTGRES_PASSWORD environment variable or pass -PostgresPassword."
}

$valuesTemplate = "$ChartPath/values-minikube.yaml"
$tempValues = [System.IO.Path]::GetTempFileName() + ".yaml"

try {
    $content = Get-Content $valuesTemplate -Raw
    $content = $content.Replace('__DOCKERHUB_USERNAME__', $DockerHubUsername)
    $content = $content.Replace('__API_TAG__', $Version)
    $content = $content.Replace('change-me', $PostgresPassword)
    Set-Content -Path $tempValues -Value $content -NoNewline
    Write-Host "Rendered temporary values file: $tempValues"

    Write-Host "Updating Helm dependencies ..."
    helm dependency build
    helm dependency update $ChartPath

    Write-Host "Installing/upgrading Helm release '$ReleaseName' in namespace '$Namespace' ..."
    helm upgrade --install $ReleaseName $ChartPath `
        -n $Namespace --create-namespace `
        -f $tempValues
} finally {
    Remove-Item $tempValues -ErrorAction SilentlyContinue
}

Write-Host "Done. Run 'kubectl get pods -n $Namespace' to watch the rollout."
