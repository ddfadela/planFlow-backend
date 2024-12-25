# utils/pdf_generator.py
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from django.conf import settings
import os

def create_project_pdf(project):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    elements.append(Paragraph(project.title, title_style))
    elements.append(Spacer(1, 12))

    # Project Details
    def add_field(label, value):
        elements.append(Paragraph(
            f"<b>{label}:</b> {value}",
            styles['Normal']
        ))
        elements.append(Spacer(1, 6))

    add_field("Description", project.description)
    add_field("Category", project.category)
    add_field("Status", project.status)
    add_field("Priority", project.priority)
    add_field("Start Date", project.start_date.strftime("%Y-%m-%d"))
    add_field("End Date", project.end_date.strftime("%Y-%m-%d"))
    
    elements.append(Spacer(1, 20))

    # Images
    if project.images.exists():
        elements.append(Paragraph("Project Images:", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        for image in project.images.all():
            img_path = os.path.join(settings.MEDIA_ROOT, str(image.image))
            if os.path.exists(img_path):
                img = Image(img_path)
                img.drawHeight = 3*inch
                img.drawWidth = 4*inch
                elements.append(img)
                elements.append(Spacer(1, 12))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf