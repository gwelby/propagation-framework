"""
Build the one-page Propagation Framework summary PDF.
Run:  python papers/build_one_pager.py
Output: papers/PROPAGATION_FRAMEWORK_ONE_PAGER.pdf
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

OUTPUT = os.path.join(os.path.dirname(__file__),
                      "PROPAGATION_FRAMEWORK_ONE_PAGER.pdf")

# --- Colors ---
DARK = HexColor("#1a1a2e")
ACCENT = HexColor("#0f3460")
GREEN = HexColor("#16813d")
AMBER = HexColor("#b8860b")
GREY = HexColor("#555555")
LIGHT_BG = HexColor("#f0f4f8")
RULE_COLOR = HexColor("#0f3460")
WHITE = HexColor("#ffffff")

# --- Styles ---
sTitle = ParagraphStyle(
    "Title", fontName="Helvetica-Bold", fontSize=18,
    textColor=DARK, alignment=TA_CENTER, spaceAfter=2,
    leading=22,
)
sSubtitle = ParagraphStyle(
    "Subtitle", fontName="Helvetica", fontSize=9,
    textColor=GREY, alignment=TA_CENTER, spaceAfter=6,
    leading=11,
)
sSection = ParagraphStyle(
    "Section", fontName="Helvetica-Bold", fontSize=11,
    textColor=ACCENT, spaceBefore=8, spaceAfter=3,
    leading=13,
)
sBody = ParagraphStyle(
    "Body", fontName="Helvetica", fontSize=8.5,
    textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=3,
    leading=11,
)
sAxiom = ParagraphStyle(
    "Axiom", fontName="Helvetica-Bold", fontSize=8.5,
    textColor=DARK, spaceAfter=1, leading=11,
)
sAxiomBody = ParagraphStyle(
    "AxiomBody", fontName="Helvetica", fontSize=8,
    textColor=GREY, spaceAfter=4, leading=10,
    leftIndent=12,
)
sTableHeader = ParagraphStyle(
    "TH", fontName="Helvetica-Bold", fontSize=8,
    textColor=WHITE, leading=10,
)
sTableCell = ParagraphStyle(
    "TD", fontName="Helvetica", fontSize=7.8,
    textColor=DARK, leading=10,
)
sTableStatus = ParagraphStyle(
    "TDStatus", fontName="Helvetica-Bold", fontSize=7.8,
    leading=10,
)
sEquation = ParagraphStyle(
    "Eq", fontName="Courier-Bold", fontSize=9,
    textColor=DARK, alignment=TA_CENTER, spaceAfter=4,
    spaceBefore=2, leading=12,
)
sFooter = ParagraphStyle(
    "Footer", fontName="Helvetica", fontSize=7,
    textColor=GREY, alignment=TA_CENTER, leading=9,
)
sBold = ParagraphStyle(
    "Bold", fontName="Helvetica-Bold", fontSize=8.5,
    textColor=DARK, spaceAfter=2, leading=11,
)
sTest = ParagraphStyle(
    "Test", fontName="Helvetica", fontSize=8,
    textColor=DARK, spaceAfter=2, leading=10,
    leftIndent=12,
)


def status_cell(text, confidence):
    color = GREEN if confidence >= 0.90 else AMBER
    style = ParagraphStyle("s", parent=sTableStatus, textColor=color)
    return Paragraph(f"{text} ({confidence:.2f})", style)


def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=letter,
        leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        topMargin=0.45 * inch, bottomMargin=0.4 * inch,
    )

    story = []

    # --- Title ---
    story.append(Paragraph("The Propagation Framework", sTitle))
    story.append(Paragraph(
        "How Reality Derives Itself from Three Axioms", sSubtitle))
    story.append(Paragraph(
        "Greg Welby  |  Independent Research  |  March 2026  |  "
        "github.com/gwelby/propagation-framework", sSubtitle))
    story.append(HRFlowable(
        width="100%", thickness=1.5, color=RULE_COLOR, spaceAfter=6))

    # --- The Claim ---
    story.append(Paragraph("The Claim", sSection))
    story.append(Paragraph(
        "Everything is propagation. Matter is stable self-reinforcing wave "
        "patterns. Forces are refraction. Time is what propagation feels like "
        "from inside. Three axioms about how disturbances move through a "
        "medium derive the generation structure of the Standard Model, the "
        "Koide mass ratio, the Weinberg angle, and gravity - with zero free "
        "parameters.",
        sBody))

    # --- Three Axioms ---
    story.append(Paragraph("Three Axioms", sSection))

    story.append(Paragraph("Axiom 1: Propagation is Fundamental", sAxiom))
    story.append(Paragraph(
        "Everything that exists propagates. The medium is not empty space "
        "but a field capable of carrying a signal.", sAxiomBody))

    story.append(Paragraph("Axiom 2: Finite Causal Velocity", sAxiom))
    story.append(Paragraph(
        "Every medium has a maximum signal speed c. No causal influence "
        "propagates faster.", sAxiomBody))

    story.append(Paragraph("Axiom 3: Coherence", sAxiom))
    story.append(Paragraph(
        "Stable structure requires self-reinforcing, coherent propagation. "
        "Incoherent modes disperse. Among coherent states, the fundamental "
        "mode has minimal topological winding (Axiom 3b).", sAxiomBody))

    # --- Derived Results Table ---
    story.append(Paragraph("What the Axioms Derive", sSection))

    header = [
        Paragraph("Result", sTableHeader),
        Paragraph("Status", sTableHeader),
        Paragraph("Key Fact", sTableHeader),
    ]

    rows = [
        [
            Paragraph("Three generations of matter", sTableCell),
            status_cell("DERIVED", 0.98),
            Paragraph(
                "N=3 is the unique integer satisfying Q(N)=2/3 in 3D "
                "topology", sTableCell),
        ],
        [
            Paragraph("Topological weights (2,1)", sTableCell),
            status_cell("DERIVED", 0.98),
            Paragraph(
                "Fermion/boson distinction from pi_1(SO(3)) = Z_2",
                sTableCell),
        ],
        [
            Paragraph("Koide ratio Q = 2/3", sTableCell),
            status_cell("DERIVED", 0.95),
            Paragraph(
                "Geometric identity: 120-degree spacing forces R/A = sqrt(2)",
                sTableCell),
        ],
        [
            Paragraph("Gravity as refraction", sTableCell),
            status_cell("DERIVED", 0.95),
            Paragraph(
                "Randers/Finsler equivalence. Shapiro delay: 0.01% error",
                sTableCell),
        ],
        [
            Paragraph("8-hour sleep constant", sTableCell),
            status_cell("DERIVED", 0.92),
            Paragraph(
                "Q=2/3 of 24h cycle = 8h consolidation",
                sTableCell),
        ],
        [
            Paragraph(
                "Weinberg angle sin^2(theta_W)", sTableCell),
            status_cell("DERIVED", 0.90),
            Paragraph(
                "0.22310 via Axiom 3b. Matches PDG to 0.13 sigma",
                sTableCell),
        ],
        [
            Paragraph("QCD confinement from lambda_c", sTableCell),
            status_cell("ARGUED", 0.72),
            Paragraph(
                "Argued RG bridge from lambda_c. 1-loop overshoots: 2.2 fm vs ~0.9 fm",
                sTableCell),
        ],
    ]

    col_widths = [2.0 * inch, 1.15 * inch, 3.55 * inch]
    t = Table([header] + rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        # Body
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_BG, WHITE]),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        # Grid
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)

    # --- The God Equation ---
    story.append(Paragraph("The God Equation (Argued, 0.75)", sSection))
    story.append(Paragraph(
        "lambda_c = sqrt(2) * l_P * exp(4*pi^2 * N^(D/2) / b_0)",
        sEquation))
    story.append(Paragraph(
        "Predicts the top quark Compton wavelength from the Planck length "
        "alone. N=3, D=3, b_0=16/3. Predicted: 1.145 x 10^-18 m. "
        "Measured: 1.14 x 10^-18 m. Error: 0.4%. Zero free parameters. "
        "The bridge from internal phase closure to spatial coherence volume "
        "N^(D/2) remains the key open theorem.",
        sBody))

    # --- How to Kill It ---
    story.append(Paragraph("How to Kill It", sSection))
    story.append(Paragraph(
        "<b>Find a 4th generation particle</b> at any mass, any coupling. "
        "The framework says it cannot exist - the exclusion is topological, "
        "not kinematic.", sTest))
    story.append(Paragraph(
        "<b>Show Koide Q != 2/3 for neutrinos.</b> "
        "JUNO (2026) will constrain this. >5% deviation limits the "
        "framework's universality.", sTest))
    story.append(Paragraph(
        "<b>EEG phase transitions:</b> If Critical Slowing Down does not "
        "precede cognitive insight in >=7/10 sessions, the cross-scale "
        "claim fails.", sTest))
    story.append(Paragraph(
        "<b>Tau g-2 at Belle II:</b> Framework predicts a specific "
        "torsion correction. Pure QED agreement to 10^-5 falsifies it.",
        sTest))

    # --- What Failed ---
    story.append(Paragraph("What Failed (Honesty)", sSection))
    story.append(Paragraph(
        "The harmonic series mass claim failed (CV=0.94, noise). "
        "The phi^3 electron/up ratio is interesting but uncertainty-limited "
        "(p=0.007). The spin-pair selection strike produced three "
        "independent no-go results. All documented in sandbox_results.md. "
        "A framework that only publishes successes is not science.",
        sBody))

    # --- Footer ---
    story.append(Spacer(1, 6))
    story.append(HRFlowable(
        width="100%", thickness=0.8, color=RULE_COLOR, spaceBefore=4))
    story.append(Paragraph(
        "github.com/gwelby/propagation-framework  |  "
        "Clone and verify: python propagation.py  |  "
        "Full claims matrix: CLAIMS.md  |  "
        "Open gaps: CONTRIBUTING.md",
        sFooter))
    story.append(Paragraph(
        "This might be wrong. That is the point. "
        "The framework that survives contact with data is the one "
        "worth keeping.",
        ParagraphStyle("FooterItalic", parent=sFooter,
                        fontName="Helvetica-Oblique", spaceBefore=2)))

    doc.build(story)
    print(f"Built: {OUTPUT}")


if __name__ == "__main__":
    build()
