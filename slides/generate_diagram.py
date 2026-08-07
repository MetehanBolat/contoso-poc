"""
Renders the NovaBank architecture diagram as a PNG, used as an image on the
"Proposed Architecture" slide of the presentation.

Regenerate with:
    python slides/generate_diagram.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.patches import FancyArrowPatch

ASSETS_DIR = Path(__file__).parent / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

NAVY = "#0B2545"
BLUE = "#1464F4"
LIGHT_BLUE = "#E8F0FE"
GREY = "#5C6470"
LIGHT_GREY = "#F2F3F5"
GREEN = "#1E9E6B"
WHITE = "#FFFFFF"


def box(ax, xy, w, h, text, fc=WHITE, ec=NAVY, fontsize=10, fontweight="normal",
        fontcolor=NAVY, lw=1.6, zorder=3, radius=0.07):
    x, y = xy
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={radius}",
        linewidth=lw, edgecolor=ec, facecolor=fc, zorder=zorder,
    ))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, fontweight=fontweight, color=fontcolor,
            zorder=zorder + 1, linespacing=1.5)


def region(ax, xy, w, h, title, ec, fc, title_color, fontsize=10.5):
    x, y = xy
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.09",
        linewidth=1.4, edgecolor=ec, facecolor=fc, zorder=0,
    ))
    ax.text(x + 0.22, y + h - 0.34, title, fontsize=fontsize, fontweight="bold", color=title_color, zorder=1)


def connector(ax, points, color=GREY, lw=1.6, ls="solid", zorder=2):
    """Draws a polyline through `points`, with an arrowhead only on the final segment."""
    for i in range(len(points) - 1):
        is_last = i == len(points) - 2
        style = "-|>" if is_last else "-"
        ax.add_patch(FancyArrowPatch(points[i], points[i + 1], arrowstyle=style, color=color,
                     linewidth=lw, mutation_scale=11, zorder=zorder, linestyle=ls,
                     shrinkA=0, shrinkB=0))


def tag(ax, xy, text, color=GREY, fontsize=8.0, fontweight="bold", ha="center"):
    ax.text(xy[0], xy[1], text, ha=ha, va="center", fontsize=fontsize, color=color,
            fontweight=fontweight, zorder=6, linespacing=1.3,
            bbox=dict(boxstyle="round,pad=0.16", fc=WHITE, ec="none", alpha=0.96))


fig, ax = plt.subplots(figsize=(14.2, 8.0), dpi=200)
ax.set_xlim(0, 14.2)
ax.set_ylim(0, 8.0)
ax.axis("off")

# ================= Left column: GitHub + customers =================
box(ax, (0.35, 6.5), 2.55, 1.05, "GitHub\n\nnovabank-poc repo", fc=LIGHT_GREY, ec=GREY, fontsize=10)
box(ax, (0.35, 4.85), 2.55, 1.15, "GitHub Actions\n\nOIDC login\n(no static secrets)",
    fc=WHITE, ec=BLUE, fontsize=9.3, fontcolor=BLUE, fontweight="bold")
connector(ax, [(1.625, 6.5), (1.625, 6.0)], color=GREY)

box(ax, (0.35, 0.55), 2.55, 1.1, "NovaBank\nCustomers", fc=LIGHT_GREY, ec=GREY, fontsize=10)

# ================= Azure outer region =================
region(ax, (3.35, 0.35), 10.5, 7.3, "", NAVY, WHITE, NAVY, fontsize=12)
ax.text(3.6, 7.44, "Azure Subscription — France Central (EU)", fontsize=12.2,
        fontweight="bold", color=NAVY, zorder=1)

# ACR — shared registry, outside the resource group
box(ax, (11.0, 6.05), 2.55, 0.95, "Azure Container\nRegistry (Premium)",
    fc=WHITE, ec=NAVY, fontsize=9, fontcolor=NAVY, fontweight="bold")

# Resource group region
region(ax, (3.65, 0.65), 6.9, 6.5, "", BLUE, LIGHT_BLUE, BLUE, fontsize=10.3)
ax.text(3.87, 6.83, "Environment Resource Group  (dev / prod)", fontsize=10.4,
        fontweight="bold", color=BLUE, zorder=1)

# VNet region
region(ax, (3.95, 3.35), 6.3, 3.3, "", GREY, WHITE, GREY, fontsize=9.3)
ax.text(4.15, 6.33, "Virtual Network", fontsize=9.3, fontweight="bold", color=GREY, zorder=1)

# App Service — full-width row inside VNet
box(ax, (4.25, 5.3), 5.75, 0.9, "App Service (Linux container)  ·  Managed Identity",
    fc=NAVY, ec=NAVY, fontsize=10, fontcolor=WHITE, fontweight="bold")

# Platform services row inside VNet
svc_y, svc_h = 3.55, 1.3
box(ax, (4.25, svc_y), 1.75, svc_h, "PostgreSQL\nFlexible\nServer", fc=WHITE, ec=GREEN,
    fontsize=8.6, fontcolor=GREEN, fontweight="bold")
box(ax, (6.25, svc_y), 1.75, svc_h, "Key Vault", fc=WHITE, ec=GREEN,
    fontsize=9, fontcolor=GREEN, fontweight="bold")
box(ax, (8.25, svc_y), 1.75, svc_h, "Container\nRegistry\n(private endpoint)",
    fc=WHITE, ec=GREEN, fontsize=8.4, fontcolor=GREEN, fontweight="bold")

# App Service -> each platform service (clean short verticals)
for cx in (5.125, 7.125, 9.125):
    connector(ax, [(cx, 5.3), (cx, svc_y + svc_h)], color=NAVY, lw=1.4)

# Observability row — inside RG, below VNet
box(ax, (3.95, 1.0), 3.3, 1.2, "Log Analytics Workspace\n365-day retention",
    fc=WHITE, ec=GREEN, fontsize=8.8, fontcolor=GREEN, fontweight="bold")
box(ax, (7.55, 1.0), 2.7, 1.2, "Application\nInsights",
    fc=WHITE, ec=GREEN, fontsize=9, fontcolor=GREEN, fontweight="bold")

# App Insights -> Log Analytics (short horizontal, in the gap between the two boxes)
connector(ax, [(7.55, 1.85), (7.25, 1.85)], color=GREY, lw=1.3, ls="dashed")
tag(ax, (6.35, 1.85), "logs & metrics", color=GREY, fontsize=7.0, fontweight="normal")

# App Service -> Application Insights (traces/deps/requests), routed in the
# clear vertical channel between the VNet edge (x=10.25) and the RG edge (x=10.55)
connector(ax, [(10.0, 5.6), (10.4, 5.6), (10.4, 1.6), (10.25, 1.6)], color=BLUE, lw=1.5)
tag(ax, (11.15, 3.6), "traces / deps\n/ requests", color=BLUE, fontsize=7.2)

# App Service -> ACR (pull image), routed above the service row, crossing the RG edge
connector(ax, [(10.0, 6.0), (10.4, 6.0), (10.4, 6.75), (11.0, 6.75)], color=NAVY, lw=1.4, ls="dotted")
tag(ax, (10.75, 6.98), "pull image\n(MI auth)", color=NAVY, fontsize=7.0)

# terraform apply — GitHub Actions -> Resource Group, in the gap between the
# Azure outer edge (x=3.35) and the RG edge (x=3.65)
connector(ax, [(2.9, 5.2), (3.5, 5.2), (3.5, 1.8), (3.95, 1.8)], color=BLUE, lw=1.9)
tag(ax, (3.5, 3.5), "terraform\napply", color=BLUE, fontsize=8.0)

# docker push — GitHub Actions -> ACR, routed above the Resource Group
connector(ax, [(2.2, 6.0), (2.2, 7.28), (12.27, 7.28), (12.27, 7.0)], color=BLUE, lw=1.9)
tag(ax, (8.0, 7.28), "docker push", color=BLUE, fontsize=8.2)

# HTTPS — Customers -> App Service, routed outside the Azure box then in
connector(ax, [(2.9, 1.1), (3.1, 1.1), (3.1, 5.6), (4.25, 5.6)], color=NAVY, lw=2.1)
tag(ax, (3.1, 3.3), "HTTPS", color=NAVY, fontsize=8.6)

fig.tight_layout(pad=0.4)
out_path = ASSETS_DIR / "architecture-diagram.png"
fig.savefig(out_path, facecolor="white")
print(f"Saved diagram to {out_path}")
