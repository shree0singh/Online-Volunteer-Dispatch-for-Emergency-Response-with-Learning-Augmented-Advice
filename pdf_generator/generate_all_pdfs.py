"""
Master PDF generation script for Advanced Algorithms PS-6 Viva Deliverables.
Generates all 5 required academic study guides and overview documents.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.units import inch

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pdf_generator.styles import NumberedCanvas, get_academic_styles
from pdf_generator.content_member1 import build_member1_content
from pdf_generator.content_member2 import build_member2_content
from pdf_generator.content_member3 import build_member3_content
from pdf_generator.content_member4 import build_member4_content
from pdf_generator.content_overview import build_overview_content


def generate_pdf(filename: str, header_text: str, content_builder_func):
    """Builds a single PDF document using ReportLab SimpleDocTemplate and NumberedCanvas."""
    output_path = os.path.join("/home/shree/code/krishna", filename)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = get_academic_styles()
    story = []
    content_builder_func(story, styles)

    # Custom canvas maker that sets header text
    def canvas_maker(*args, **kwargs):
        c = NumberedCanvas(*args, **kwargs)
        c.doc_header_text = header_text
        return c

    doc.build(story, canvasmaker=canvas_maker)
    print(f"Successfully generated: {output_path} ({os.path.getsize(output_path)} bytes)")


def main():
    print("=== STARTING ACADEMIC PDF GENERATION FOR VIVA PREPARATION ===")

    # 1. Member 1 – Study Guide.pdf
    generate_pdf(
        filename="Member 1 – Study Guide.pdf",
        header_text="Member 1 Study Guide | Math Foundations & Offline Optimization",
        content_builder_func=build_member1_content
    )

    # 2. Member 2 – Study Guide.pdf
    generate_pdf(
        filename="Member 2 – Study Guide.pdf",
        header_text="Member 2 Study Guide | Online Algorithms, Bounds & Baselines",
        content_builder_func=build_member2_content
    )

    # 3. Member 3 – Study Guide.pdf
    generate_pdf(
        filename="Member 3 – Study Guide.pdf",
        header_text="Member 3 Study Guide | Learning-Augmented Algorithms & Safeguards",
        content_builder_func=build_member3_content
    )

    # 4. Member 4 – Study Guide.pdf
    generate_pdf(
        filename="Member 4 – Study Guide.pdf",
        header_text="Member 4 Study Guide | Simulation, Empirical Evaluation & Fairness",
        content_builder_func=build_member4_content
    )

    # 5. Complete Project Overview & Team Coordination.pdf
    generate_pdf(
        filename="Complete Project Overview & Team Coordination.pdf",
        header_text="Complete Project Overview & Team Coordination | RGIPT CSE PS-6",
        content_builder_func=build_overview_content
    )

    print("\n=== ALL 5 DELIVERABLE PDFS GENERATED SUCCESSFULLY ===")


if __name__ == "__main__":
    main()

