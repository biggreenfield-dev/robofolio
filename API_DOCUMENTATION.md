# Robofolio API Documentation

**Base URL:** `http://localhost:5000` (local) or your deployed URL
**Version:** 1.0
**Authentication:** None (MVP) — API key auth planned for v2

---

## Endpoints

### `GET /health`

Health check endpoint for monitoring and deployment verification.

**Response (200):**
```json
{ "status": "healthy", "service": "robofolio-api" }
```

---

### `POST /api/analyze-website`

Scrapes and analyzes a company website using Claude AI to extract structured company information.

**Request Body:**
```json
{ "url": "https://example-company.de" }
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "company_name": "Example GmbH",
    "industry": "Automotive parts manufacturing",
    "location": "Munich, Bavaria, Germany",
    "company_size": "Mid-market (€10M-€500M)",
    "main_products": "Precision metal components for automotive OEMs",
    "automation_level": "Semi-automated",
    "production_challenges": "High defect rate on small parts, throughput bottleneck",
    "contact_email": "info@example.de",
    "contact_phone": "+49 89 1234567",
    "language": "de"
  }
}
```

**Error (400):** `{ "error": "URL is required" }`
**Error (500):** `{ "error": "Could not fetch website content" }`

**Notes:** Uses Jina AI Reader for scraping (with API key) or falls back to free Jina / simple HTTP fetch. Website content is truncated to 15,000 characters before analysis.

---

### `POST /api/analyze-photos`

Analyzes up to 5 workspace/production photos using Claude Vision to extract technical details.

**Request:** `multipart/form-data`
- `photos` — up to 5 image files (JPEG, PNG)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "process_type": "Pick & place",
    "current_process_description": "Manual loading of metal parts onto conveyor...",
    "workspace_dimensions": "~4m x 3m",
    "workspace_layout": "Linear",
    "environment_type": "Standard factory floor",
    "existing_equipment": "Conveyor belt, manual workstation, inspection lamp",
    "products_visible": "Small metal components, ~5cm diameter",
    "automation_level": "Fully manual",
    "physical_constraints": "Limited floor space",
    "safety_equipment": "Safety glasses, gloves",
    "ergonomic_concerns": "Repetitive motions, awkward bending",
    "lighting": "Adequate",
    "automation_suitability": "High — repetitive task, standardized parts, sufficient space for cobot"
  }
}
```

**Error (400):** `{ "error": "No photos provided" }`

---

### `POST /api/submit-lead`

Submits a complete lead, triggers scoring, PDF generation, Google Sheets save, and email notifications.

**Request Body:**
```json
{
  "company_name": "Liebherr-Hausgerate GmbH",
  "industry": "Home Appliances / Refrigeration",
  "location": "Germany",
  "company_size": "Large (€500M+)",
  "contact_name": "Josefine",
  "contact_email": "josefine@liebherr.com",
  "contact_phone": "+49 ...",
  "contact_title": "Project Lead",
  "application_type": "Adhesive Tape Application / Door Securing",
  "primary_goal": "Automate manual tape application on refrigerator doors",
  "current_process": "Manual application of 3 tape strips per door, ~75s total",
  "budget_range": "€50K-€100K",
  "budget_status": "approved",
  "timeline": "3-6months",
  "authority": "decision-maker",
  "process_type": "Tape application",
  "workspace_dimensions": "Conveyor line",
  "automation_suitability": "High",
  "language": "de"
}
```

**Response (200):**
```json
{
  "success": true,
  "lead_id": "RF-20260216-042",
  "lead_score": 85,
  "pdf_generated": true,
  "sheets_saved": true,
  "message": "Lead submitted successfully"
}
```

---

## Lead Scoring Algorithm

Score range: 0–100, broken down as follows:

| Factor | Max Points | Criteria |
|--------|-----------|----------|
| Budget | 30 | approved=30, in-process=20, need-roi=10, researching=5 |
| Timeline | 25 | 0-3mo=25, 3-6mo=20, 6-12mo=15, 12+mo=10 |
| Authority | 20 | decision-maker=20, 1-approval=15, 2+-approvals=10, committee=5 |
| Technical Clarity | 15 | Both process+workspace=15, one=10, neither=5 |
| Company Fit | 10 | Mid-market=10, large=7, other=5 |

**Score Tiers:** Hot (75+), Warm (50-74), Cool (25-49), Cold (<25)

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Claude API key for AI analysis |
| `JINA_API_KEY` | No | Jina AI Reader key for better web scraping |
| `SMTP_HOST` | No | Email server (default: smtp.gmail.com) |
| `SMTP_PORT` | No | Email port (default: 587) |
| `SMTP_USER` | No | Email sender address |
| `SMTP_PASS` | No | Email password / app password |
| `GOOGLE_SHEETS_WEBHOOK` | No | Google Apps Script Web App URL |
| `INTEGRATOR_EMAILS` | No | Comma-separated list of integrator emails |
| `PDF_OUTPUT_DIR` | No | Directory for generated PDFs (default: /tmp/robofolio_leads) |

---

## Local Development

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY='sk-ant-...'
python backend_api.py
# Server starts at http://localhost:5000
```

## Testing

```bash
# Health check
curl http://localhost:5000/health

# Analyze website
curl -X POST http://localhost:5000/api/analyze-website \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.de"}'

# Submit lead
curl -X POST http://localhost:5000/api/submit-lead \
  -H "Content-Type: application/json" \
  -d '{"company_name":"Test GmbH","budget_status":"approved","timeline":"3-6months","authority":"decision-maker"}'
```
