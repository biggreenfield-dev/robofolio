# AI-Powered Lead Capture System

## Vision

**Instead of making buyers fill out 20+ form fields, let them:**
1. Drop in their company website URL (10 seconds)
2. Upload a quick video of their production line (30 seconds)
3. Upload 2-3 photos of their workspace (20 seconds)
4. Answer only 3-5 smart questions about what AI couldn't extract (1 minute)

**Total time: 2 minutes vs. 10+ minutes for traditional forms**

This creates a **massive competitive advantage** and a delightful UX that feels like magic.

---

## AI Data Extraction Matrix

### From Company Website (URL Input)

**AI Can Extract:**
- ✅ Company name (from homepage, title tags)
- ✅ Industry/sector (from "About Us", products, services)
- ✅ Location (headquarters, address from contact page)
- ✅ Company size indicators (employee count from LinkedIn, revenue if public)
- ✅ Current products/services (from product pages)
- ✅ Existing automation level (case studies, "our facility" pages)
- ✅ Technology stack (mentioned in tech/innovation pages)
- ✅ Contact information (email, phone from contact page)
- ✅ Language preference (website language → form language)

**AI Extraction Prompt:**
```
Extract the following from this company website:
1. Company name
2. Industry (be specific: "automotive parts manufacturing" not just "manufacturing")
3. Headquarters location (city, region, country)
4. Approximate company size (small <€10M, mid-market €10-500M, large €500M+)
5. Main products/services
6. Current automation level (manual, semi-automated, highly automated)
7. Any mentions of production challenges or goals
8. Primary contact email and phone
9. Does the site mention robotics, automation, or Industry 4.0 initiatives?

Format as JSON.
```

### From Video Upload (Process Documentation)

**AI Can Extract:**
- ✅ Current process type (manual assembly, packaging, welding, inspection, etc.)
- ✅ Cycle time (measure time between parts in video)
- ✅ Workspace dimensions (estimate from video, especially if worker visible for scale)
- ✅ Environmental conditions (indoor/outdoor, temperature visible?, cleanliness)
- ✅ Product type and size (parts being handled)
- ✅ Current throughput (parts per hour from video observation)
- ✅ Ergonomic issues (repetitive motions, heavy lifting, awkward positions)
- ✅ Safety concerns (proximity to hazards, PPE usage)
- ✅ Physical constraints (ceiling height, floor space, existing equipment nearby)
- ✅ Number of workers involved
- ✅ Quality inspection methods (if visible)

**AI Extraction Prompt (Video Analysis):**
```
Analyze this manufacturing/production process video and extract:

PROCESS:
1. What operation is being performed? (e.g., pick & place, welding, assembly, packaging, palletizing, inspection)
2. Describe the current process in 2-3 sentences
3. How many steps are involved?
4. How many workers are performing this task?

TIMING:
5. What is the cycle time? (time to complete one part/unit)
6. Estimated throughput (parts per hour based on observation)

PHYSICAL ENVIRONMENT:
7. Estimated workspace dimensions (length x width x height)
8. Is this a cleanroom, standard factory floor, outdoor, warehouse?
9. Temperature indicators (cold, hot, normal)?
10. Proximity to other equipment or workstations

PRODUCT:
11. What type of product/part is being handled?
12. Approximate size and weight of parts
13. Fragile or robust?

CHALLENGES OBSERVED:
14. Repetitive motions that could be automated?
15. Heavy lifting or ergonomic concerns?
16. Safety hazards visible?
17. Quality control issues visible?

AUTOMATION POTENTIAL:
18. Is this a good candidate for robotic automation? Why or why not?
19. Type of robot likely needed (collaborative, industrial, mobile, gantry)
20. Estimated complexity (simple, moderate, complex)

Format as JSON.
```

### From Photo Uploads (Workspace Documentation)

**AI Can Extract:**
- ✅ Workspace layout and available floor space
- ✅ Ceiling height estimates
- ✅ Existing equipment and machinery
- ✅ Product types and sizes
- ✅ Environmental conditions (clean, dusty, wet, etc.)
- ✅ Current automation level
- ✅ Lighting conditions
- ✅ Accessibility and pathways
- ✅ Utility locations (power, compressed air visible?)
- ✅ Safety equipment present

**AI Extraction Prompt (Image Analysis):**
```
Analyze these workspace photos and extract:

SPACE:
1. Estimated floor space available for automation (in square meters)
2. Estimated ceiling height
3. Layout type (U-shaped, linear, island, etc.)
4. Obstacles or constraints visible?

EXISTING EQUIPMENT:
5. List any existing machinery or equipment visible
6. Are there conveyors, workbenches, or material handling systems?
7. Current automation level (0% manual, 25%, 50%, 75%, fully automated)

ENVIRONMENT:
8. Cleanliness level (cleanroom, standard, industrial, outdoor)
9. Lighting (natural, industrial, dim)
10. Environmental challenges (visible dust, moisture, heat sources)

PRODUCTS:
11. What products or parts are visible?
12. Size and weight estimates
13. Storage methods (bins, pallets, racks)

UTILITIES & INFRASTRUCTURE:
14. Visible electrical panels or power sources?
15. Compressed air lines visible?
16. Network/communication infrastructure visible?

SAFETY:
17. Safety equipment present (barriers, e-stops, PPE)
18. Potential safety concerns

Format as JSON.
```

### What AI CANNOT Extract (Must Ask User)

**Critical Business Information:**
- ❌ Budget range (confidential)
- ❌ Budget status (approved, in process, researching)
- ❌ Project timeline (when needed operational)
- ❌ Timeline urgency (fixed deadline vs. flexible)
- ❌ Decision-making authority (who approves this)
- ❌ Number of approvers needed

**Strategic Goals:**
- ❌ Primary business goal (unless explicitly stated on website)
- ❌ Target KPIs (specific throughput increase, defect reduction, ROI targets)
- ❌ "Why now?" - catalyst for project

**Specific Requirements:**
- ❌ Integration requirements (must work with specific MES, ERP, etc.)
- ❌ Compliance standards required (ISO, ANSI, CE, FDA, etc.)
- ❌ Preferred robot brands or technology
- ❌ Single shift vs. multi-shift operation

---

## New User Flow: AI-Powered Lead Capture

### **Step 1: "Tell Us About Your Company"** (10 seconds)

**UI:**
```
╔══════════════════════════════════════════════════════════╗
║  🏢 Let's start with your company                        ║
║                                                          ║
║  Option 1: Enter your company website                   ║
║  ┌────────────────────────────────────────────┐        ║
║  │ https://www.your-company.com               │ [→]    ║
║  └────────────────────────────────────────────┘        ║
║                                                          ║
║  OR                                                      ║
║                                                          ║
║  Option 2: Upload company presentation/PDF              ║
║  [📎 Drop files here or click to upload]                ║
║                                                          ║
║  OR                                                      ║
║                                                          ║
║  Option 3: Just tell us your company name                ║
║  ┌────────────────────────────────────────────┐        ║
║  │ Company name                               │ [→]    ║
║  └────────────────────────────────────────────┘        ║
║                                                          ║
║  💡 We'll automatically gather public information       ║
╚══════════════════════════════════════════════════════════╝
```

**What Happens:**
1. User enters website URL or company name
2. AI scrapes website (Claude + web scraping)
3. AI extracts: company name, industry, location, size, contacts
4. Progress indicator: "🔍 Analyzing your website..." (15-30 seconds)
5. **Show confirmation:** "✓ Found: [Company Name] - [Industry] - [Location]. Is this correct?"

**Fallback:** If website not accessible or user doesn't have one, show basic form fields.

---

### **Step 2: "Show Us Your Current Process"** (Optional, 1 minute)

**UI:**
```
╔══════════════════════════════════════════════════════════╗
║  🎥 Help us understand your current process              ║
║                                                          ║
║  This step is optional but helps us match you better!    ║
║                                                          ║
║  Option 1: Upload a short video (recommended)            ║
║  [🎬 Record or upload video]                             ║
║                                                          ║
║  💡 A 30-second phone video of your production line      ║
║     helps us understand your needs better than any form  ║
║                                                          ║
║  Option 2: Upload photos of your workspace               ║
║  [📷 Upload 2-5 photos]                                  ║
║                                                          ║
║  💡 Include: overall workspace, close-up of process,     ║
║     any existing equipment                               ║
║                                                          ║
║  [Skip this step] ────────────────────────────── [Next]  ║
╚══════════════════════════════════════════════════════════╝
```

**What Happens:**
1. User uploads video (max 2 minutes) and/or photos (max 10 photos)
2. AI analyzes media (Claude multimodal analysis)
3. Progress indicator: "🤖 Analyzing your process..." (30-60 seconds)
4. AI extracts: process type, cycle time, workspace, products, constraints
5. **Show summary:**
   ```
   ✓ Detected: Pick & place operation
   ✓ Current cycle time: ~15 seconds/part
   ✓ Workspace: ~4m x 3m, standard factory floor
   ✓ Products: Small metal parts, <1kg
   ```

---

### **Step 3: "Smart Questions"** (Only What AI Couldn't Extract) (2 minutes)

**UI:** Dynamic form - only shows questions for missing data

**Example A: AI Found Most Info from Website + Video**
```
╔══════════════════════════════════════════════════════════╗
║  ✨ Great! We've gathered most of your information.      ║
║  Just a few quick questions:                             ║
║                                                          ║
║  1. What's your project timeline?                        ║
║     ○ Within 3 months     ○ 3-6 months                   ║
║     ○ 6-12 months         ○ 12+ months                   ║
║                                                          ║
║  2. Estimated budget range?                              ║
║     [ Dropdown: €50K-€100K, €100K-€250K, etc. ]         ║
║                                                          ║
║  3. Are you the decision maker?                          ║
║     ○ Yes, I decide       ○ Need 1 approval              ║
║     ○ Need 2+ approvals   ○ Committee decision           ║
║                                                          ║
║  4. What's your primary goal with this project?          ║
║     [ Dropdown: Increase throughput, Reduce defects,    ║
║       Reduce labor costs, Improve safety, Other ]        ║
║                                                          ║
║  5. Your email & phone for integrator contact:           ║
║     Email: [_______________________]                     ║
║     Phone: [_______________________]                     ║
║                                                          ║
║                                    [Get My Matches →]    ║
╚══════════════════════════════════════════════════════════╝
```

**Example B: AI Found Limited Info (No Video/Photos)**
```
╔══════════════════════════════════════════════════════════╗
║  ✨ Thanks! Since we don't have visual information,      ║
║  we'll need a bit more detail:                           ║
║                                                          ║
║  1. What type of automation are you looking for?         ║
║     [ Dropdown: Pick & place, Palletizing, Welding,     ║
║       Assembly, Inspection, Material handling, Other ]   ║
║                                                          ║
║  2. Briefly describe your current process: (2-3 sent.)   ║
║     [_______________________________________________]    ║
║                                                          ║
║  3. Current production volume?                           ║
║     [ Dropdown: <100 parts/hr, 100-500, 500-1000, etc.]  ║
║                                                          ║
║  4. What's your project timeline?                        ║
║     [ Same as Example A ]                                ║
║                                                          ║
║  ... (continues with budget, authority, goal, contact)    ║
╚══════════════════════════════════════════════════════════╝
```

**Smart Logic:**
- If AI extracted application type from video → skip question 1
- If AI measured cycle time from video → skip volume question
- If AI found workspace dimensions → skip constraints question
- **Always ask:** Budget, timeline, authority, contact info (sensitive/personal)

---

### **Step 4: "Review & Submit"** (30 seconds)

**UI:**
```
╔══════════════════════════════════════════════════════════╗
║  📋 Review Your Project Profile                          ║
║                                                          ║
║  [Edit] COMPANY                                          ║
║  ✓ Müller Maschinenbau GmbH                              ║
║  ✓ Automotive Parts Manufacturing                        ║
║  ✓ Munich, Bavaria, Germany                              ║
║  ✓ ~€50M revenue, 150 employees                          ║
║                                                          ║
║  [Edit] PROJECT                                          ║
║  ✓ Application: Pick & place + quality inspection        ║
║  ✓ Current: Manual loading, 200 parts/hr                 ║
║  ✓ Goal: Increase throughput 30%, reduce defects         ║
║  ✓ Workspace: 4m x 3m, standard factory floor            ║
║                                                          ║
║  [Edit] TIMELINE & BUDGET                                ║
║  ✓ Timeline: Q2 2026 (3-6 months)                        ║
║  ✓ Budget: €150K - €250K (approved)                      ║
║  ✓ Decision maker: You + CFO approval                    ║
║                                                          ║
║  [Edit] CONTACT                                          ║
║  ✓ Thomas Müller, Head of Production                     ║
║  ✓ t.mueller@muller-mb.de                                ║
║  ✓ +49 89 1234 5678                                      ║
║                                                          ║
║  [← Back]                    [Get My Matches →]          ║
║                                                          ║
║  🤖 We'll match you with 2-3 specialized integrators     ║
║     who will contact you within 48 hours.                ║
╚══════════════════════════════════════════════════════════╝
```

**User can click [Edit] on any section to correct AI-extracted data**

---

## Technical Architecture

### Option 1: Claude-Powered (Recommended for MVP)

**Stack:**
- Frontend: Static HTML/JS
- AI: Claude API (multimodal for images/video)
- Scraping: Jina AI Reader or Firecrawl for websites
- Storage: Google Sheets + Google Drive
- PDF Generation: Python (reportlab) or Google Apps Script

**Data Flow:**
```
1. User submits website URL
   ↓
2. Firecrawl/Jina converts website to markdown
   ↓
3. Claude API analyzes markdown → extracts company data (JSON)
   ↓
4. User uploads video/photos
   ↓
5. Claude API (vision) analyzes media → extracts process data (JSON)
   ↓
6. Frontend displays smart questionnaire (only missing fields)
   ↓
7. User fills in remaining fields
   ↓
8. Combined data (AI + user) → Google Sheets
   ↓
9. Trigger: Python script generates lead deck PDF
   ↓
10. Email PDF to matched integrators + confirmation to lead
```

**Cost Estimate:**
- Claude API: ~$0.50-$2.00 per lead (depends on media size)
- Firecrawl: $0.01-0.05 per website scrape
- **Total: ~$0.50-$2.00 per qualified lead** (very affordable!)

### Option 2: Open Source (Lower cost, more complex)

**Stack:**
- AI: Llama 3.2 Vision (local) or OpenAI GPT-4V
- Scraping: BeautifulSoup + Playwright
- Video analysis: OpenCV + Llama 3.2
- Hosting: VPS or Cloudflare Workers

**Cost:** ~$0.10-0.50 per lead (mostly compute)

---

## Implementation Phases

### Phase 1: MVP with Website Scraping Only (Week 1)
- ✅ User enters website URL
- ✅ AI extracts company info
- ✅ User fills smart questionnaire (reduced fields)
- ✅ Generate lead deck
- ⏱️ Time saved: 5 minutes → 3 minutes

### Phase 2: Add Photo Upload (Week 2)
- ✅ User uploads 2-5 photos
- ✅ AI extracts workspace dimensions, equipment, environment
- ✅ Further reduce questionnaire
- ⏱️ Time saved: 5 minutes → 2.5 minutes

### Phase 3: Add Video Analysis (Week 3)
- ✅ User uploads video (up to 2 minutes)
- ✅ AI extracts process type, cycle time, throughput
- ✅ Minimal questionnaire (budget, timeline, contact only)
- ⏱️ Time saved: 5 minutes → 2 minutes

### Phase 4: Polish & Optimize (Week 4)
- ✅ Add video recording directly in browser
- ✅ Improve AI prompts based on real data
- ✅ Add AI confidence scores (show fields AI is uncertain about)
- ✅ A/B test different flows

---

## Competitive Advantage

### What Makes This Unique?

1. **No other robotics marketplace does this**
   - HowToRobot: Long forms
   - Clutch: Text-only profiles
   - wlw.de: Basic directory

2. **Feels like magic**
   - "I just dropped in my website and uploaded a video, and they understood everything!"
   - Viral potential: "Check out how easy this was"

3. **Better data quality**
   - Video/photos show what words can't describe
   - AI catches details humans forget to mention
   - More accurate integrator matching

4. **Faster time-to-match**
   - 2 minutes vs. 10-15 minutes traditional form
   - Higher completion rate (50-60% vs. 15-20%)
   - Integrators get richer information immediately

5. **Scalable to non-technical users**
   - "Just show us your factory" is universal
   - No need to understand technical jargon
   - Works across languages (video is visual!)

---

## UI/UX Mockup: Landing Page Hero Section

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║              🤖 ROBOFOLIO                                     ║
║                                                               ║
║     Find Your Perfect Robotics Partner in 2 Minutes          ║
║                                                               ║
║     Just show us your factory — our AI handles the rest      ║
║                                                               ║
║  ┌─────────────────────────────────────────────────────┐    ║
║  │                                                       │    ║
║  │   [🎥 Video]  →  [🤖 AI Magic]  →  [📄 Lead Deck]   │    ║
║  │                                                       │    ║
║  │   30 sec upload     Auto-extract      Perfect match  │    ║
║  │                                                       │    ║
║  └─────────────────────────────────────────────────────┘    ║
║                                                               ║
║            [Get Started — It's Free & Takes 2 Minutes]       ║
║                                                               ║
║  ✓ No forms to fill out    ✓ AI-powered    ✓ 48hr response  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Next Steps

1. **Validate concept** - Do you love this approach?
2. **Choose implementation path** - Claude API (fast) or open source (cheap)?
3. **Build Phase 1 MVP** - Website scraping + smart questionnaire
4. **Test with 5-10 beta users**
5. **Add video/photo if Phase 1 works well**

**This could be THE feature that makes Robofolio the default choice in Europe.** 🚀

---

**What do you think? Should we build this?**
