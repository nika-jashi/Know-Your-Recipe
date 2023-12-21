from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageTemplate, BaseDocTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.http import HttpResponse
import os


class FooterPageTemplate(PageTemplate):
    def __init__(self, id, frames, *args, **kwargs):
        PageTemplate.__init__(self, id, frames, *args, **kwargs)

    def afterDrawPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(letter[0] - inch, inch / 2, f"Created At: {doc.created_at}")
        canvas.restoreState()


class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        frame = Frame(
            inch,
            inch,
            letter[0] - 2 * inch,
            letter[1] - 2 * inch,
            id='normal',
        )
        template = FooterPageTemplate('footer', [frame])
        self.addPageTemplates(template)


def generate_recipe_pdf(recipe):
    # Create the PDF file path
    pdf_filename = f"{recipe.title.replace(' ', '_').lower()}_recipe.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)

    # Ensure the directory exists, create if necessary
    media_directory = os.path.dirname(pdf_path)
    if not os.path.exists(media_directory):
        os.makedirs(media_directory)

    # Create a response object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'

    # Create the PDF content using ReportLab
    doc = MyDocTemplate(response, pagesize=letter)
    doc.created_at = recipe.created_at.strftime("%d/%m/%Y")
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'Title1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        spaceAfter=12,
        alignment=1  # Centered
    )
    title = Paragraph(f"<u>{recipe.title}</u>", title_style)

    # Details
    details_style = styles['Heading2']
    link_style = styles['BodyText']
    masked_link_text = f"<u>Recipe Reference Link</u>"  # Masked text for the link
    actual_link = recipe.link
    details = [
        Paragraph('<b>Details:</b>', details_style),
        Paragraph(f"Instructions: {recipe.description}", styles['BodyText']),
        Paragraph(f"Preparation Time: {recipe.preparation_time_minutes} minutes", styles['BodyText']),
        Paragraph(f"Price: ${recipe.price}", styles['BodyText']),
        Paragraph(f"Link: {masked_link_text} ({actual_link})", link_style),
        Paragraph(f"Difficulty: {recipe.get_competence_level_display()}", styles['BodyText']),
    ]

    # Tags
    tags_style = styles['Heading2']
    tags = [
        Paragraph('<b>Tags:</b>', tags_style),
    ]
    for tag in recipe.tags.all():
        tags.append(Paragraph(f"• {tag.name}", styles['BodyText']))

    # Ingredients
    ingredients_style = styles['Heading2']
    ingredients = [
        Paragraph('<b>Ingredients:</b>', ingredients_style),
    ]
    for ingredient in recipe.ingredients.all():
        ingredients.append(Paragraph(f"• {ingredient.name}", styles['BodyText']))

    # Build the document
    content = [title]
    if recipe.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(recipe.image.path))
        recipe_image = Image(image_path, width=150, height=150)
        content.append(recipe_image)
    content += details + [Spacer(1, 12)] + tags + [Spacer(1, 12)] + ingredients + [Spacer(1, 12)]
    doc.build(content)

    return response
