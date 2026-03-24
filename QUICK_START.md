# Robofolio AI System - Quick Start Guide

Get your AI-powered lead capture system running in **under 1 hour**.

---

## 🎯 What You're Building

A landing page where users:
1. Drop their website URL → AI extracts company info
2. Upload photos → AI analyzes workspace
3. Answer 5 questions → Submit
4. Get matched with integrators in 48 hours

**Total user time: 2 minutes**

---

## ⚡ Quick Start (Local Testing)

### 1. Get Anthropic API Key (5 min)

```
1. Go to: https://console.anthropic.com/
2. Sign up + add $5 credit
3. Create API key
4. Copy it (sk-ant-api03-xxx...)
```

### 2. Install & Run Backend (10 min)

```bash
cd /path/to/Claude-Robofolio

# Install dependencies
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY='sk-ant-api03-your-key-here'

# Run backend
python backend_api.py
```

Should see: `Running on http://0.0.0.0:5000`

### 3. Connect Frontend to Backend (15 min)

Follow: **[CONNECT_FRONTEND_TO_BACKEND.md](./CONNECT_FRONTEND_TO_BACKEND.md)**

Make 3 simple changes to `index-ai.html`:
- Change #1: Website analysis (real API call)
- Change #2: Photo analysis (real API call)
- Change #3: Form submission (real API call)

### 4. Test It! (5 min)

```bash
# Open in browser
open index-ai.html  # macOS
# or just double-click the file

# Test:
1. Enter website: https://www.bmw.com
2. Click "Analyze" → wait 30 sec
3. See extracted company info!
```

✅ **Done! Your AI system is working!**

---

## 🚀 Deploy to Production (30 min)

### Option 1: Heroku + Netlify (Free)

**Backend to Heroku:**
```bash
# Install Heroku CLI
brew install heroku  # macOS
# or download from: https://devcenter.heroku.com/

# Deploy
heroku login
heroku create robofolio-api
heroku config:set ANTHROPIC_API_KEY='your-key'
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

Your API: `https://robofolio-api.herokuapp.com`

**Frontend to Netlify:**
```
1. Go to: https://netlify.com
2. Drag & drop index-ai.html (rename to index.html)
3. Update API URL in code to Heroku URL
4. Deploy!
```

Your site: `https://robofolio.netlify.app`

### Option 2: Railway (Easiest - $5/mo)

```
1. Go to: https://railway.app
2. Connect GitHub
3. Push code to GitHub
4. Deploy from Railway
5. Set ANTHROPIC_API_KEY in Railway dashboard
```

Done in 5 clicks!

---

## 💰 Costs

**Development/Testing:**
- Anthropic API: $5 (lasts for 500+ test leads)
- Hosting: Free (Heroku/Netlify free tier)

**Production (100 leads/month):**
- AI: ~$10/month
- Hosting: $7/month (Heroku) or free (Railway free tier)
- **Total: ~$17/month**

**Revenue (100 leads @ €12 each):**
- €1,200/month
- **Profit: €1,180/month** 🤑

---

## 📊 Test Checklist

Before going live, test these:

✅ Website analysis works (try 3 different websites)
✅ Photo upload works (try 2-3 photos)
✅ Photo analysis returns data
✅ Form submission succeeds
✅ Backend logs show no errors
✅ API key is working (check Anthropic dashboard for usage)

---

## 🐛 Common Issues

**"Failed to fetch"**
→ Backend not running or wrong URL

**"API request failed"**
→ Check ANTHROPIC_API_KEY is set

**Photos not uploading**
→ Files too large (max 10MB) or wrong format

**Website analysis returns empty**
→ Some sites block scraping (this is normal)

---

## 🎯 Next Steps

Once working locally:

**Week 1:**
- [ ] Deploy to production
- [ ] Test with 5 real companies
- [ ] Get feedback

**Week 2:**
- [ ] Recruit 10 integrators
- [ ] Refine AI prompts based on real data
- [ ] Add Google Analytics

**Week 3:**
- [ ] Public launch
- [ ] Start marketing
- [ ] Scale!

---

## 📚 Full Documentation

- [IMPLEMENTATION_CHECKLIST.md](./IMPLEMENTATION_CHECKLIST.md) - Detailed steps
- [CONNECT_FRONTEND_TO_BACKEND.md](./CONNECT_FRONTEND_TO_BACKEND.md) - Code changes needed
- [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Complete deployment guide
- [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) - Full system overview

---

## 💪 You've Got This!

The hardest part (building the system) is done. Now just:
1. Get API key
2. Run backend
3. Test it
4. Deploy

**Let's make Robofolio the #1 robotics marketplace in Europe!** 🚀

---

**Questions? Stuck? Let me know!**
