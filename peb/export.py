"""Export routines for PEB certificates."""

from __future__ import annotations

from xml.etree.ElementTree import Element, tostring

from fpdf import FPDF

from .models import Building
from .calculations import energy_score
from .config import REGIONAL_CONFIG


class CertificatePDF(FPDF):
    """Very small PDF for PEB certificate."""

    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "PEB Certificate", ln=True, align="C")


def export_certificate(building: Building, region: str, pdf_path: str, xml_path: str) -> None:
    """Export building certificate to PDF and XML."""
    score = energy_score(building, region)

    pdf = CertificatePDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Region: {region.title()} ({REGIONAL_CONFIG[region]['version']})", ln=True)
    pdf.cell(0, 10, f"Energy score: {score:.2f} kWh/m²", ln=True)
    pdf.output(pdf_path)

    root = Element("certificate")
    root.set("region", region)
    root.set("version", REGIONAL_CONFIG[region]["version"])
    score_elem = Element("energy_score")
    score_elem.text = f"{score:.2f}"
    root.append(score_elem)

    with open(xml_path, "wb") as f:
        f.write(tostring(root))
