"""
Generates the Contoso Cloud Foundation interview presentation as a native
OpenDocument Presentation (.odp) file, using odfpy.

Why a script instead of a binary checked into git:
  - The deck is fully reproducible and diffable (content lives in Python, not
    inside a zipped binary).
  - Anyone can regenerate slides/contoso-cloud-foundation.odp after editing
    this file or docs/architecture-summary.md, without opening an editor.

Usage:
    python slides/generate_presentation.py

Output:
    slides/contoso-cloud-foundation.odp   (opens in LibreOffice Impress,
    OpenOffice Impress, and also imports cleanly into PowerPoint/Google Slides)
"""

from __future__ import annotations

from pathlib import Path

from odf.opendocument import OpenDocumentPresentation
from odf.style import (
    GraphicProperties,
    MasterPage,
    PageLayout,
    PageLayoutProperties,
    ParagraphProperties,
    Style,
    TextProperties,
)
from odf.draw import Frame, Image, Page, TextBox
from odf.text import P, ListItem, List as TextList, LineBreak
from odf.presentation import Notes

SLIDES_DIR = Path(__file__).parent
ASSETS_DIR = SLIDES_DIR / "assets"
OUTPUT_PATH = SLIDES_DIR / "contoso-cloud-foundation.odp"
DIAGRAM_PATH = ASSETS_DIR / "architecture-diagram.png"

# ---------------------------------------------------------------------------
# Palette (matches docs / diagram)
# ---------------------------------------------------------------------------
NAVY = "#0B2545"
BLUE = "#1464F4"
GREEN = "#1E9E6B"
GREY = "#5C6470"
LIGHT_GREY = "#F2F3F5"
LIGHT_BLUE = "#E8F0FE"
WHITE = "#FFFFFF"
RED = "#C0392B"

# 16:9 slide, standard Impress size in cm
PAGE_W = 28.0
PAGE_H = 15.75

doc = OpenDocumentPresentation()

# ---------------------------------------------------------------------------
# Page layout + master page (required by the ODF presentation schema)
# ---------------------------------------------------------------------------
page_layout = PageLayout(name="PL1")
page_layout.addElement(PageLayoutProperties(pagewidth=f"{PAGE_W}cm", pageheight=f"{PAGE_H}cm",
                                             printorientation="landscape"))
doc.automaticstyles.addElement(page_layout)

master_page = MasterPage(name="Default", pagelayoutname=page_layout)
doc.masterstyles.addElement(master_page)


# ---------------------------------------------------------------------------
# Reusable style helpers
# ---------------------------------------------------------------------------
_style_counter = 0


def _next_name(prefix: str) -> str:
    global _style_counter
    _style_counter += 1
    return f"{prefix}{_style_counter}"


def add_text_style(color=NAVY, size="18pt", bold=False, italic=False, align="left") -> Style:
    name = _next_name("PT")
    style = Style(name=name, family="paragraph")
    style.addElement(ParagraphProperties(textalign=align))
    style.addElement(TextProperties(color=color, fontsize=size,
                                     fontweight="bold" if bold else "normal",
                                     fontstyle="italic" if italic else "normal",
                                     fontfamily="Calibri"))
    doc.styles.addElement(style)
    return style


def add_frame_style(fill_color=None, stroke_color=None, stroke_width="0.03cm", vertical="middle") -> Style:
    name = _next_name("GR")
    style = Style(name=name, family="graphic")
    gp_kwargs = dict(textareaverticalalign=vertical)
    if fill_color:
        gp_kwargs["fill"] = "solid"
        gp_kwargs["fillcolor"] = fill_color
    else:
        gp_kwargs["fill"] = "none"
    if stroke_color:
        gp_kwargs["stroke"] = "solid"
        gp_kwargs["strokecolor"] = stroke_color
        gp_kwargs["strokewidth"] = stroke_width
    else:
        gp_kwargs["stroke"] = "none"
    style.addElement(GraphicProperties(**gp_kwargs))
    doc.styles.addElement(style)
    return style


def new_page(name: str) -> Page:
    page = Page(masterpagename=master_page, name=name)
    doc.presentation.addElement(page)
    return page


def add_textbox(page: Page, x, y, w, h, lines, text_style, frame_style=None, name="tb"):
    """lines: list[str] (each becomes a <text:p>) or list of (text, style) for mixed styling."""
    frame = Frame(width=f"{w}cm", height=f"{h}cm", x=f"{x}cm", y=f"{y}cm",
                  name=_next_name(name))
    if frame_style:
        frame.setAttribute("stylename", frame_style)
    box = TextBox()
    for line in lines:
        p = P(stylename=text_style, text=line)
        box.addElement(p)
    frame.addElement(box)
    page.addElement(frame)
    return frame


def add_bullets(page: Page, x, y, w, h, bullets, text_style, frame_style=None, name="bul", gap_style=None):
    """bullets: list[str] top-level bullets, or list[(str, [sub-bullets])]."""
    frame = Frame(width=f"{w}cm", height=f"{h}cm", x=f"{x}cm", y=f"{y}cm",
                  name=_next_name(name))
    if frame_style:
        frame.setAttribute("stylename", frame_style)
    box = TextBox()
    tlist = TextList()
    for item in bullets:
        if isinstance(item, tuple):
            text, subs = item
        else:
            text, subs = item, None
        li = ListItem()
        li.addElement(P(stylename=text_style, text=text))
        if subs:
            sub_list = TextList()
            sub_style = gap_style or text_style
            for s in subs:
                sli = ListItem()
                sli.addElement(P(stylename=sub_style, text=s))
                sub_list.addElement(sli)
            li.addElement(sub_list)
        tlist.addElement(li)
    box.addElement(tlist)
    frame.addElement(box)
    page.addElement(frame)
    return frame


def add_image(page: Page, path: Path, x, y, w, h, name="img"):
    frame = Frame(width=f"{w}cm", height=f"{h}cm", x=f"{x}cm", y=f"{y}cm",
                  name=_next_name(name))
    img = Image(href=doc.addPicture(str(path)), type="simple", show="embed", actuate="onLoad")
    frame.addElement(img)
    page.addElement(frame)
    return frame


def add_rect_frame(page: Page, x, y, w, h, frame_style, name="rect"):
    frame = Frame(width=f"{w}cm", height=f"{h}cm", x=f"{x}cm", y=f"{y}cm",
                  name=_next_name(name))
    frame.setAttribute("stylename", frame_style)
    box = TextBox()
    frame.addElement(box)
    page.addElement(frame)
    return frame


def add_notes(page: Page, text: str):
    """Adds speaker notes to a slide (visible in Impress' Notes view)."""
    notes = Notes()
    frame = Frame(width="24cm", height="10cm", x="2cm", y="2cm")
    box = TextBox()
    for line in text.strip().split("\n"):
        box.addElement(P(text=line))
    frame.addElement(box)
    notes.addElement(frame)
    page.addElement(notes)


# ---------------------------------------------------------------------------
# Shared styles
# ---------------------------------------------------------------------------
st_title = add_text_style(color=NAVY, size="32pt", bold=True)
st_subtitle = add_text_style(color=BLUE, size="18pt", bold=False)
st_kicker = add_text_style(color=BLUE, size="14pt", bold=True)
st_slide_title = add_text_style(color=NAVY, size="24pt", bold=True)
st_body = add_text_style(color=NAVY, size="15pt")
st_body_sm = add_text_style(color=GREY, size="12.5pt")
st_footer = add_text_style(color=GREY, size="10pt")
st_white_bold = add_text_style(color=WHITE, size="14pt", bold=True, align="center")
st_white = add_text_style(color=WHITE, size="12pt", align="center")
st_stat_num = add_text_style(color=NAVY, size="30pt", bold=True, align="center")
st_stat_label = add_text_style(color=GREY, size="11pt", align="center")
st_green_bold = add_text_style(color=GREEN, size="13pt", bold=True)
st_red_bold = add_text_style(color=RED, size="13pt", bold=True)
st_section_title = add_text_style(color=WHITE, size="30pt", bold=True, align="center")
st_section_sub = add_text_style(color="#B9CBEF", size="15pt", align="center")

fs_navy_card = add_frame_style(fill_color=NAVY, vertical="middle")
fs_blue_card = add_frame_style(fill_color=BLUE, vertical="middle")
fs_green_card = add_frame_style(fill_color="#E7F6EE", stroke_color=GREEN, vertical="middle")
fs_grey_card = add_frame_style(fill_color=LIGHT_GREY, stroke_color=GREY, vertical="top")
fs_lightblue_card = add_frame_style(fill_color=LIGHT_BLUE, stroke_color=BLUE, vertical="top")
fs_plain = add_frame_style(vertical="top")
fs_section_bg = add_frame_style(fill_color=NAVY, vertical="middle")
fs_line = add_frame_style(fill_color=BLUE, vertical="top")
fs_white_card = add_frame_style(fill_color=WHITE, stroke_color=GREY, vertical="top")


def footer(page: Page, slide_no: int, total: int, label: str = "Contoso Cloud Foundation"):
    add_textbox(page, 1.0, PAGE_H - 0.9, 16.0, 0.6, [f"{label}"], st_footer, name="ftr")
    add_textbox(page, PAGE_W - 4.0, PAGE_H - 0.9, 3.0, 0.6, [f"{slide_no} / {total}"], st_footer, name="pgn")


def divider(page: Page, x, y, w, h=0.06):
    add_rect_frame(page, x, y, w, h, fs_line, name="div")


TOTAL_SLIDES = 12

# ===========================================================================
# Slide 1 — Title
# ===========================================================================
p1 = new_page("Title")
add_rect_frame(p1, 0, 0, PAGE_W, PAGE_H, fs_navy_card, name="bg")
add_textbox(p1, 2.0, 5.0, 24.0, 1.0, ["CONTOSO CLOUD FOUNDATION"], st_kicker, name="kicker")
_kicker_style = add_text_style(color="#7FB2FF", size="15pt", bold=True)
add_textbox(p1, 2.0, 5.0, 24.0, 1.0, ["CONTOSO CLOUD FOUNDATION"], _kicker_style, name="kicker2")
_title_white = add_text_style(color=WHITE, size="38pt", bold=True)
add_textbox(p1, 2.0, 5.8, 24.0, 2.5, [
    "A pragmatic first step to Azure",
], _title_white, name="title")
_sub_white = add_text_style(color="#C9D6EE", size="16pt")
add_textbox(p1, 2.0, 7.6, 22.0, 1.0, [
    "Proof-of-concept, architecture direction & Terraform IaC — prepared for Contoso's CTO & Head of Engineering",
], _sub_white, name="subtitle")
add_rect_frame(p1, 2.0, 9.0, 4.0, 0.06, fs_line, name="rule")
_footer_white = add_text_style(color="#8FA0C4", size="11pt")
add_textbox(p1, 2.0, 13.6, 20.0, 0.8, ["7 August 2026"], _footer_white, name="presenter")

# ===========================================================================
# Slide 2 — Agenda
# ===========================================================================
p2 = new_page("Agenda")
add_textbox(p2, 1.2, 0.7, 20.0, 1.0, ["Agenda"], st_slide_title, name="t")
divider(p2, 1.25, 1.75, 3.0)

agenda_items = [
    ("01", "The situation at Contoso", "Where the portal runs today, and why it matters for a bank"),
    ("02", "Why Azure, why PaaS-first", "The direction, and the alternatives we ruled out"),
    ("03", "Architecture walkthrough", "Compute, data, identity, network, observability"),
    ("04", "Infrastructure as Code & CI/CD", "Terraform module design, dev/prod isolation, GitHub Actions"),
    ("05", "Live demo", "Deploy, call the API, tail the logs"),
    ("06", "AI in the workflow", "Where an LLM genuinely helps, and where it doesn't"),
    ("07", "Trade-offs, risks & next steps", "What we'd do with more time, and why we didn't do it now"),
]
y = 2.4
row_h = 1.55
for num, title, desc in agenda_items:
    add_rect_frame(p2, 1.2, y, 1.3, row_h - 0.15, fs_lightblue_card, name="num_bg")
    add_textbox(p2, 1.2, y, 1.3, row_h - 0.15, [num], add_text_style(color=BLUE, size="20pt", bold=True, align="center"), name="num")
    add_textbox(p2, 2.8, y + 0.05, 22.0, 0.6, [title], add_text_style(color=NAVY, size="15pt", bold=True), name="atitle")
    add_textbox(p2, 2.8, y + 0.65, 22.0, 0.6, [desc], st_body_sm, name="adesc")
    y += row_h
footer(p2, 2, TOTAL_SLIDES)

# ===========================================================================
# Slide 3 — The situation at Contoso (Discover)
# ===========================================================================
p3 = new_page("Situation")
add_textbox(p3, 1.2, 0.7, 20.0, 1.0, ["The situation at Contoso"], st_slide_title, name="t")
add_textbox(p3, 1.2, 1.5, 22.0, 0.6, ["Discover"], st_subtitle, name="s")
divider(p3, 1.25, 2.3, 3.0)

add_textbox(p3, 1.2, 2.7, 12.0, 0.6, ["Today"], add_text_style(color=RED, size="15pt", bold=True), name="today_h")
today_items = [
    "One VM running the customer portal API",
    "PostgreSQL co-located on the same VM",
    "Logs written to local files only — no central audit trail",
    "A single environment: no dev/test/prod separation",
    "Deployments are manual (\"click-ops\")",
]
add_bullets(p3, 1.2, 3.4, 12.5, 6.0, today_items, st_body, name="today")

add_textbox(p3, 14.5, 2.7, 12.0, 0.6, ["Constraints we must respect"], add_text_style(color=BLUE, size="15pt", bold=True), name="constraints_h")
constraint_items = [
    "Regulated industry (financial services) — EU data residency",
    "Availability ≥ 99.9%",
    "RPO ≤ 1 hour  ·  RTO ≤ 4 hours",
    "Application + infrastructure logs retained centrally ≥ 12 months, access-restricted",
    "Cost must be defensible to leadership",
]
add_bullets(p3, 14.5, 3.4, 12.5, 6.0, constraint_items, st_body, name="constraints")

add_rect_frame(p3, 1.2, 10.2, 25.6, 1.9, fs_grey_card, name="risk_box")
add_textbox(p3, 1.6, 10.45, 24.8, 0.5, ["Why this matters"], add_text_style(color=NAVY, size="13pt", bold=True), name="risk_h")
add_textbox(p3, 1.6, 10.95, 24.8, 1.0, [
    "No environment separation + no central logging = limited incident-response capability and audit risk for a regulated bank."
], st_body_sm, name="risk_body")
footer(p3, 3, TOTAL_SLIDES)

# ===========================================================================
# Slide 4 — Why Azure, why PaaS-first (Define & Design)
# ===========================================================================
p4 = new_page("Direction")
add_textbox(p4, 1.2, 0.7, 20.0, 1.0, ["Why Azure, why PaaS-first"], st_slide_title, name="t")
add_textbox(p4, 1.2, 1.5, 22.0, 0.6, ["Define & Design"], st_subtitle, name="s")
divider(p4, 1.25, 2.3, 3.0)

add_textbox(p4, 1.2, 2.7, 25.0, 0.9, [
    "Recommendation: a single-region, PaaS-first \u201cmodernize-while-moving\u201d pattern on Microsoft Azure — not a VM lift-and-shift, not Kubernetes."
], add_text_style(color=NAVY, size="15.5pt", bold=True), name="thesis")

cols = [
    ("Considered", GREY, [
        "VM lift-and-shift (IaaS)",
        "AKS / container orchestration",
        "Multi-region active-active",
        "Full landing zone (policy, hub-spoke) on day one",
    ]),
    ("Chosen instead", GREEN, [
        "App Service (Linux, container) — managed patching & TLS",
        "Same PostgreSQL engine on Flexible Server — zero data-model rewrite",
        "Single EU region (France Central) — meets RPO/RTO within-region",
        "Reusable Terraform module + dev/prod instances now; landing zone deferred",
    ]),
]
x = 1.2
w = 12.6
for name, color, items in cols:
    add_rect_frame(p4, x, 3.9, w, 6.2, fs_white_card, name="col_bg")
    add_textbox(p4, x + 0.4, 4.1, w - 0.8, 0.6, [name], add_text_style(color=color, size="15pt", bold=True), name="col_h")
    add_bullets(p4, x + 0.4, 4.8, w - 0.8, 5.0, items, st_body_sm, name="col_items")
    x += w + 0.4

footer(p4, 4, TOTAL_SLIDES)

# ===========================================================================
# Slide 5 — Architecture diagram
# ===========================================================================
p5 = new_page("Architecture")
add_textbox(p5, 1.2, 0.55, 20.0, 0.9, ["Proposed architecture"], st_slide_title, name="t")
divider(p5, 1.25, 1.5, 3.0)
if DIAGRAM_PATH.exists():
    add_image(p5, DIAGRAM_PATH, 1.4, 1.75, 25.2, 11.9, name="diagram")
add_textbox(p5, 1.2, 13.75, 25.6, 0.6, [
    "Only the App Service is publicly reachable; data plane services sit behind private endpoints (prod)."
], st_body_sm, name="caption")
footer(p5, 5, TOTAL_SLIDES)

# ===========================================================================
# Slide 6 — Core building blocks (table-like)
# ===========================================================================
p6 = new_page("BuildingBlocks")
add_textbox(p6, 1.2, 0.7, 20.0, 1.0, ["Core building blocks"], st_slide_title, name="t")
divider(p6, 1.25, 1.75, 3.0)

blocks = [
    ("Compute", "App Service (Linux, container)", "Hosts the FastAPI app; managed patching, TLS, autoscale-ready"),
    ("Image registry", "Azure Container Registry (Premium)", "Stores the API image; pulled via managed identity"),
    ("Data", "PostgreSQL Flexible Server", "Drop-in for the on-prem DB; zone-redundant HA in prod"),
    ("Secrets", "Azure Key Vault", "DB credentials & app secrets"),
    ("Identity", "User-assigned Managed Identity", "Passwordless access to ACR, Key Vault, PostgreSQL"),
    ("Observability", "Log Analytics + App Insights", "Central logs, 365-day retention for audit"),
    ("Network", "VNet, 2 subnets, NSG", "Isolates data plane behind private endpoints"),
    ("Delivery", "GitHub Actions (OIDC) + Terraform", "Repeatable, auditable, click-ops-free"),
]
col_w = 12.6
row_h = 1.4
for i, (layer, service, purpose) in enumerate(blocks):
    col = i % 2
    row = i // 2
    x = 1.2 + col * (col_w + 0.4)
    y = 2.3 + row * row_h
    add_rect_frame(p6, x, y, col_w, row_h - 0.15, fs_white_card, name="blk_bg")
    add_textbox(p6, x + 0.3, y + 0.06, 3.0, row_h - 0.25, [layer], add_text_style(color=BLUE, size="11.5pt", bold=True), name="blk_layer")
    add_textbox(p6, x + 3.3, y + 0.06, col_w - 3.6, 0.55, [service], add_text_style(color=NAVY, size="12.5pt", bold=True), name="blk_service")
    add_textbox(p6, x + 3.3, y + 0.62, col_w - 3.6, 0.55, [purpose], add_text_style(color=GREY, size="10.5pt"), name="blk_purpose")

footer(p6, 6, TOTAL_SLIDES)

# ===========================================================================
# Slide 7 — Dev vs Prod
# ===========================================================================
p7 = new_page("DevProd")
add_textbox(p7, 1.2, 0.7, 20.0, 1.0, ["Two environments, one Terraform module"], st_slide_title, name="t")
divider(p7, 1.25, 1.75, 3.0)

env_cols = [
    ("dev", BLUE, [
        "Public network access enabled — faster inner-loop testing",
        "Single-zone PostgreSQL, no HA",
        "App Service P0v3  ·  PostgreSQL B_Standard_B1ms",
        "Synthetic / anonymized data only — never real customer data",
    ]),
    ("prod", GREEN, [
        "Private endpoints only — data plane off the public internet",
        "Zone-redundant HA + geo-redundant backup",
        "App Service P0v3  ·  PostgreSQL GP_Standard_D2s_v3",
        "Meets availability ≥ 99.9%, RPO ≤ 1h, RTO ≤ 4h",
    ]),
]
x = 1.2
w = 12.6
for name, color, items in env_cols:
    add_rect_frame(p7, x, 2.3, w, 5.6, fs_white_card, name="env_bg")
    add_rect_frame(p7, x, 2.3, w, 1.0, add_frame_style(fill_color=color, vertical="middle"), name="env_hdr_bg")
    add_textbox(p7, x, 2.3, w, 1.0, [name], add_text_style(color=WHITE, size="20pt", bold=True, align="center"), name="env_hdr")
    add_bullets(p7, x + 0.4, 3.5, w - 0.8, 4.2, items, st_body_sm, name="env_items")
    x += w + 0.4

add_textbox(p7, 1.2, 8.2, 25.6, 1.4, [
    "Same cs-api Terraform module, instantiated per environment with isolated state (.tfbackend) and sizing (.tfvars) — dev and prod share identical logic, never the same blast radius."
], add_text_style(color=NAVY, size="13.5pt", italic=True), name="note")
footer(p7, 7, TOTAL_SLIDES)

# ===========================================================================
# Slide 8 — CI/CD pipeline
# ===========================================================================
p8 = new_page("CICD")
add_textbox(p8, 1.2, 0.7, 20.0, 1.0, ["Repeatable delivery — no click-ops"], st_slide_title, name="t")
divider(p8, 1.25, 1.75, 3.0)

pipeline_steps = [
    ("1", "Push / PR to main", "Developer pushes code or infra changes"),
    ("2", "run-tf-plan.yml", "Azure OIDC login, terraform init/plan, diff surfaced on the PR"),
    ("3", "build-api-acr.yml", "Docker image built & pushed to the environment's ACR"),
    ("4", "run-tf-apply.yml", "terraform apply on merge to main — infra converges"),
]
x = 1.2
w = 6.2
for num, title, desc in pipeline_steps:
    add_rect_frame(p8, x, 2.6, w, 3.4, fs_white_card, name="step_bg")
    add_rect_frame(p8, x, 2.6, 1.0, 1.0, fs_blue_card, name="step_num_bg")
    add_textbox(p8, x, 2.6, 1.0, 1.0, [num], add_text_style(color=WHITE, size="18pt", bold=True, align="center"), name="step_num")
    add_textbox(p8, x + 0.3, 3.8, w - 0.6, 0.7, [title], add_text_style(color=NAVY, size="12.5pt", bold=True), name="step_title")
    add_textbox(p8, x + 0.3, 4.55, w - 0.6, 1.3, [desc], st_body_sm, name="step_desc")
    x += w + 0.35

add_rect_frame(p8, 1.2, 6.5, 25.6, 1.7, fs_green_card, name="oidc_box")
add_textbox(p8, 1.6, 6.75, 24.8, 0.5, ["No stored cloud secrets"], add_text_style(color=GREEN, size="13.5pt", bold=True), name="oidc_h")
add_textbox(p8, 1.6, 7.25, 24.8, 0.8, [
    "All workflows authenticate via Azure OIDC federated credentials (azure/login) — GitHub proves its identity to Azure AD per run, no long-lived client secret sits in GitHub."
], st_body_sm, name="oidc_body")

add_textbox(p8, 1.2, 8.6, 25.6, 0.6, ["Getting started (same steps CI runs automatically):"], add_text_style(color=NAVY, size="13pt", bold=True), name="cmd_h")
cmd_lines = [
    "cd iac/instances/frc",
    "terraform init  -backend-config=\"dev/dev.tfbackend\"",
    "terraform plan  -var-file=\"dev/dev.tfvars\"",
    "terraform apply -var-file=\"dev/dev.tfvars\"",
]
add_rect_frame(p8, 1.2, 9.25, 25.6, 2.6, add_frame_style(fill_color=NAVY, vertical="middle"), name="cmd_bg")
mono_style = add_text_style(color="#D8E4FF", size="13pt")
add_textbox(p8, 1.7, 9.4, 24.6, 2.3, cmd_lines, mono_style, name="cmd_text")
footer(p8, 8, TOTAL_SLIDES)

# ===========================================================================
# Slide 9 — Demo
# ===========================================================================
p9 = new_page("Demo")
add_rect_frame(p9, 0, 0, PAGE_W, PAGE_H, fs_section_bg, name="bg")
add_textbox(p9, 2.0, 6.3, 24.0, 1.5, ["Live demo"], st_section_title, name="t")
add_textbox(p9, 2.0, 7.9, 24.0, 1.0, [
    "Deploy to dev  ·  call the API  ·  tail Log Analytics / App Insights"
], st_section_sub, name="s")
footer(p9, 9, TOTAL_SLIDES, label="")

# ===========================================================================
# Slide 10 — AI in the workflow
# ===========================================================================
p10 = new_page("AI")
add_textbox(p10, 1.2, 0.7, 20.0, 1.0, ["Using AI as part of the workflow"], st_slide_title, name="t")
divider(p10, 1.25, 1.75, 3.0)

add_textbox(p10, 1.2, 2.2, 25.6, 0.8, [
    "AI is used where it adds real leverage in a cloud/IaC workflow — not as a checkbox."
], add_text_style(color=NAVY, size="14.5pt", italic=True), name="lede")

ai_cols = [
    ("AI IaC Reviewer", "Flags missing tags, public endpoints exposed unintentionally, and diagnostic settings gaps in Terraform before apply."),
    ("AI Architecture Explainer", "Turns the technical architecture into a one-page, non-technical rationale leadership can read in 5 minutes."),
    ("AI Log Insights Helper", "Summarizes app/infra logs from Log Analytics and suggests likely next diagnostic steps during an incident."),
]
x = 1.2
w = 8.4
for title, desc in ai_cols:
    add_rect_frame(p10, x, 3.3, w, 5.0, fs_lightblue_card, name="ai_bg")
    add_textbox(p10, x + 0.35, 3.55, w - 0.7, 1.1, [title], add_text_style(color=BLUE, size="14.5pt", bold=True), name="ai_title")
    add_textbox(p10, x + 0.35, 4.65, w - 0.7, 3.4, [desc], st_body_sm, name="ai_desc")
    x += w + 0.2

add_textbox(p10, 1.2, 8.6, 25.6, 1.6, [
    "In this PoC: minimal working examples that show how context (a Terraform plan, a log excerpt) is fed to an LLM and how the response is used — see /ai for the helper + README."
], st_body, name="note")
footer(p10, 10, TOTAL_SLIDES)

# ===========================================================================
# Slide 11 — Trade-offs, risks & next steps
# ===========================================================================
p11 = new_page("NextSteps")
add_textbox(p11, 1.2, 0.7, 20.0, 1.0, ["Trade-offs, risks & next steps"], st_slide_title, name="t")
divider(p11, 1.25, 1.75, 3.0)

add_textbox(p11, 1.2, 2.2, 12.0, 0.6, ["Biggest trade-offs accepted"], add_text_style(color=RED, size="14.5pt", bold=True), name="risk_h")
risk_items = [
    "Dev has public network access — cheaper/faster, but not representative of prod",
    "Single region (France Central) — no cross-region DR yet",
    "No WAF / Front Door in front of App Service yet",
    "No formal landing zone / Azure Policy guardrails yet",
]
add_bullets(p11, 1.2, 2.9, 12.5, 4.5, risk_items, st_body_sm, name="risk_items")

add_textbox(p11, 14.5, 2.2, 12.0, 0.6, ["Next, in priority order"], add_text_style(color=GREEN, size="14.5pt", bold=True), name="next_h")
next_items = [
    "Front Door + WAF, App Service fully private",
    "Lightweight landing zone: mgmt groups + Azure Policy, hub-spoke if a 2nd workload lands",
    "Key Vault references instead of app settings; automatic credential rotation",
    "CI quality gate: lint, unit tests, terraform validate before apply",
    "Formal DR restore drill against the RTO ≤ 4h / RPO ≤ 1h target",
]
add_bullets(p11, 14.5, 2.9, 12.5, 6.0, next_items, st_body_sm, name="next_items")

add_rect_frame(p11, 1.2, 10.4, 25.6, 1.9, fs_grey_card, name="honest_box")
add_textbox(p11, 1.6, 10.65, 24.8, 0.5, ["Being explicit about scope"], add_text_style(color=NAVY, size="13pt", bold=True), name="honest_h")
add_textbox(p11, 1.6, 11.15, 24.8, 1.0, [
    "This is a single-region, PaaS-only footprint — deliberately not a full landing zone yet. That's a scope choice, not an oversight."
], st_body_sm, name="honest_body")
footer(p11, 11, TOTAL_SLIDES)

# ===========================================================================
# Slide 12 — Closing / Q&A
# ===========================================================================
p12 = new_page("Closing")
add_rect_frame(p12, 0, 0, PAGE_W, PAGE_H, fs_section_bg, name="bg")
add_textbox(p12, 2.0, 5.6, 24.0, 1.5, ["Questions & discussion"], st_section_title, name="t")
add_textbox(p12, 2.0, 7.2, 24.0, 1.0, [
    "docs/architecture-summary.md  ·  docs/assumptions.md  ·  iac/modules/cs-api/README.md"
], st_section_sub, name="s")
_thanks_style = add_text_style(color="#8FA0C4", size="13pt", align="center")
add_textbox(p12, 2.0, 12.8, 24.0, 0.8, ["Thank you"], _thanks_style, name="thanks")
footer(p12, 12, TOTAL_SLIDES, label="")

# ---------------------------------------------------------------------------
doc.save(str(OUTPUT_PATH))
print(f"Saved presentation to {OUTPUT_PATH}")
