# Robofolio Lead Capture & Qualification Strategy

## Overview

This document outlines the complete lead capture strategy, from landing page form → data collection → lead deck generation for integrators.

## What Integrators Need (Based on Research)

Based on industry research and RFQ best practices, robotics integrators need this information to qualify a lead:

### 1. **BANT Qualification** (Budget, Authority, Need, Timeline)
- **Budget**: Estimated project budget range
- **Authority**: Who makes the decision? Who needs to approve?
- **Need**: What problem are they solving? Why now?
- **Timeline**: When do they need this operational?

### 2. **Technical Specifications**
- Application type (pick & place, welding, palletizing, inspection, etc.)
- Production volume requirements
- Cycle time targets
- Current process description
- Physical constraints (space, environment, safety)
- Integration requirements (MES, ERP, existing equipment)

### 3. **Company Context**
- Industry vertical
- Company size/revenue
- Location (for on-site visits, regulations)
- Current automation maturity

### 4. **Project Scope**
- Primary goals/KPIs
- Success criteria
- Required vs. nice-to-have features
- Compliance/standards requirements (ISO, ANSI, CE, etc.)

## The Multi-Step Form Strategy

### Problem with Current Single-Page Form
Our current 5-field form collects:
1. Name
2. Email
3. Company
4. Industry
5. Brief description

**This is NOT enough to generate a high-quality lead deck!**

### Solution: Multi-Step Progressive Form

#### **Step 1: Basic Contact Info** (Low barrier)
- Name
- Email
- Company name
- Phone (optional)

**CTA:** "Next: Tell us about your project" (70% completion rate expected)

#### **Step 2: Project Overview** (Qualification)
- Industry dropdown (Automotive, Food & Beverage, Logistics, Electronics, etc.)
- Application type dropdown (Pick & Place, Palletizing, Welding, Assembly, Inspection, Material Handling, Other)
- Primary goal (free text, 2-3 sentences)
  - Placeholder: "e.g., Reduce manual handling in our packaging line to increase throughput by 30%"
- Current process description (free text, 2-3 sentences)
  - Placeholder: "e.g., Currently using 3 workers to manually load parts onto conveyor. 200 parts/hour capacity."

**CTA:** "Next: Project requirements" (60% completion rate expected)

#### **Step 3: Technical Requirements** (Deep qualification)
- Production volume target
  - Dropdown: "<100 parts/hr", "100-500 parts/hr", "500-1000 parts/hr", "1000+ parts/hr"
- Desired cycle time (if known)
  - Input with unit selector (seconds/minutes per part)
- Physical constraints
  - Checkboxes: "Limited floor space", "High temperature environment", "Cleanroom required", "Shared workspace (cobot needed)", "None"
- Integration requirements
  - Checkboxes: "Must integrate with existing MES", "Must integrate with ERP", "Vision system required", "Force/torque sensing required", "None"

**CTA:** "Next: Timeline & budget" (50% completion rate expected)

#### **Step 4: BANT Qualification** (Critical for integrators)
- Project timeline
  - Radio buttons: "Within 3 months", "3-6 months", "6-12 months", "12+ months", "Just exploring"
- Urgency
  - Radio: "Fixed deadline (regulatory, contract, etc.)", "Soft deadline (internal goal)", "Flexible timeline"
- Budget status
  - Radio: "Budget approved", "Budget in approval process", "Need ROI justification", "Just researching costs"
- Estimated budget range
  - Dropdown: "€50K-€100K", "€100K-€250K", "€250K-€500K", "€500K+", "Unsure"
- Decision-making process
  - Radio: "I'm the decision maker", "I need 1 approval", "I need 2+ approvals", "Committee decision"

**CTA:** "Get my matches" (Complete form)

### Form Completion Funnel Expectations

| Step | Expected Completion | Cumulative |
|------|---------------------|------------|
| Step 1 (Contact) | 70% | 70% |
| Step 2 (Project) | 85% | 60% |
| Step 3 (Technical) | 80% | 48% |
| Step 4 (BANT) | 90% | 43% |

**Final conversion rate: 40-45% of form starters complete all steps**

This is BETTER than a long single-page form (which might have 15-20% completion) because:
- Lower initial barrier
- Commitment escalation (sunk cost)
- Progress bar motivation
- Ability to save partial leads

## Lead Scoring System

Once form is submitted, automatically calculate a lead score (0-100):

### Scoring Criteria

**Budget (30 points)**
- Budget approved: 30 points
- Budget in approval: 20 points
- Need ROI justification: 10 points
- Just researching: 5 points

**Timeline (25 points)**
- Within 3 months + fixed deadline: 25 points
- 3-6 months + fixed deadline: 20 points
- 6-12 months: 15 points
- 12+ months: 10 points
- Just exploring: 5 points

**Authority (20 points)**
- I'm the decision maker: 20 points
- Need 1 approval: 15 points
- Need 2+ approvals: 10 points
- Committee decision: 5 points

**Technical Clarity (15 points)**
- Clear volume + cycle time + constraints: 15 points
- Volume + cycle time OR constraints: 10 points
- Vague requirements: 5 points

**Company Fit (10 points)**
- Mittelstand (€10M-€500M revenue): 10 points
- Larger enterprise: 7 points
- Smaller company: 5 points

### Lead Grade Tiers

- **90-100: Hot Lead** - Budget approved, clear timeline, decision maker
- **70-89: Warm Lead** - Good fit, needs some qualification
- **50-69: Cool Lead** - Early stage, longer nurture needed
- **0-49: Cold Lead** - Research phase, low intent

## Lead Deck Generation

When a lead submits the form:

1. **Immediately**: Send confirmation email to lead
2. **Within 1 minute**: Generate PDF lead deck using `lead_deck_generator.py`
3. **Within 2 minutes**: Send lead deck to 2-3 matched integrators + notification email
4. **Within 24 hours**: Follow up with lead to confirm receipt and set expectations

### Lead Deck Contents (One-Page PDF)

The generated PDF includes:

**Header:**
- Robofolio branding
- Lead ID (unique)
- Date generated

**Company & Contact:**
- Company name, industry, location, revenue estimate
- Contact name, title, email, phone

**Project Overview:**
- Application type
- Primary goal
- Current process description

**BANT Qualification:**
- Budget range + status
- Decision-making authority
- Timeline + urgency level

**Technical Requirements:**
- Required features
- Production volume
- Cycle time targets
- Constraints/environment

**Lead Score + Next Steps:**
- Score (0-100) with rationale
- Recommended next actions for integrator

## Data Flow Architecture

```
Landing Page Form (Multi-step)
        ↓
Google Sheets (Raw data capture)
        ↓
Google Apps Script Trigger
        ↓
Lead Scoring Logic (Calculate score)
        ↓
Lead Deck Generator (Python + Reportlab)
        ↓
PDF Saved to Google Drive
        ↓
Email to Matched Integrators (Gmail API)
        ↓
Email to Lead (Auto-confirmation)
```

### Implementation Options

**Option A: Fully Automated (Recommended for MVP)**
- Use Google Apps Script for everything
- Store PDFs in Google Drive
- Use MailApp for emails
- Pros: No server needed, free, integrated
- Cons: Limited to Google ecosystem

**Option B: Hybrid (Scale-up option)**
- Google Sheets captures form data
- Zapier/Make triggers Python script on submission
- Python generates PDF, uploads to Drive
- SendGrid sends emails to integrators
- Pros: More flexible, better for scale
- Cons: Costs money, more complex

**Option C: Full Backend (Future)**
- Custom backend (Node.js/Python)
- PostgreSQL database
- Redis for lead matching queue
- AWS S3 for PDF storage
- Pros: Full control, scalable
- Cons: Expensive, requires dev resources

**For MVP: Start with Option A**

## Integrator Matching Logic

When a lead submits, match with 2-3 integrators based on:

1. **Geographic proximity** (Bavaria, Baden-Württemberg, DACH)
2. **Industry specialization** (automotive, food & bev, logistics, etc.)
3. **Application expertise** (pick & place, palletizing, welding, etc.)
4. **Company size fit** (small integrators for small companies, large for enterprise)
5. **Availability** (current capacity, project load)

### Matching Algorithm (Simple MVP version)

```
For each new lead:
  1. Filter integrators by geography (within 200km preferred)
  2. Filter by industry match (exact > adjacent > general)
  3. Filter by application type (exact match only)
  4. Rank by:
     - Lead response rate (historical)
     - Average deal close rate
     - Customer ratings
     - Last lead sent (rotate to prevent overload)
  5. Select top 3 integrators
  6. Send lead deck to all 3
  7. First to respond within 24 hours gets priority intro to lead
```

## Email Templates

### To Lead (Auto-confirmation)

**Subject:** [DE] Ihre Anfrage bei Robofolio - Wir verbinden Sie mit Integratoren

**Body:**
```
Hallo [Name],

vielen Dank für Ihre Anfrage über Robofolio!

Wir haben Ihr Projekt erhalten und verbinden Sie jetzt mit 2-3 spezialisierten Robotik-Integratoren, die perfekt zu Ihren Anforderungen passen.

📋 Ihr Projekt:
- Anwendung: [Application Type]
- Branche: [Industry]
- Timeline: [Timeline]

⏱ Was passiert als Nächstes:
1. Wir senden Ihr Projekt an passende Integratoren (heute)
2. Sie erhalten Kontakt von Integratoren innerhalb von 48 Stunden
3. Sie können Angebote vergleichen und den besten Partner auswählen

Haben Sie Fragen? Antworten Sie einfach auf diese E-Mail.

Beste Grüße,
Das Robofolio Team

P.S. Dieser Service ist für Sie 100% kostenlos.
```

### To Integrator (Lead notification)

**Subject:** [DE] Neuer qualifizierter Lead: [Application] für [Company] (Score: [X]/100)

**Body:**
```
Hallo [Integrator Name],

Sie haben einen neuen qualifizierten Lead über Robofolio erhalten!

🎯 Lead Score: [85]/100 - HOT LEAD

📎 Lead Deck: [Link to PDF]

🏢 Firma: [Company Name]
📍 Standort: [Location]
🏭 Branche: [Industry]
🤖 Anwendung: [Application Type]
💰 Budget: [Budget Range]
📅 Timeline: [Timeline]

✅ NEXT STEPS:
Kontaktieren Sie den Lead innerhalb von 24 Stunden für beste Conversion-Raten.

Kontaktdaten:
- Name: [Contact Name] ([Title])
- E-Mail: [Email]
- Telefon: [Phone]

Der Lead erwartet Ihre Kontaktaufnahme. Bitte bestätigen Sie den Erhalt dieses Leads.

Viel Erfolg!
Das Robofolio Team

---
Sie haben diesen Lead erhalten, weil Sie als [Industry]-Spezialist in [Location] registriert sind.
```

## Key Metrics to Track

### Conversion Funnel
- Landing page visitors
- Form starts (Step 1 initiated)
- Step 1 → Step 2 completion
- Step 2 → Step 3 completion
- Step 3 → Step 4 completion
- Form submissions (complete)

### Lead Quality
- Average lead score
- Distribution by tier (Hot/Warm/Cool/Cold)
- Integrator response rate
- Lead-to-quote conversion
- Lead-to-close conversion

### Integrator Engagement
- Time to first response
- Response rate (% of leads responded to)
- Quote rate (% of responses that become quotes)
- Win rate (% of quotes that close)

## Next Steps for Implementation

1. ✅ **Lead deck PDF template created**
2. 🔲 **Design multi-step form UI**
3. 🔲 **Update landing page with multi-step form**
4. 🔲 **Build Google Apps Script for lead scoring + PDF generation**
5. 🔲 **Create email templates (DE + EN)**
6. 🔲 **Test end-to-end flow with sample data**
7. 🔲 **Build integrator matching logic**
8. 🔲 **Go live!**

---

**Questions? Want to adjust the strategy?** Let's refine this before implementing!
