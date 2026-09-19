import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from database.db import fetch_all_doubts
from config import UNIT_TO_TOPIC

def generate_pdf_report(unit_filter="All", filename="OS_Doubt_Summary.pdf"):
    doubts = fetch_all_doubts(unit_filter)
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    NAVY = colors.HexColor("#1e293b")
    PRIMARY = colors.HexColor("#2563eb")
    TEXT_MUTED = colors.HexColor("#64748b")
    LIGHT_BG = colors.HexColor("#f8fafc")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=NAVY,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=TEXT_MUTED,
        spaceAfter=15
    )
    
    unit_badge_style = ParagraphStyle(
        'UnitBadge',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=4
    )
    
    question_style = ParagraphStyle(
        'QuestionText',
        parent=styles['Heading4'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=NAVY,
        spaceAfter=4
    )
    
    answer_style = ParagraphStyle(
        'AnswerText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=10
    )
    
    elements = []
    
    # Header
    elements.append(Paragraph("Agentic AI & Automation: Doubts & Revision Summary", title_style))
    now_str = datetime.datetime.now().strftime("%B %d, %Y - %I:%M %p")
    filter_label = UNIT_TO_TOPIC.get(unit_filter, unit_filter)
    elements.append(Paragraph(f"Subject: Agentic AI & Automation (Course Level 3) | Generated: {now_str} | Topic Filter: {filter_label}", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=15))

    
    if not doubts:
        elements.append(Paragraph("No doubts found for the selected filter.", answer_style))
    else:
        elements.append(Paragraph(f"<b>Total Doubts Resolved:</b> {len(doubts)}", subtitle_style))
        elements.append(Spacer(1, 10))
        
        for idx, item in enumerate(doubts, start=1):
            q_text = item['question']
            a_text = item['answer'].replace('\n', '<br/>')
            topic = UNIT_TO_TOPIC.get(item['unit_tag'], item['unit_tag'])
            conf = int(item['confidence'] * 100) if item['confidence'] <= 1.0 else int(item['confidence'])
            ts = item['timestamp']
            
            # Badge header
            elements.append(Paragraph(f"#{idx} | [{topic}] (Confidence: {conf}%) — <i>{ts}</i>", unit_badge_style))
            elements.append(Paragraph(f"<b>Q:</b> {q_text}", question_style))
            elements.append(Paragraph(f"<b>A:</b> {a_text}", answer_style))
            elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceBefore=5, spaceAfter=10))
            
    doc.build(elements)
    return filename

