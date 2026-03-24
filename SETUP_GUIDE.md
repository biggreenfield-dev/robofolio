# Robofolio AI-Powered System - Complete Setup Guide

## 🎯 What You've Built

You now have a complete AI-powered lead capture system that:
- Analyzes company websites automatically with AI
- Extracts data from workspace photos
- Generates smart questionnaires based on extracted data
- Creates professional one-page PDF lead decks for integrators
- Scores leads automatically (0-100)

## 📦 System Components

```
Robofolio/
├── index-ai.html           # AI-powered landing page (frontend)
├── backend_api.py          # Flask API with Claude AI integration
├── lead_deck_generator.py  # PDF generation script
├── requirements.txt        # Python dependencies
└── SETUP_GUIDE.md         # This file
```

## 🚀 Quick Start (Local Testing)

### Step 1: Install Dependencies

```bash
cd /path/to/Robofolio
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Get API Keys

#### Anthropic API Key (Required)
1. Go to https://console.anthropic.com/
2. Create an account or sign in
3. Navigate to "API Keys"
4. Create a new API key
5. Copy the key

#### Jina AI Key (Optional - for better website scraping)
1. Go to https://jina.ai/
2. Sign up for free tier
3. Get your API key

### Step 3: Configure Environment Variables

Create a `.env` file:

```bash
# .env file
ANTHROPIC_API_KEY=your-anthropic-api-key-here
JINA_API_KEY=your-jina-api-key-here  # Optional
```

Or export them:

```bash
export ANTHROPIC_API_KEY='your-anthropic-api-key-here'
export JINA_API_KEY='your-jina-api-key-here'  # Optional
```

### Step 4: Start the Backend API

```bash
python backend_api.py
```

The API will start on `http://localhost:5000`

### Step 5: Update Frontend API Endpoint

Open `index-ai.html` and update the API endpoint (search for "TODO"):

```javascript
// Around line 1200-1300 in the JavaScript section
const API_BASE_URL = 'http://localhost:5000/api';  // For local testing
// const API_BASE_URL = 'https://your-api.herokuapp.com/api';  // For production
```

### Step 6: Open the Landing Page

1. Open `index-ai.html` in your browser
2. Test the form:
   - Enter a website URL (try: https://www.bmw.com)
   - Upload some photos
   - Fill in the questions
   - Submit

## 🌐 Production Deployment

### Option A: Deploy to Heroku (Recommended for MVP)

#### 1. Install Heroku CLI

```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. Prepare for Deployment

Create `Procfile`:

```
web: gunicorn backend_api:app
```

Add `gunicorn` to `requirements.txt`:

```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

#### 3. Deploy Backend

```bash
# Login to Heroku
heroku login

# Create app
heroku create robofolio-api

# Set environment variables
heroku config:set ANTHROPIC_API_KEY='your-key-here'
heroku config:set JINA_API_KEY='your-key-here'

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Check logs
heroku logs --tail
```

Your API will be at: `https://robofolio-api.herokuapp.com`

#### 4. Deploy Frontend to Netlify

1. Go to [netlify.com](https://netlify.com)
2. Sign up/login
3. Drag and drop `index-ai.html` (rename to `index.html`)
4. Update API_BASE_URL in the file to your Heroku URL
5. Deploy!

Your site will be at: `https://robofolio.netlify.app`

**Cost: FREE** (Heroku free tier + Netlify free tier)

---

### Option B: Deploy to Vercel (Serverless)

Vercel is great for serverless APIs.

#### 1. Install Vercel CLI

```bash
npm install -g vercel
```

#### 2. Create `vercel.json`

```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend_api.py",
      "use": "@vercel/python"
    },
    {
      "src": "index-ai.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend_api.py"
    },
    {
      "src": "/(.*)",
      "dest": "index-ai.html"
    }
  ],
  "env": {
    "ANTHROPIC_API_KEY": "@anthropic-api-key",
    "JINA_API_KEY": "@jina-api-key"
  }
}
```

#### 3. Deploy

```bash
vercel login
vercel

# Set environment variables
vercel env add ANTHROPIC_API_KEY
vercel env add JINA_API_KEY

# Deploy to production
vercel --prod
```

**Cost: FREE** (Vercel free tier includes serverless functions)

---

### Option C: Deploy to Railway (Easiest)

Railway is the easiest deployment platform.

#### 1. Go to [railway.app](https://railway.app)

#### 2. Connect GitHub

1. Push your code to GitHub
2. Click "New Project" on Railway
3. Select "Deploy from GitHub repo"
4. Select your Robofolio repo

#### 3. Set Environment Variables

In Railway dashboard:
- Go to your project
- Click "Variables"
- Add `ANTHROPIC_API_KEY` and `JINA_API_KEY`

#### 4. Deploy Frontend

1. Create new project for frontend (static site)
2. Upload `index-ai.html`
3. Update API_BASE_URL to your Railway backend URL

**Cost: $5/month** (after free tier)

---

## 🔧 Advanced Configuration

### Connect to Google Sheets

To save leads to Google Sheets:

1. **Enable Google Sheets API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project
   - Enable "Google Sheets API"
   - Create credentials (Service Account)
   - Download JSON key file

2. **Update backend_api.py**

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)

def save_to_google_sheets(lead_data):
    SPREADSHEET_ID = 'your-spreadsheet-id'
    RANGE_NAME = 'Leads!A:Z'

    values = [[
        lead_data.get('timestamp'),
        lead_data.get('company_name'),
        lead_data.get('contact_email'),
        # ... add all fields
    ]]

    body = {'values': values}

    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()

    return result
```

### Send Email Notifications

Use SendGrid for emails:

```bash
pip install sendgrid
```

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_lead_confirmation(lead_data):
    message = Mail(
        from_email='noreply@robofolio.com',
        to_emails=lead_data['contact_email'],
        subject='Your Robofolio Lead Submission',
        html_content=f'<strong>Thank you {lead_data["contact_name"]}!</strong>'
    )

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    return response
```

### Generate PDF Lead Decks

The `lead_deck_generator.py` script is ready to use:

```python
from lead_deck_generator import create_lead_deck

# In backend_api.py, after lead submission:
pdf_path = create_lead_deck(lead_data, f"/tmp/{lead_id}.pdf")

# Upload to cloud storage or attach to email
```

---

## 📊 Monitoring & Analytics

### Track API Usage

Add analytics to `backend_api.py`:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/analyze-website', methods=['POST'])
def analyze_website():
    logger.info(f"Website analysis requested: {request.json.get('url')}")
    # ... rest of code
```

### Add Google Analytics

In `index-ai.html`, add before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Monitor Costs

Claude API pricing (as of 2026):
- Input: $3 / million tokens
- Output: $15 / million tokens

Estimated cost per lead:
- Website analysis: ~5K tokens input, 1K output = ~$0.03
- Photo analysis (3 photos): ~10K tokens input, 2K output = ~$0.06
- **Total: ~$0.10 per lead**

With 100 leads/month = $10/month for AI
With 1000 leads/month = $100/month for AI

---

## 🧪 Testing

### Test Website Analysis

```bash
curl -X POST http://localhost:5000/api/analyze-website \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bmw.com"}'
```

### Test Photo Analysis

```bash
curl -X POST http://localhost:5000/api/analyze-photos \
  -F "photos=@workspace1.jpg" \
  -F "photos=@workspace2.jpg"
```

### Test Lead Submission

```bash
curl -X POST http://localhost:5000/api/submit-lead \
  -H "Content-Type: application/json" \
  -d @test_lead.json
```

---

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not set"
- Make sure you set the environment variable
- Check: `echo $ANTHROPIC_API_KEY`
- Restart your terminal after setting

### "Could not fetch website content"
- Website may block bots - try with Jina AI key
- Check if URL is accessible in browser
- Some sites require JavaScript - Jina handles this

### "CORS error" in browser
- Make sure Flask-CORS is installed
- Check API_BASE_URL in frontend matches backend
- For production, add specific origins to CORS config

### "Rate limit exceeded"
- You hit Anthropic's rate limit
- Upgrade to paid tier for higher limits
- Add rate limiting to your API

---

## 📈 Next Steps

Once your MVP is live:

1. **Week 1-2: Beta Testing**
   - Send to 10 friendly companies
   - Collect feedback on AI accuracy
   - Refine extraction prompts

2. **Week 3-4: Add Video Analysis**
   - Extend photo analysis to handle videos
   - Use Claude's vision for video frames
   - Extract cycle times from video

3. **Month 2: Integrator Matching**
   - Build integrator database
   - Create matching algorithm
   - Automate email sending

4. **Month 3: Scale**
   - Optimize AI prompts for cost
   - Add caching to reduce API calls
   - Implement queue system for high volume

---

## 💰 Cost Breakdown (Monthly)

### At 100 Leads/Month

| Item | Cost |
|------|------|
| Claude API | $10 |
| Heroku Hobby | $7 |
| Netlify | Free |
| SendGrid (email) | Free |
| Google Sheets | Free |
| **Total** | **~$17/month** |

### At 1000 Leads/Month

| Item | Cost |
|------|------|
| Claude API | $100 |
| Heroku Standard | $25 |
| Netlify Pro | $19 |
| SendGrid | $20 |
| **Total** | **~$164/month** |

**Revenue at 1000 leads/month:** If integrators pay €10-15 per lead, that's €10,000-15,000/month revenue for ~$164 costs = incredible margins!

---

## 🎓 Learning Resources

- [Anthropic API Docs](https://docs.anthropic.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Heroku Deployment Guide](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Jina AI Reader](https://jina.ai/reader/)

---

## 🆘 Support

Need help? Contact:
- Email: knopp.max@googlemail.com
- Review: AI_POWERED_LEAD_CAPTURE.md for strategy
- Review: LEAD_CAPTURE_STRATEGY.md for details

---

**You're ready to launch! Start with local testing, then deploy to Heroku + Netlify. Good luck! 🚀**
