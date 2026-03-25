"""
Robofolio AI-Powered Lead Capture Backend API
Flask API with Claude AI integration for website and media analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import requests
import base64
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime

app = Flask(__name__)

# CORS: Allow configured origins in production, or all in development
ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', '*')
if ALLOWED_ORIGINS == '*':
    CORS(app)
else:
    CORS(app, origins=[o.strip() for o in ALLOWED_ORIGINS.split(',')])

# Configuration
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
JINA_API_KEY = os.environ.get('JINA_API_KEY', '')  # Optional: for better web scraping
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASS = os.environ.get('SMTP_PASS', '')
GOOGLE_SHEETS_WEBHOOK = os.environ.get('GOOGLE_SHEETS_WEBHOOK', '')  # Apps Script Web App URL
IS_PRODUCTION = os.environ.get('RENDER', '') == 'true' or os.environ.get('PORT', '') != ''

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


@app.route('/api/analyze-website', methods=['POST'])
def analyze_website():
    """
    Analyze a company website and extract relevant information
    """
    try:
        data = request.get_json()
        website_url = data.get('url', '')

        if not website_url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400

        # Ensure URL has scheme
        if not website_url.startswith('http'):
            website_url = 'https://' + website_url

        # Check API key before doing work
        if not ANTHROPIC_API_KEY:
            return jsonify({'success': False, 'error': 'ANTHROPIC_API_KEY not configured on server. Set it with: export ANTHROPIC_API_KEY=your-key'}), 500

        # Scrape website content
        print(f"Scraping website: {website_url}")
        website_content = scrape_website(website_url)

        if not website_content:
            return jsonify({'success': False, 'error': f'Could not fetch website content from {website_url}. The site may be blocking automated access.'}), 400

        print(f"Scraped {len(website_content)} chars from {website_url}")

        # Analyze with Claude
        content_snippet = website_content[:15000]
        extraction_prompt = f"""Analyze this company website content and extract the following information in JSON format:

{{
  "company_name": "Full company name",
  "industry": "Specific industry (e.g., 'Automotive parts manufacturing', 'Food & beverage packaging')",
  "location": "City, region/state, country",
  "company_size": "Estimated size category: 'Small (<€10M)', 'Mid-market (€10M-€500M)', or 'Large (€500M+)'",
  "main_products": "Brief description of main products or services",
  "automation_level": "Current automation level if mentioned: 'Manual', 'Semi-automated', 'Highly automated', or 'Unknown'",
  "production_challenges": "Any mentioned production challenges or goals",
  "contact_email": "Primary contact email if available",
  "contact_phone": "Primary phone number if available",
  "language": "Website language (de, en, etc.)"
}}

Website content:
{content_snippet}

Respond ONLY with valid JSON. If information is not available, use "Unknown" or empty string.
"""

        print("Sending to Claude for analysis...")
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": extraction_prompt
            }]
        )

        # Parse Claude's response
        extracted_json = message.content[0].text
        print(f"Claude response length: {len(extracted_json)}")

        # Try to extract JSON from response (sometimes Claude adds explanation)
        if '```json' in extracted_json:
            extracted_json = extracted_json.split('```json')[1].split('```')[0]
        elif '```' in extracted_json:
            extracted_json = extracted_json.split('```')[1].split('```')[0]

        extracted_data = json.loads(extracted_json.strip())

        return jsonify({
            'success': True,
            'data': extracted_data
        })

    except json.JSONDecodeError as e:
        print(f"JSON parse error in analyze_website: {str(e)}")
        return jsonify({'success': False, 'error': 'Could not parse AI response. Please try again.'}), 500
    except anthropic.AuthenticationError:
        print("Anthropic API authentication failed")
        return jsonify({'success': False, 'error': 'Invalid ANTHROPIC_API_KEY. Please check your API key.'}), 500
    except anthropic.APIError as e:
        print(f"Anthropic API error: {str(e)}")
        return jsonify({'success': False, 'error': f'AI service error: {str(e)}'}), 500
    except Exception as e:
        print(f"Error in analyze_website: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/analyze-photos', methods=['POST'])
def analyze_photos():
    """
    Analyze uploaded photos of workspace/production process
    """
    try:
        # Get uploaded files
        files = request.files.getlist('photos')

        if not files or len(files) == 0:
            return jsonify({'error': 'No photos provided'}), 400

        # Convert images to base64 for Claude
        images_data = []
        for file in files[:5]:  # Max 5 photos
            image_bytes = file.read()
            base64_image = base64.standard_b64encode(image_bytes).decode('utf-8')

            # Detect media type
            media_type = file.content_type or 'image/jpeg'

            images_data.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64_image
                }
            })

        # Analyze with Claude Vision
        analysis_prompt = """
Analyze these workspace/production photos and extract the following information in JSON format:

{
  "process_type": "Type of operation visible (e.g., 'Pick & place', 'Assembly', 'Packaging', 'Welding', 'Inspection', etc.)",
  "current_process_description": "2-3 sentence description of what you see happening in the workspace",
  "workspace_dimensions": "Estimated workspace size (e.g., '~4m x 3m' or 'Large open floor')",
  "workspace_layout": "Layout type (e.g., 'Linear', 'U-shaped', 'Island', 'Multiple workstations')",
  "environment_type": "Environment (e.g., 'Standard factory floor', 'Cleanroom', 'Warehouse', 'Outdoor')",
  "existing_equipment": "List of visible equipment/machinery",
  "products_visible": "Type and size of products/parts visible",
  "automation_level": "Current automation: 'Fully manual', 'Semi-automated', 'Highly automated'",
  "physical_constraints": "Any constraints observed (e.g., 'Limited floor space', 'Low ceiling', 'Cluttered')",
  "safety_equipment": "Safety equipment visible (barriers, e-stops, PPE, etc.)",
  "ergonomic_concerns": "Any ergonomic issues observed (heavy lifting, repetitive motions, awkward positions)",
  "lighting": "Lighting conditions (Good, Adequate, Poor)",
  "automation_suitability": "Is this suitable for robotic automation? Brief assessment."
}

Respond ONLY with valid JSON. Be specific and detailed in your observations.
"""

        # Create message with images
        message_content = [{"type": "text", "text": analysis_prompt}] + images_data

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{
                "role": "user",
                "content": message_content
            }]
        )

        # Parse response
        extracted_json = message.content[0].text

        if '```json' in extracted_json:
            extracted_json = extracted_json.split('```json')[1].split('```')[0]
        elif '```' in extracted_json:
            extracted_json = extracted_json.split('```')[1].split('```')[0]

        extracted_data = json.loads(extracted_json.strip())

        return jsonify({
            'success': True,
            'data': extracted_data
        })

    except Exception as e:
        print(f"Error in analyze_photos: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/submit-lead', methods=['POST'])
def submit_lead():
    """
    Submit complete lead data and trigger lead deck generation
    """
    try:
        lead_data = request.get_json()

        # Generate unique lead ID
        lead_id = f"RF-{datetime.now().strftime('%Y%m%d')}-{generate_random_id()}"
        lead_data['lead_id'] = lead_id
        lead_data['date'] = datetime.now().strftime('%Y-%m-%d')
        lead_data['timestamp'] = datetime.now().isoformat()

        # Calculate lead score
        lead_score = calculate_lead_score(lead_data)
        lead_data['lead_score'] = lead_score

        # Save to Google Sheets
        sheets_ok = save_to_google_sheets(lead_data)

        # Generate PDF lead deck
        pdf_path = generate_lead_deck_pdf(lead_data)

        # Send emails
        send_lead_confirmation_email(lead_data)
        send_integrator_notification_emails(lead_data, pdf_path)

        return jsonify({
            'success': True,
            'lead_id': lead_id,
            'lead_score': lead_score,
            'pdf_generated': pdf_path is not None,
            'sheets_saved': sheets_ok,
            'message': 'Lead submitted successfully'
        })

    except Exception as e:
        print(f"Error in submit_lead: {str(e)}")
        return jsonify({'error': str(e)}), 500


def scrape_website(url):
    """
    Scrape website content using Jina AI Reader or fallback to simple fetch.
    Tries multiple methods and returns the first successful result.
    """
    # Option 1: Use Jina AI Reader with API key (best quality)
    if JINA_API_KEY:
        try:
            print(f"  Trying Jina AI (with API key)...")
            jina_url = f"https://r.jina.ai/{url}"
            headers = {
                'Authorization': f'Bearer {JINA_API_KEY}',
                'X-Return-Format': 'markdown'
            }
            response = requests.get(jina_url, headers=headers, timeout=45)
            if response.status_code == 200 and len(response.text) > 100:
                print(f"  Jina AI (key) success: {len(response.text)} chars")
                return response.text
            else:
                print(f"  Jina AI (key) returned status {response.status_code}, len={len(response.text)}")
        except Exception as e:
            print(f"  Jina AI (key) failed: {e}")

    # Option 2: Jina free service (no API key)
    try:
        print(f"  Trying Jina AI (free)...")
        jina_url = f"https://r.jina.ai/{url}"
        headers = {
            'X-Return-Format': 'markdown',
            'Accept': 'text/plain'
        }
        response = requests.get(jina_url, headers=headers, timeout=45)
        if response.status_code == 200 and len(response.text) > 100:
            print(f"  Jina AI (free) success: {len(response.text)} chars")
            return response.text
        else:
            print(f"  Jina AI (free) returned status {response.status_code}, len={len(response.text)}")
    except Exception as e:
        print(f"  Jina AI (free) failed: {e}")

    # Option 3: Direct fetch with browser-like User-Agent
    try:
        print(f"  Trying direct fetch...")
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        }, timeout=30, allow_redirects=True)

        if response.status_code == 200 and len(response.text) > 100:
            print(f"  Direct fetch success: {len(response.text)} chars")
            # Strip HTML tags for a rough text extraction
            import re
            text = re.sub(r'<script[^>]*>.*?</script>', '', response.text, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text) > 100:
                return text
            print(f"  Direct fetch: cleaned text too short ({len(text)} chars)")
        else:
            print(f"  Direct fetch returned status {response.status_code}")
    except Exception as e:
        print(f"  Direct fetch failed: {e}")

    print(f"  All scraping methods failed for {url}")
    return None


def calculate_lead_score(lead_data):
    """
    Calculate lead score based on BANT and other factors
    Score: 0-100
    """
    score = 0

    # Budget (30 points)
    budget_status = lead_data.get('budget_status', '')
    if budget_status == 'approved':
        score += 30
    elif budget_status == 'in-process':
        score += 20
    elif budget_status == 'need-roi':
        score += 10
    elif budget_status == 'researching':
        score += 5

    # Timeline (25 points)
    timeline = lead_data.get('timeline', '')
    if timeline == '0-3months':
        score += 25
    elif timeline == '3-6months':
        score += 20
    elif timeline == '6-12months':
        score += 15
    elif timeline == '12+months':
        score += 10

    # Authority (20 points)
    authority = lead_data.get('authority', '')
    if authority == 'decision-maker':
        score += 20
    elif authority == '1-approval':
        score += 15
    elif authority == '2+-approvals':
        score += 10
    elif authority == 'committee':
        score += 5

    # Technical Clarity (15 points)
    # Check if we have extracted technical data
    has_process = bool(lead_data.get('process_type') or lead_data.get('extracted_process_type'))
    has_workspace = bool(lead_data.get('workspace_dimensions') or lead_data.get('extracted_workspace'))

    if has_process and has_workspace:
        score += 15
    elif has_process or has_workspace:
        score += 10
    else:
        score += 5

    # Company Fit (10 points)
    company_size = lead_data.get('company_size', '')
    if 'mid-market' in company_size.lower() or ('10' in company_size and '500' in company_size):
        score += 10
    elif 'large' in company_size.lower():
        score += 7
    else:
        score += 5

    return min(score, 100)  # Cap at 100


def generate_random_id():
    """Generate random ID for leads"""
    import random
    import string
    return ''.join(random.choices(string.digits, k=3))


# ---------------------------------------------------------------------------
# Google Sheets Integration
# ---------------------------------------------------------------------------

def save_to_google_sheets(lead_data):
    """
    Save lead data to Google Sheets via Apps Script Web App webhook.
    The Google Apps Script should be deployed as a Web App (see GOOGLE_SHEETS_SETUP.md).
    It receives JSON POST data and appends a row to the configured sheet.
    """
    if not GOOGLE_SHEETS_WEBHOOK:
        print("WARN: GOOGLE_SHEETS_WEBHOOK not configured, skipping Sheets save")
        return False

    try:
        row_data = {
            'lead_id': lead_data.get('lead_id', ''),
            'date': lead_data.get('date', ''),
            'company_name': lead_data.get('company_name', ''),
            'industry': lead_data.get('industry', ''),
            'location': lead_data.get('location', ''),
            'company_size': lead_data.get('company_size', ''),
            'contact_name': lead_data.get('contact_name', ''),
            'contact_email': lead_data.get('contact_email', ''),
            'contact_phone': lead_data.get('contact_phone', ''),
            'contact_title': lead_data.get('contact_title', ''),
            'application_type': lead_data.get('application_type', ''),
            'primary_goal': lead_data.get('primary_goal', ''),
            'current_process': lead_data.get('current_process', ''),
            'budget_range': lead_data.get('budget_range', ''),
            'budget_status': lead_data.get('budget_status', ''),
            'timeline': lead_data.get('timeline', ''),
            'authority': lead_data.get('authority', ''),
            'lead_score': lead_data.get('lead_score', 0),
            'process_type': lead_data.get('process_type', ''),
            'workspace_dimensions': lead_data.get('workspace_dimensions', ''),
            'automation_suitability': lead_data.get('automation_suitability', ''),
        }

        response = requests.post(
            GOOGLE_SHEETS_WEBHOOK,
            json=row_data,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )

        if response.status_code == 200:
            print(f"Lead {lead_data.get('lead_id')} saved to Google Sheets")
            return True
        else:
            print(f"Google Sheets error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")
        return False


# ---------------------------------------------------------------------------
# PDF Lead Deck Generation
# ---------------------------------------------------------------------------

def generate_lead_deck_pdf(lead_data):
    """
    Generate a professional PDF lead deck for integrators.
    Uses ReportLab to match the Robofolio Lead template format.
    Returns the file path of the generated PDF, or None on failure.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.lib.colors import HexColor, white
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_RIGHT, TA_CENTER
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            PageBreak, HRFlowable
        )

        # Colors
        NAVY = HexColor("#1B3A5C")
        LIGHT_BG = HexColor("#F5F7FA")
        BORDER = HexColor("#D0D5DD")
        TEXT_DARK = HexColor("#1a1a1a")
        TEXT_MED = HexColor("#4a4a4a")
        TEXT_LIGHT = HexColor("#6B7280")
        GREEN_BG = HexColor("#E8F5E9")
        GREEN_LT = HexColor("#F0FAF0")
        GREEN_ACC = HexColor("#2E7D32")
        WIDTH, HEIGHT = A4
        margin_w = WIDTH - 40 * mm

        def _s(name, **kw):
            return ParagraphStyle(name, **kw)

        S = {
            'logo': _s('Logo', fontName='Helvetica-Bold', fontSize=22, textColor=NAVY),
            'lead_id': _s('LeadId', fontName='Helvetica', fontSize=9, textColor=TEXT_LIGHT, alignment=TA_RIGHT),
            'section': _s('Sect', fontName='Helvetica-Bold', fontSize=13, textColor=NAVY, spaceBefore=6*mm, spaceAfter=3*mm),
            'company': _s('Co', fontName='Helvetica-Bold', fontSize=14, textColor=TEXT_DARK),
            'iv': _s('IV', fontName='Helvetica', fontSize=9, textColor=TEXT_DARK, leading=13),
            'fl': _s('FL', fontName='Helvetica-BoldOblique', fontSize=9, textColor=TEXT_MED),
            'fv': _s('FV', fontName='Helvetica', fontSize=9, textColor=TEXT_DARK, leading=14),
            'bh': _s('BH', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY),
            'bv': _s('BV', fontName='Helvetica', fontSize=9, textColor=TEXT_DARK),
            'bn': _s('BN', fontName='Helvetica', fontSize=8, textColor=TEXT_LIGHT),
            'st': _s('ST', fontName='Helvetica-Bold', fontSize=13, textColor=TEXT_DARK),
            'sn': _s('SN', fontName='Helvetica', fontSize=9, textColor=TEXT_MED),
            'gt': _s('GT', fontName='Helvetica-Bold', fontSize=13, textColor=GREEN_ACC),
            'gv': _s('GV', fontName='Helvetica', fontSize=9, textColor=TEXT_DARK, leading=14),
            'foot': _s('FT', fontName='Helvetica-Oblique', fontSize=8, textColor=TEXT_LIGHT, alignment=TA_CENTER),
        }

        lead_id = lead_data.get('lead_id', 'RF-000')
        date_str = lead_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        score = lead_data.get('lead_score', 0)
        score_label = 'High' if score >= 75 else 'Medium' if score >= 50 else 'Low'

        # Ensure output directory exists
        pdf_dir = os.environ.get('PDF_OUTPUT_DIR', '/tmp/robofolio_leads')
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_path = os.path.join(pdf_dir, f"{lead_id}.pdf")

        doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                                leftMargin=20*mm, rightMargin=20*mm,
                                topMargin=18*mm, bottomMargin=18*mm)
        story = []

        # ---- PAGE 1 ----
        # Header
        hdr = [[Paragraph("ROBOFOLIO", S['logo']),
                 Paragraph(f"Lead ID: {lead_id}<br/>Generated: {date_str}", S['lead_id'])]]
        t = Table(hdr, colWidths=[margin_w*0.5, margin_w*0.5])
        t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                                ('LEFTPADDING',(0,0),(-1,-1),0),
                                ('RIGHTPADDING',(0,0),(-1,-1),0)]))
        story.append(t)
        story.append(Spacer(1, 6*mm))
        story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=5*mm))

        # Company + Contact
        half = margin_w * 0.5
        story.append(Table(
            [[Paragraph("COMPANY INFORMATION", S['section']),
              Paragraph("PRIMARY CONTACT", S['section'])]],
            colWidths=[half, half]
        ))
        story.append(Spacer(1, 2*mm))

        info = [
            [Paragraph(lead_data.get('company_name', 'Unknown'), S['company']),
             Paragraph(lead_data.get('contact_name', 'tbd'), S['company'])],
            [Paragraph(f"<font color='#6B7280'>Industry:</font> {lead_data.get('industry','Unknown')}", S['iv']),
             Paragraph(f"<font color='#6B7280'>Title:</font> {lead_data.get('contact_title','tbd')}", S['iv'])],
            [Paragraph(f"<font color='#6B7280'>Location:</font> {lead_data.get('location','Unknown')}", S['iv']),
             Paragraph(f"<font color='#6B7280'>Email:</font> {lead_data.get('contact_email','tbd')}", S['iv'])],
            [Paragraph(f"<font color='#6B7280'>Size:</font> {lead_data.get('company_size','Unknown')}", S['iv']),
             Paragraph(f"<font color='#6B7280'>Phone:</font> {lead_data.get('contact_phone','tbd')}", S['iv'])],
        ]
        it = Table(info, colWidths=[half, half])
        it.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),3*mm), ('RIGHTPADDING',(0,0),(-1,-1),3*mm),
            ('TOPPADDING',(0,0),(-1,-1),2*mm), ('BOTTOMPADDING',(0,0),(-1,-1),2*mm),
            ('BOX',(0,0),(0,-1),0.5,BORDER), ('BOX',(1,0),(1,-1),0.5,BORDER),
            ('BACKGROUND',(0,0),(-1,-1),LIGHT_BG),
        ]))
        story.append(it)
        story.append(Spacer(1, 6*mm))

        # Project Overview
        story.append(Paragraph("PROJECT OVERVIEW", S['section']))
        story.append(Spacer(1, 2*mm))
        ov = [
            [Paragraph("<b>Application Type:</b>", S['fl']),
             Paragraph(lead_data.get('application_type', 'Unknown'), S['fv'])],
            [Paragraph("<b>Primary Goal:</b>", S['fl']),
             Paragraph(lead_data.get('primary_goal', 'Not specified'), S['fv'])],
            [Paragraph("<b>Current Process:</b>", S['fl']),
             Paragraph(lead_data.get('current_process', 'Not specified'), S['fv'])],
        ]
        ovt = Table(ov, colWidths=[35*mm, margin_w-35*mm])
        ovt.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(0,-1),3*mm), ('LEFTPADDING',(1,0),(1,-1),5*mm),
            ('RIGHTPADDING',(0,0),(-1,-1),3*mm),
            ('TOPPADDING',(0,0),(-1,-1),3*mm), ('BOTTOMPADDING',(0,0),(-1,-1),3*mm),
            ('BOX',(0,0),(-1,-1),0.5,BORDER),
            ('LINEBELOW',(0,0),(-1,0),0.5,BORDER), ('LINEBELOW',(0,1),(-1,1),0.5,BORDER),
            ('BACKGROUND',(0,0),(0,-1),LIGHT_BG),
        ]))
        story.append(ovt)
        story.append(Spacer(1, 6*mm))

        # BANT
        story.append(Paragraph("QUALIFICATION (BANT)", S['section']))
        story.append(Spacer(1, 2*mm))
        third = margin_w / 3
        budget_display = lead_data.get('budget_range', 'Unknown')
        timeline_map = {'0-3months':'0-3 months','3-6months':'3-6 months',
                        '6-12months':'6-12 months','12+months':'12+ months'}
        timeline_display = timeline_map.get(lead_data.get('timeline',''), lead_data.get('timeline','Unknown'))
        authority_map = {'decision-maker':'Decision maker','1-approval':'1 approval needed',
                         '2+-approvals':'2+ approvals','committee':'Committee'}
        authority_display = authority_map.get(lead_data.get('authority',''), lead_data.get('authority','Unknown'))
        bt = [
            [Paragraph("BUDGET", S['bh']), Paragraph("AUTHORITY", S['bh']), Paragraph("TIMELINE", S['bh'])],
            [Paragraph(budget_display, S['bv']), Paragraph(authority_display, S['bv']), Paragraph(timeline_display, S['bv'])],
            [Paragraph(lead_data.get('budget_status','').replace('-',' ').title(), S['bn']),
             Paragraph("", S['bn']),
             Paragraph("", S['bn'])],
        ]
        btt = Table(bt, colWidths=[third, third, third])
        btt.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),3*mm), ('RIGHTPADDING',(0,0),(-1,-1),3*mm),
            ('TOPPADDING',(0,0),(-1,0),3*mm), ('TOPPADDING',(0,1),(-1,1),4*mm),
            ('BOTTOMPADDING',(0,0),(-1,-1),3*mm),
            ('BOX',(0,0),(-1,-1),0.5,BORDER),
            ('LINEBELOW',(0,0),(-1,0),0.5,NAVY),
            ('LINEBEFORE',(1,0),(1,-1),0.5,BORDER),
            ('LINEBEFORE',(2,0),(2,-1),0.5,BORDER),
            ('BACKGROUND',(0,0),(-1,0),LIGHT_BG),
        ]))
        story.append(btt)

        story.append(PageBreak())

        # ---- PAGE 2 ----
        story.append(Spacer(1, 6*mm))

        # Score + Next Steps
        sc_inner = [[Paragraph(f"<b>LEAD SCORE: {score}/100</b>", S['st'])],
                     [Paragraph(f"{score_label}: Based on BANT qualification and technical data completeness.", S['sn'])]]
        sc_t = Table(sc_inner, colWidths=[half-8*mm])
        sc_t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                                   ('LEFTPADDING',(0,0),(-1,-1),4*mm), ('TOPPADDING',(0,0),(0,0),4*mm),
                                   ('BOTTOMPADDING',(-1,-1),(-1,-1),4*mm)]))

        ns_inner = [[Paragraph("<b>NEXT STEPS</b>", S['gt'])],
                     [Paragraph("1) Schedule discovery call within 48 hours "
                                "2) Request floor plan and current process video "
                                "3) Prepare preliminary ROI analysis", S['gv'])]]
        ns_t = Table(ns_inner, colWidths=[half-8*mm])
        ns_t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                                   ('LEFTPADDING',(0,0),(-1,-1),4*mm), ('TOPPADDING',(0,0),(0,0),4*mm),
                                   ('BOTTOMPADDING',(-1,-1),(-1,-1),4*mm)]))

        combo = Table([[sc_t, ns_t]], colWidths=[half, half])
        combo.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('BACKGROUND',(0,0),(0,0),GREEN_BG), ('BACKGROUND',(1,0),(1,0),GREEN_LT),
            ('BOX',(0,0),(-1,-1),0.5,BORDER), ('LINEBEFORE',(1,0),(1,0),0.5,BORDER),
            ('LEFTPADDING',(0,0),(-1,-1),0), ('RIGHTPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0), ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ]))
        story.append(combo)
        story.append(Spacer(1, 10*mm))

        story.append(Paragraph(
            f"This lead has been pre-qualified by Robofolio. "
            f"Respond within 24 hours for best conversion rates.",
            S['foot']))

        doc.build(story)
        print(f"PDF lead deck generated: {pdf_path}")
        return pdf_path

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None


# ---------------------------------------------------------------------------
# Email Notifications
# ---------------------------------------------------------------------------

def send_lead_confirmation_email(lead_data):
    """
    Send auto-confirmation email to the lead (manufacturer) after submission.
    """
    contact_email = lead_data.get('contact_email', '')
    if not contact_email or not SMTP_USER:
        print("WARN: No contact email or SMTP not configured, skipping confirmation email")
        return False

    try:
        contact_name = lead_data.get('contact_name', 'there')
        app_type = lead_data.get('application_type', 'your project')
        industry = lead_data.get('industry', '')
        timeline = lead_data.get('timeline', '')
        lead_id = lead_data.get('lead_id', '')
        language = lead_data.get('language', 'de')

        if language == 'de':
            subject = f"Ihre Anfrage bei Robofolio — Wir verbinden Sie mit Integratoren ({lead_id})"
            body = f"""Hallo {contact_name},

vielen Dank fuer Ihre Anfrage ueber Robofolio!

Wir haben Ihr Projekt erhalten und verbinden Sie jetzt mit 2-3 spezialisierten Robotik-Integratoren, die perfekt zu Ihren Anforderungen passen.

Ihr Projekt:
- Anwendung: {app_type}
- Branche: {industry}
- Timeline: {timeline}

Was passiert als Naechstes:
1. Wir senden Ihr Projekt an passende Integratoren (heute)
2. Sie erhalten Kontakt von Integratoren innerhalb von 48 Stunden
3. Sie koennen Angebote vergleichen und den besten Partner auswaehlen

Haben Sie Fragen? Antworten Sie einfach auf diese E-Mail.

Beste Gruesse,
Das Robofolio Team

P.S. Dieser Service ist fuer Sie 100% kostenlos.
"""
        else:
            subject = f"Your Robofolio inquiry — We're connecting you with integrators ({lead_id})"
            body = f"""Hello {contact_name},

Thank you for your inquiry through Robofolio!

We have received your project and are now connecting you with 2-3 specialized robotics integrators that are a perfect fit for your requirements.

Your Project:
- Application: {app_type}
- Industry: {industry}
- Timeline: {timeline}

What happens next:
1. We send your project to matching integrators (today)
2. You will hear from integrators within 48 hours
3. You can compare proposals and choose the best partner

Have questions? Simply reply to this email.

Best regards,
The Robofolio Team

P.S. This service is 100% free for you.
"""

        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = contact_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        print(f"Confirmation email sent to {contact_email}")
        return True

    except Exception as e:
        print(f"Error sending confirmation email: {e}")
        return False


def send_integrator_notification_emails(lead_data, pdf_path=None):
    """
    Send lead notification emails to matched integrators.
    In MVP, sends to a configured list; later uses the matching algorithm.
    """
    if not SMTP_USER:
        print("WARN: SMTP not configured, skipping integrator notifications")
        return False

    # MVP: Use a static list of integrator emails from environment
    # In production, this would come from the matching algorithm
    integrator_emails_str = os.environ.get('INTEGRATOR_EMAILS', '')
    if not integrator_emails_str:
        print("WARN: No INTEGRATOR_EMAILS configured")
        return False

    integrator_emails = [e.strip() for e in integrator_emails_str.split(',') if e.strip()]

    lead_id = lead_data.get('lead_id', '')
    score = lead_data.get('lead_score', 0)
    score_tier = 'HOT' if score >= 75 else 'WARM' if score >= 50 else 'COOL'
    company = lead_data.get('company_name', 'Unknown')
    app_type = lead_data.get('application_type', 'Unknown')
    industry = lead_data.get('industry', 'Unknown')
    location = lead_data.get('location', 'Unknown')
    budget = lead_data.get('budget_range', 'Unknown')
    timeline = lead_data.get('timeline', 'Unknown')
    contact_name = lead_data.get('contact_name', 'tbd')
    contact_title = lead_data.get('contact_title', '')
    contact_email = lead_data.get('contact_email', 'tbd')
    contact_phone = lead_data.get('contact_phone', 'tbd')

    subject = f"Neuer qualifizierter Lead: {app_type} fuer {company} (Score: {score}/100) — {score_tier}"
    body = f"""Hallo,

Sie haben einen neuen qualifizierten Lead ueber Robofolio erhalten!

Lead Score: {score}/100 — {score_tier} LEAD

Firma: {company}
Standort: {location}
Branche: {industry}
Anwendung: {app_type}
Budget: {budget}
Timeline: {timeline}

NEXT STEPS:
Kontaktieren Sie den Lead innerhalb von 24 Stunden fuer beste Conversion-Raten.

Kontaktdaten:
- Name: {contact_name} ({contact_title})
- E-Mail: {contact_email}
- Telefon: {contact_phone}

Der Lead erwartet Ihre Kontaktaufnahme.

Viel Erfolg!
Das Robofolio Team

---
Lead ID: {lead_id}
"""

    sent_count = 0
    for email in integrator_emails:
        try:
            msg = MIMEMultipart()
            msg['From'] = SMTP_USER
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # Attach PDF if available
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    pdf_attach = MIMEApplication(f.read(), _subtype='pdf')
                    pdf_attach.add_header('Content-Disposition', 'attachment',
                                          filename=f'{lead_id}_Lead_Deck.pdf')
                    msg.attach(pdf_attach)

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)

            sent_count += 1
            print(f"Lead notification sent to integrator: {email}")

        except Exception as e:
            print(f"Error sending to {email}: {e}")

    print(f"Integrator notifications sent: {sent_count}/{len(integrator_emails)}")
    return sent_count > 0


# ---------------------------------------------------------------------------
# Cobot Solution Database & Matching
# ---------------------------------------------------------------------------

def load_cobot_database():
    """Load the cobot solution database from JSON file"""
    db_path = os.path.join(os.path.dirname(__file__), 'cobot_database.json')
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading cobot database: {e}")
        return None


@app.route('/api/solutions/categories', methods=['GET'])
def get_categories():
    """Return available solution categories and matching fields"""
    db = load_cobot_database()
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 500

    # Build category summaries with counts and price ranges
    category_info = {}
    for sol in db['solutions']:
        cat = sol.get('Kategorie', '')
        if cat not in category_info:
            category_info[cat] = {'count': 0, 'prices': [], 'providers': set()}
        category_info[cat]['count'] += 1
        price = sol.get('Preis ca. (EUR)')
        if price:
            try:
                category_info[cat]['prices'].append(float(str(price).replace('.', '').replace(',', '.')))
            except (ValueError, TypeError):
                pass
        provider = sol.get('Lösungsanbieter', '')
        if provider:
            category_info[cat]['providers'].add(provider)

    categories = []
    cat_labels_de = {
        'Schweißen': {'icon': '🔥', 'label_en': 'Welding'},
        'Palettierung': {'icon': '📦', 'label_en': 'Palletizing'},
        'Maschinenbeschickung': {'icon': '⚙️', 'label_en': 'Machine Tending'},
        'Kleben / Dosieren': {'icon': '💧', 'label_en': 'Gluing / Dispensing'},
        'Verschrauben': {'icon': '🔩', 'label_en': 'Screw Driving'},
        'Inspektion / Vision': {'icon': '👁️', 'label_en': 'Inspection / Vision'},
        'Lackieren': {'icon': '🎨', 'label_en': 'Painting'},
    }
    for cat, info in category_info.items():
        prices = info['prices']
        meta = cat_labels_de.get(cat, {'icon': '🤖', 'label_en': cat})
        categories.append({
            'name': cat,
            'name_en': meta['label_en'],
            'icon': meta['icon'],
            'solution_count': info['count'],
            'provider_count': len(info['providers']),
            'price_range': {
                'min': int(min(prices)) if prices else None,
                'max': int(max(prices)) if prices else None,
            }
        })

    return jsonify({
        'success': True,
        'categories': sorted(categories, key=lambda x: x['solution_count'], reverse=True),
        'matching_fields': db.get('matching_fields', []),
        'total_solutions': len(db['solutions']),
        'total_partners': len(db.get('german_partners', []))
    })


@app.route('/api/match-solutions', methods=['POST'])
def match_solutions():
    """
    Direct Search: Match solutions based on user specifications.
    Expects JSON with: category, max_weight, reach, precision, environment, budget, industry
    """
    try:
        data = request.get_json()
        category = data.get('category', '')
        max_weight = data.get('max_weight')
        budget_max = data.get('budget_max')
        industry = data.get('industry', '')
        region = data.get('region', 'Europa')

        db = load_cobot_database()
        if not db:
            return jsonify({'success': False, 'error': 'Database not available'}), 500

        # Filter solutions
        matches = []
        for sol in db['solutions']:
            score = 0
            reasons = []

            # Category match (required)
            if category and sol.get('Kategorie', '').lower() != category.lower():
                continue
            score += 40
            reasons.append(f"Kategorie: {sol.get('Kategorie')}")

            # Region preference
            sol_region = sol.get('Region') or ''
            if region and sol_region and sol_region.lower() == region.lower():
                score += 10
                reasons.append(f"Region: {sol_region}")

            # Payload capacity check
            sol_payload = sol.get('Max. Nutzlast (kg)')
            if max_weight and sol_payload:
                try:
                    payload_val = float(str(sol_payload).replace(',', '.'))
                    weight_val = float(max_weight)
                    if payload_val >= weight_val:
                        score += 20
                        reasons.append(f"Nutzlast {payload_val} kg ≥ {weight_val} kg")
                    else:
                        score -= 10
                        reasons.append(f"Nutzlast {payload_val} kg < {weight_val} kg (knapp)")
                except (ValueError, TypeError):
                    pass

            # Budget check
            sol_price = sol.get('Preis ca. (EUR)')
            if budget_max and sol_price:
                try:
                    price_val = float(str(sol_price).replace('.', '').replace(',', '.'))
                    budget_val = float(str(budget_max).replace('.', '').replace(',', '.'))
                    if price_val <= budget_val:
                        score += 20
                        reasons.append(f"Preis €{int(price_val):,} im Budget")
                    elif price_val <= budget_val * 1.2:
                        score += 10
                        reasons.append(f"Preis €{int(price_val):,} knapp über Budget")
                    else:
                        score -= 5
                        reasons.append(f"Preis €{int(price_val):,} über Budget")
                except (ValueError, TypeError):
                    pass

            # Industry fit
            if industry and sol.get('Brancheneignung'):
                eignung = (sol.get('Brancheneignung') or '').lower()
                if industry.lower() in eignung or 'alle' in eignung or 'universal' in eignung:
                    score += 10
                    reasons.append("Branche passt")

            matches.append({
                'solution': {
                    'id': sol.get('ID'),
                    'name': sol.get('Lösungsname'),
                    'provider': sol.get('Lösungsanbieter'),
                    'category': sol.get('Kategorie'),
                    'robot': sol.get('Roboter inklusive'),
                    'manufacturer': sol.get('Cobot-Hersteller'),
                    'payload_kg': sol.get('Max. Nutzlast (kg)'),
                    'components': sol.get('Enthaltene Komponenten'),
                    'software': sol.get('Software'),
                    'price_eur': sol.get('Preis ca. (EUR)'),
                    'setup_time': sol.get('Einrichtungszeit'),
                    'roi_months': sol.get('ROI (Monate)'),
                    'industries': sol.get('Brancheneignung'),
                    'features': sol.get('Besondere Merkmale'),
                    'website': sol.get('Website'),
                },
                'match_score': max(0, min(100, score)),
                'match_reasons': reasons,
            })

        # Sort by score descending, return top 5
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        top_matches = matches[:5]

        # Find matching German partners for the category
        partners = []
        for p in db.get('german_partners', []):
            branche = (p.get('Branche') or '').lower()
            cat_lower = (category or '').lower()
            if cat_lower in branche or 'robotik' in branche or 'automation' in branche:
                partners.append({
                    'name': p.get('Partner'),
                    'region': p.get('Region'),
                    'opportunities': p.get('Anz. Opportunities'),
                    'rank': p.get('Rang'),
                })
            if len(partners) >= 3:
                break

        return jsonify({
            'success': True,
            'matches': top_matches,
            'total_in_category': len([s for s in db['solutions'] if (s.get('Kategorie') or '').lower() == (category or '').lower()]),
            'suggested_partners': partners,
        })

    except Exception as e:
        print(f"Error in match-solutions: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/discovery-analysis', methods=['POST'])
def discovery_analysis():
    """
    Discovery Path: AI analyzes company website/photos and identifies automation potential.
    Uses Claude to map findings to solution categories from the database.
    """
    try:
        data = request.get_json()
        website_data = data.get('website_analysis', {})
        photo_analysis = data.get('photo_analysis', '')
        company_info = data.get('company_info', {})

        if not ANTHROPIC_API_KEY:
            return jsonify({'success': False, 'error': 'API key not configured'}), 500

        db = load_cobot_database()
        if not db:
            return jsonify({'success': False, 'error': 'Database not available'}), 500

        # Build context about available solutions
        categories_summary = {}
        for sol in db['solutions']:
            cat = sol.get('Kategorie', '')
            if cat not in categories_summary:
                categories_summary[cat] = {
                    'solutions': [],
                    'price_range': [],
                    'roi_range': [],
                }
            categories_summary[cat]['solutions'].append(sol.get('Lösungsname', ''))
            price = sol.get('Preis ca. (EUR)')
            if price:
                try:
                    categories_summary[cat]['price_range'].append(float(str(price).replace('.', '').replace(',', '.')))
                except:
                    pass
            roi = sol.get('ROI (Monate)')
            if roi:
                categories_summary[cat]['roi_range'].append(str(roi))

        cat_context = ""
        for cat, info in categories_summary.items():
            prices = info['price_range']
            price_str = f"€{int(min(prices)):,} – €{int(max(prices)):,}" if prices else "auf Anfrage"
            cat_context += f"\n- {cat}: {len(info['solutions'])} Lösungen, Preis {price_str}, ROI {', '.join(set(info['roi_range']))}"

        discovery_prompt = f"""Du bist ein Automatisierungsberater für Robofolio, einen Marktplatz für Robotik-Komplettlösungen.

Analysiere die folgenden Informationen über ein Unternehmen und identifiziere konkrete Automatisierungspotenziale.

UNTERNEHMENSDATEN:
- Branche: {company_info.get('industry', 'Unbekannt')}
- Größe: {company_info.get('company_size', 'Unbekannt')}
- Produkte: {company_info.get('main_products', 'Unbekannt')}
- Aktueller Automatisierungsgrad: {company_info.get('automation_level', 'Unbekannt')}

WEBSITE-ANALYSE:
{json.dumps(website_data, ensure_ascii=False, indent=2)[:3000]}

FOTO-ANALYSE:
{photo_analysis[:3000] if photo_analysis else 'Keine Fotos analysiert'}

VERFÜGBARE LÖSUNGSKATEGORIEN:{cat_context}

Antworte als JSON mit folgendem Format:
{{
  "automation_potential": "high" | "medium" | "low",
  "summary_de": "Kurze Zusammenfassung des Automatisierungspotenzials (2-3 Sätze, Deutsch)",
  "summary_en": "Short summary of automation potential (2-3 sentences, English)",
  "opportunities": [
    {{
      "category": "Exakte Kategorie aus der Liste oben",
      "title_de": "Konkreter Anwendungsfall (Deutsch)",
      "title_en": "Specific use case (English)",
      "description_de": "Warum diese Automatisierung sinnvoll ist (Deutsch)",
      "description_en": "Why this automation makes sense (English)",
      "estimated_roi_months": "10-14",
      "priority": "high" | "medium" | "low",
      "estimated_savings_percent": 30
    }}
  ],
  "recommended_next_steps_de": ["Schritt 1", "Schritt 2"],
  "recommended_next_steps_en": ["Step 1", "Step 2"]
}}

Identifiziere 2-4 konkrete Automatisierungsmöglichkeiten basierend auf der Branche und den verfügbaren Daten. Sei realistisch und spezifisch."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{"role": "user", "content": discovery_prompt}]
        )

        response_text = message.content[0].text
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0]

        analysis = json.loads(response_text.strip())

        # Enrich opportunities with solution data from DB
        for opp in analysis.get('opportunities', []):
            cat = opp.get('category', '')
            matching_solutions = [s for s in db['solutions'] if s.get('Kategorie', '') == cat]
            opp['available_solutions'] = len(matching_solutions)
            if matching_solutions:
                prices = []
                for s in matching_solutions:
                    p = s.get('Preis ca. (EUR)')
                    if p:
                        try:
                            prices.append(float(str(p).replace('.', '').replace(',', '.')))
                        except:
                            pass
                if prices:
                    opp['price_range'] = {'min': int(min(prices)), 'max': int(max(prices))}
                # Include top solution name
                opp['top_solution'] = matching_solutions[0].get('Lösungsname', '')

        return jsonify({
            'success': True,
            'analysis': analysis,
            'database_info': {
                'total_solutions': len(db['solutions']),
                'total_categories': len(db['categories']),
                'total_partners': len(db.get('german_partners', [])),
            }
        })

    except json.JSONDecodeError as e:
        print(f"JSON parse error in discovery: {e}")
        return jsonify({'success': False, 'error': 'Could not parse AI response'}), 500
    except Exception as e:
        print(f"Error in discovery-analysis: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    db = load_cobot_database()
    return jsonify({
        'status': 'healthy',
        'service': 'robofolio-api',
        'api_key_configured': bool(ANTHROPIC_API_KEY),
        'environment': 'production' if IS_PRODUCTION else 'development',
        'database_loaded': db is not None,
        'solutions_count': len(db['solutions']) if db else 0,
    })


if __name__ == '__main__':
    # Check for required environment variables
    if not ANTHROPIC_API_KEY:
        print("WARNING: ANTHROPIC_API_KEY not set. Set it with:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")

    print("Starting Robofolio AI API...")
    print(f"Anthropic API Key configured: {bool(ANTHROPIC_API_KEY)}")
    print(f"Jina API Key configured: {bool(JINA_API_KEY)} (optional)")

    port = int(os.environ.get('PORT', 5001))
    debug = not IS_PRODUCTION
    app.run(debug=debug, host='0.0.0.0', port=port)
