"""
PDF Styling and Layout Utilities for Academic Viva Study Guides.
Implements two-pass NumberedCanvas, academic color schemes, callouts, and table styles.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y'
    along with running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#718096"))

        # Running header (pages > 1)
        if self._pageNumber > 1:
            header_text = getattr(self, "doc_header_text", "Online Volunteer Dispatch — Viva Preparation Guide")
            self.drawString(54, 11 * inch - 36, header_text)
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Running footer
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(8.5 * inch - 54, 36, page_str)
        footer_text = "RGIPT CSE | Advanced Algorithms (PS-6) | Academic Year 2026–27"
        self.drawString(54, 36, footer_text)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * inch - 54, 46)

        self.restoreState()


def get_academic_styles():
    """Builds a cohesive typography and color hierarchy."""
    base = getSampleStyleSheet()

    PRIMARY = colors.HexColor("#1A365D")   # Deep Academic Navy
    SECONDARY = colors.HexColor("#2B6CB0") # Vibrant Slate Blue
    BODY_COLOR = colors.HexColor("#2D3748")# Charcoal Body
    MUTED = colors.HexColor("#718096")

    styles = {
        'DocTitle': ParagraphStyle(
            'DocTitle',
            parent=base['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=PRIMARY,
            spaceAfter=6
        ),
        'DocSubtitle': ParagraphStyle(
            'DocSubtitle',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=11,
            leading=15,
            textColor=SECONDARY,
            spaceAfter=14
        ),
        'SectionH1': ParagraphStyle(
            'SectionH1',
            parent=base['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=PRIMARY,
            spaceBefore=14,
            spaceAfter=6,
            keepWithNext=True
        ),
        'SectionH2': ParagraphStyle(
            'SectionH2',
            parent=base['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=11.5,
            leading=15,
            textColor=SECONDARY,
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True
        ),
        'SectionH3': ParagraphStyle(
            'SectionH3',
            parent=base['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=13,
            textColor=BODY_COLOR,
            spaceBefore=7,
            spaceAfter=3,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body',
            parent=base['BodyText'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=BODY_COLOR,
            spaceAfter=6
        ),
        'BodyBold': ParagraphStyle(
            'BodyBold',
            parent=base['BodyText'],
            fontName='Helvetica-Bold',
            fontSize=9.5,
            leading=13.5,
            textColor=BODY_COLOR,
            spaceAfter=6
        ),
        'Bullet': ParagraphStyle(
            'Bullet',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=BODY_COLOR,
            leftIndent=14,
            firstLineIndent=-10,
            spaceAfter=3
        ),
        'Question': ParagraphStyle(
            'Question',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=13.5,
            textColor=PRIMARY,
            spaceBefore=7,
            spaceAfter=3,
            keepWithNext=True
        ),
        'Answer': ParagraphStyle(
            'Answer',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=BODY_COLOR,
            leftIndent=8,
            spaceAfter=6
        ),
        'Code': ParagraphStyle(
            'Code',
            parent=base['Code'],
            fontName='Courier',
            fontSize=8,
            leading=10.5,
            textColor=colors.HexColor("#1A202C")
        ),
        'CalloutText': ParagraphStyle(
            'CalloutText',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12.5,
            textColor=colors.HexColor("#2C5282")
        ),
        'WarningText': ParagraphStyle(
            'WarningText',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12.5,
            textColor=colors.HexColor("#9B2C2C")
        ),
        'TipText': ParagraphStyle(
            'TipText',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12.5,
            textColor=colors.HexColor("#22543D")
        ),
        'TableHeader': ParagraphStyle(
            'TableHeader',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=11,
            textColor=colors.white,
            alignment=1
        ),
        'TableCell': ParagraphStyle(
            'TableCell',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=11,
            textColor=BODY_COLOR
        ),
        'TableCellBold': ParagraphStyle(
            'TableCellBold',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=11,
            textColor=BODY_COLOR
        )
    }
    return styles


def make_callout(text: str, styles, callout_type: str = "note", title: str = ""):
    """Creates a stylized bordered callout box."""
    if callout_type == "warning":
        bg_color = colors.HexColor("#FFF5F5")
        border_color = colors.HexColor("#E53E3E")
        style = styles['WarningText']
        prefix = f"<b>CRITICAL VIVA WARNING: {title}</b><br/>" if title else "<b>CRITICAL VIVA WARNING:</b> "
    elif callout_type == "tip":
        bg_color = colors.HexColor("#F0FFF4")
        border_color = colors.HexColor("#38A169")
        style = styles['TipText']
        prefix = f"<b>PROFESSOR'S TIP: {title}</b><br/>" if title else "<b>PROFESSOR'S TIP:</b> "
    else:  # note / key concept
        bg_color = colors.HexColor("#EBF8FF")
        border_color = colors.HexColor("#3182CE")
        style = styles['CalloutText']
        prefix = f"<b>KEY TAKEAWAY: {title}</b><br/>" if title else "<b>KEY TAKEAWAY:</b> "

    content = Paragraph(prefix + text, style)
    t = Table([[content]], colWidths=[7.0 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t


def make_code_box(code_str: str, styles):
    """Wraps code text inside a shaded monospace block."""
    p = Paragraph(code_str.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles['Code'])
    t = Table([[p]], colWidths=[7.0 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def make_styled_table(data_rows, col_widths, styles):
    """Constructs a responsive wrapped table with alternating row colors."""
    table_data = []
    # Header
    header_cells = [Paragraph(f"<b>{cell}</b>", styles['TableHeader']) for cell in data_rows[0]]
    table_data.append(header_cells)

    # Body
    for row in data_rows[1:]:
        row_cells = []
        for cell in row:
            if isinstance(cell, str) and cell.startswith("**") and cell.endswith("**"):
                row_cells.append(Paragraph(cell[2:-2], styles['TableCellBold']))
            else:
                row_cells.append(Paragraph(str(cell), styles['TableCell']))
        table_data.append(row_cells)

    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    return t

