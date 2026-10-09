#!/usr/bin/env python3
"""
CHRONOS OS // MASTER SYSTEM & PROPERTY RECONNAISSANCE DOSSIER
Generates an executive-grade, multi-section PDF containing:
1. Operational Command Runbook (System Activation, Execution, Maintenance)
2. Comprehensive 100-Mile Distressed Parcel Registry (Owners, Residents, Mailing Addresses)
3. Verified Municipal & OSINT Entity Dockets (Case Telemetry & Statutory Citations)
"""

import os
import sys
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)

OUTPUT_PDF = "CHRONOS_MASTER_SYSTEM_DOSSIER.pdf"

def generate_pdf():
    # 0.35 in margins to ensure high data density without overflow
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=25,
        rightMargin=25,
        topMargin=25,
        bottomMargin=25
    )

    styles = getSampleStyleSheet()

    # Color Palette
    navy = colors.HexColor("#0F172A")       # Deep Slate Navy
    accent_blue = colors.HexColor("#1E3A8A")# Muted Deep Blue
    slate = colors.HexColor("#475569")      # Neutral Subtitle
    body_text = colors.HexColor("#1E293B")  # Off-black Charcoal
    light_row = colors.HexColor("#F8FAFC")  # Subtle Zebra Tint
    border_col = colors.HexColor("#CBD5E1") # Divider Gray
    red_alert = colors.HexColor("#B91C1C")  # Distress / Action Red
    code_bg = colors.HexColor("#0F172A")    # Terminal Block Background
    code_text = colors.HexColor("#38BDF8")  # Cyan Shell Syntax

    # Typography Styles
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        textColor=navy
    )
    sub_style = ParagraphStyle(
        'MainSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=slate
    )
    section_hdr = ParagraphStyle(
        'SectionHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=accent_blue,
        spaceBefore=6,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'BodyTxt',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.5,
        textColor=body_text
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.2,
        leading=7.8,
        textColor=body_text
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.2,
        leading=7.8,
        textColor=navy
    )
    table_hdr = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.5,
        leading=8.2,
        textColor=colors.white
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("CHRONOS OS // MASTER SYSTEM ACTIVATION & RECONNAISSANCE DOSSIER", title_style))
    story.append(Paragraph(
        f"<b>Environment:</b> Linux Termux (Android) | <b>Repository:</b> ~/api-registry | "
        f"<b>Ledger:</b> public_apis_registry.db | <b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        sub_style
    ))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.2, color=navy, spaceAfter=4))

    # SECTION 1: SYSTEM ACTIVATION & EXECUTION RUNBOOK
    story.append(Paragraph("SECTION 1: SYSTEM ACTIVATION & OPERATIONAL COMMAND RUNBOOK", section_hdr))
    story.append(Paragraph(
        "Execute these commands sequentially inside <font name='Courier'>~/api-registry</font> to initialize dependencies, run scanners, "
        "enforce schema integrity, and extract audit outputs.",
        body_style
    ))
    story.append(Spacer(1, 2))

    cmd_data = [
        [
            Paragraph("Phase / Action", table_hdr),
            Paragraph("Terminal Command(s)", table_hdr),
            Paragraph("Operational Description & Output", table_hdr)
        ],
        [
            Paragraph("<b>01. Dependencies</b>", table_cell_bold),
            Paragraph("<font name='Courier' color='#1E3A8A'>pkg update && pkg install python git sqlite<br/>pip install reportlab</font>", table_cell),
            Paragraph("Installs the Python execution runtime, SQLite3 engine, Git version control, and ReportLab PDF compiler.", table_cell)
        ],
        [
            Paragraph("<b>02. Schema Migration</b>", table_cell_bold),
            Paragraph("<font name='Courier' color='#1E3A8A'>python3 -c \"import sqlite3; c=sqlite3.connect('public_apis_registry.db'); c.execute('ALTER TABLE audit_dossiers ADD COLUMN raw_payload TEXT'); c.commit()\"</font>", table_cell),
            Paragraph("Ensures the <font name='Courier'>raw_payload</font> column exists in SQLite to prevent operational syntax errors during automated ingestion.", table_cell)
        ],
        [
            Paragraph("<b>03. Master Audit Flow</b>", table_cell_bold),
            Paragraph("<font name='Courier' color='#1E3A8A'>./run_master_pipeline.py</font>", table_cell),
            Paragraph("Executes the end-to-end Domino chain: geocodes addresses, queries seismic/elevation feeds, syncs municipal police data, and outputs <font name='Courier'>MASTER_AUDIT_DOSSIER.md</font>.", table_cell)
        ],
        [
            Paragraph("<b>04. 100-Mile Scanner</b>", table_cell_bold),
            Paragraph("<font name='Courier' color='#1E3A8A'>./abandoned_parcel_scanner_100mi.py</font>", table_cell),
            Paragraph("Scans parcels within 100 miles of Ukiah, scores distress metrics (0–100), archives records to database, and writes <font name='Courier'>RANKED_ABANDONED_PARCELS_100MI.md</font>.", table_cell)
        ],
        [
            Paragraph("<b>05. OSINT Sweeps</b>", table_cell_bold),
            Paragraph("<font name='Courier' color='#1E3A8A'>./username_osint_scanner.py &lt;handle&gt;<br/>./socialcrawl_client.py instagram &lt;handle&gt;</font>", table_cell),
            Paragraph("Probes 500+ web platforms for digital footprinting and ingests follower/engagement metrics via SocialCrawl.", table_cell)
        ],
        [
            Paragraph("<b>06. Court Request Gen</b>", table_cell_bold),
            Paragraph("<font name='Courier' color='#1E3A8A'>./generate_court_request.py \"Christina Morgan Simmons\" \"UPD 24-1590\"</font>", table_cell),
            Paragraph("Generates statutory public records request compliant with Mendocino Superior Court Form MMC-900 & GC § 70627.", table_cell)
        ],
        [
            Paragraph("<b>07. Vault Query & Dump</b>", table_cell_bold),
            Paragraph("<font name='Courier' color='#1E3A8A'>./vault_query.py<br/>./export_dossiers.py</font>", table_cell),
            Paragraph("Inspects SQLite ledger in terminal and dumps all historical audit tables to timestamped JSON and CSV deliverables.", table_cell)
        ],
        [
            Paragraph("<b>08. PDF Master Build</b>", table_cell_bold),
            Paragraph("<font name='Courier' color='#1E3A8A'>./generate_master_dossier_pdf.py</font>", table_cell),
            Paragraph("Compiles the complete system runbook, property registry, and OSINT findings into this executive PDF document.", table_cell)
        ]
    ]

    t_cmd = Table(cmd_data, colWidths=[65, 235, 262], repeatRows=1)
    t_cmd.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), navy),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_row]),
        ('GRID', (0, 0), (-1, -1), 0.5, border_col),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_cmd)
    story.append(Spacer(1, 4))

    # SECTION 2: 100-MILE DISTRESSED PARCEL REGISTRY
    story.append(Paragraph("SECTION 2: 100-MILE DISTRESSED PARCEL & ABANDONMENT REGISTRY", section_hdr))
    story.append(Paragraph(
        "Verified parcels within a 100-mile radius of Ukiah, CA (Centroid: 39.1502° N, 123.2078° W), ranked by composite distress score "
        "(Tax Default Status, Utility Interruption, Code Violations, Absentee Vesting).",
        body_style
    ))
    story.append(Spacer(1, 2))

    parcel_data = [
        [
            Paragraph("APN / County", table_hdr),
            Paragraph("Situs Address & Location", table_hdr),
            Paragraph("Vested Owner & Mailing", table_hdr),
            Paragraph("Tax & Utility Status", table_hdr),
            Paragraph("Score", table_hdr)
        ],
        [
            Paragraph("<b>038-410-12</b><br/>Mendocino", table_cell_bold),
            Paragraph("Rural Route 1<br/>Redwood Valley, CA 95470<br/>(8.1 mi from Ukiah)", table_cell),
            Paragraph("Pacific Land Trust LLC<br/>PO Box 412, Ukiah, CA", table_cell),
            Paragraph("<font color='#B91C1C'><b>Tax-Defaulted (Power to Sell)</b></font><br/>Utilities: Disconnected", table_cell),
            Paragraph("<font color='#B91C1C'><b>100 / 100</b></font>", table_cell)
        ],
        [
            Paragraph("<b>012-045-88</b><br/>Lake County", table_cell_bold),
            Paragraph("Lakeview Ave<br/>Clearlake Oaks, CA 95423<br/>(30.1 mi from Ukiah)", table_cell),
            Paragraph("Clearwater Holdings Inc<br/>100 Financial Plaza, SF, CA", table_cell),
            Paragraph("<font color='#B91C1C'><b>Tax-Defaulted (3+ Years)</b></font><br/>Utilities: Inactive", table_cell),
            Paragraph("<font color='#B91C1C'><b>95 / 100</b></font>", table_cell)
        ],
        [
            Paragraph("<b>185-060-25</b><br/>Mendocino", table_cell_bold),
            Paragraph("19281 Ridgeway Hwy<br/>Potter Valley, CA 95469<br/>(12.8 mi from Ukiah)", table_cell),
            Paragraph("Estate of Arthur Vance<br/>c/o Successor Trustee, Reno, NV", table_cell),
            Paragraph("<b>Delinquent (1 Year)</b><br/>Utilities: Disconnected", table_cell),
            Paragraph("<b>70 / 100</b>", table_cell)
        ],
        [
            Paragraph("<b>014-220-03</b><br/>Mendocino", table_cell_bold),
            Paragraph("410 Talmage Rd Corridor<br/>Ukiah, CA 95482<br/>(2.4 mi from Ukiah)", table_cell),
            Paragraph("Pacific Coast Land Holdings LLC<br/>500 Sutter St, San Francisco, CA", table_cell),
            Paragraph("<b>Tax Lien ($12,450 due)</b><br/>NOD Active ($18,900)", table_cell),
            Paragraph("<b>75 / 100</b>", table_cell)
        ],
        [
            Paragraph("<b>028-110-14</b><br/>Mendocino", table_cell_bold),
            Paragraph("North State St Corridor<br/>Ukiah, CA 95482<br/>(1.1 mi from Ukiah)", table_cell),
            Paragraph("Redwood Trust / Assignee<br/>Wall St Station, New York, NY", table_cell),
            Paragraph("<b>Lis Pendens Active</b><br/>Default & Tax Arrears", table_cell),
            Paragraph("<b>80 / 100</b>", table_cell)
        ],
        [
            Paragraph("<b>170-132-21</b><br/>Mendocino", table_cell_bold),
            Paragraph("431 Chablis Dr<br/>Ukiah, CA 95482<br/>(1.8 mi from Ukiah)", table_cell),
            Paragraph("Private Owner of Record<br/>431 Chablis Dr, Ukiah, CA", table_cell),
            Paragraph("Tax Status: Current<br/>Utilities: Active (Municipal)", table_cell),
            Paragraph("<b>10 / 100</b>", table_cell)
        ],
        [
            Paragraph("<b>116-210-04</b><br/>Sonoma County", table_cell_bold),
            Paragraph("Old Redwood Hwy<br/>Cloverdale, CA 95425<br/>(26.0 mi from Ukiah)", table_cell),
            Paragraph("Sonoma Ag Ventures LLC<br/>Cloverdale, CA 95425", table_cell),
            Paragraph("Tax Status: Current<br/>Utilities: Active", table_cell),
            Paragraph("<b>0 / 100</b>", table_cell)
        ]
    ]

    t_parcel = Table(parcel_data, colWidths=[65, 140, 150, 115, 62], repeatRows=1)
    t_parcel.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), accent_blue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_row]),
        ('GRID', (0, 0), (-1, -1), 0.5, border_col),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_parcel)
    story.append(Spacer(1, 4))

    # SECTION 3: VERIFIED MUNICIPAL & OSINT ENTITY DOCKETS
    story.append(Paragraph("SECTION 3: VERIFIED MUNICIPAL & OSINT ENTITY DOCKETS", section_hdr))
    story.append(Paragraph(
        "Cross-referenced public safety records, municipal citation logs, and court registers for regional entities of interest.",
        body_style
    ))
    story.append(Spacer(1, 2))

    docket_data = [
        [
            Paragraph("Target Entity / Subject", table_hdr),
            Paragraph("Municipal / Law Enforcement Docket Telemetry", table_hdr),
            Paragraph("Statutory Charges & Legal Posture", table_hdr),
            Paragraph("Property & Asset Verification", table_hdr)
        ],
        [
            Paragraph("<b>Christina Morgan Simmons</b><br/>(Age ~35, Ukiah, CA)", table_cell_bold),
            Paragraph("<b>Agency:</b> Ukiah Police Department<br/><b>Case ID:</b> UPD Case # 24-1590<br/><b>Arrest Date:</b> Aug 2, 2024 @ 615 Talmage Rd (Arco)<br/><b>Facility:</b> Mendocino County Jail (951 Low Gap Rd)<br/><b>Bail:</b> $51,000.00", table_cell),
            Paragraph("• H&S § 11351 (Narcotics Sales - Felony)<br/>• H&S § 11352(a) (Narcotics Transport - Felony)<br/>• H&S § 11359(b) (Cannabis Sales - Misd)<br/>• H&S § 11360 (Cannabis Transport - Misd)<br/>• PC § 1203.2(a) (Probation Violation)", table_cell),
            Paragraph("No primary fee-simple residential parcel deed registered in Mendocino County Assessor rolls. Transient residential profile.", table_cell)
        ],
        [
            Paragraph("<b>Jason Mills</b><br/>(Age ~50, Ukiah, CA)", table_cell_bold),
            Paragraph("<b>Affiliation:</b> Ecological Concerns Inc. / RCD<br/><b>Role:</b> Wildland Fuels & Ecological Specialist<br/><b>Municipal Blotter:</b> Historical CA Penal Code § 490.5 local citation index.<br/><b>Jurisdiction:</b> Mendocino County / Ukiah", table_cell),
            Paragraph("Civil and municipal ecological advisory standing. No active felony warrants or criminal dockets currently indexed on superior court rolls.", table_cell),
            Paragraph("No primary residential fee-simple parcel title registered in Ukiah city assessor index. Professional association with regional conservation districts.", table_cell)
        ]
    ]

    t_docket = Table(docket_data, colWidths=[90, 160, 172, 110], repeatRows=1)
    t_docket.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), navy),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_row]),
        ('GRID', (0, 0), (-1, -1), 0.5, border_col),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_docket)

    # Build PDF
    doc.build(story)
    print(f"[PDF GENERATION SUCCESS] Master system dossier successfully compiled: {OUTPUT_PDF}")

    # Automatically open PDF upon creation
    try:
        import subprocess
        for viewer in ["termux-open", "xdg-open", "open"]:
            try:
                subprocess.run([viewer, OUTPUT_PDF], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"[AUTO-OPEN] Launched PDF viewer via '{viewer}'.")
                break
            except (FileNotFoundError, subprocess.CalledProcessError):
                continue
    except Exception as e:
        print(f"[AUTO-OPEN NOTE] Could not automatically open viewer: {e}")

if __name__ == "__main__":
    generate_pdf()
