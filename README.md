# Robofolio - German-Language Landing Page

Welcome to your Robofolio landing page! This is a professional, bilingual (German/English) landing page designed to capture leads from German Mittelstand manufacturers looking for robotics integrators.

## 📁 Files in This Folder

- **index.html** - Your main landing page (bilingual: DE/EN)
- **GOOGLE_SHEETS_SETUP.md** - Step-by-step guide to connect form submissions to Google Sheets
- **Robofolio_Strategic_Plan.docx** - Your strategic plan document
- **Robofolio_Competitive_Analysis.xlsx** - Market analysis and competitor research
- **Robofolio_MVP_Landing_Page.html** - Original English wireframe (for reference)

## 🚀 Quick Start

### 1. Test the Landing Page Locally

Simply open `index.html` in your web browser to see the page. You can:
- Toggle between German (DE) and English (EN) using the language switcher
- Browse the entire page to see all sections
- Try the form (it won't submit yet - see step 2)

### 2. Connect Google Sheets

Follow the detailed instructions in `GOOGLE_SHEETS_SETUP.md` to:
1. Create a Google Sheet for your leads
2. Set up Google Apps Script to receive form submissions
3. Configure email notifications
4. Update the form submission URL in `index.html`

**Time required**: ~15 minutes

### 3. Deploy Your Landing Page

Once Google Sheets is connected, deploy your page to make it live:

#### Option A: Netlify (Recommended - Easiest)
1. Create free account at [netlify.com](https://netlify.com)
2. Drag and drop your `index.html` file
3. Get instant URL like `robofolio.netlify.app`
4. Later: Connect custom domain

#### Option B: Vercel
1. Create free account at [vercel.com](https://vercel.com)
2. Connect your GitHub account
3. Push files to GitHub repo
4. Deploy from Vercel dashboard

#### Option C: GitHub Pages
1. Create GitHub account
2. Create new repo named `robofolio-landing`
3. Upload `index.html`
4. Enable GitHub Pages in Settings
5. Access at `yourusername.github.io/robofolio-landing`

## ✨ Features

### Bilingual Support (DE/EN)
- Toggle between German and English with one click
- Language preference saved in browser
- All content professionally translated
- Form submissions include language preference

### Lead Capture Form
- 5 fields optimized for conversion
- Google Sheets integration
- Automatic email notifications
- Timestamp tracking
- Mobile-friendly design

### Professional Design
- Modern, clean aesthetic
- Fully responsive (mobile, tablet, desktop)
- Smooth animations and transitions
- Trust signals and social proof
- Clear call-to-action buttons

### SEO Ready
- Semantic HTML5 structure
- Meta descriptions
- Fast loading (single file, no external dependencies)
- Mobile-optimized

## 📊 What's Next?

Based on your 30-day strategic plan, here are your immediate next steps:

### Week 1: Get Live
- ✅ Landing page created (DONE!)
- 🔲 Connect Google Sheets integration
- 🔲 Deploy to Netlify/Vercel
- 🔲 Test form submissions end-to-end

### Week 2: Integrator Recruitment
- 🔲 Create integrator database (spreadsheet/Airtable)
- 🔲 Research 20 target Systemintegratoren in Bavaria & Baden-Württemberg
- 🔲 Draft outreach email templates
- 🔲 Begin contacting integrators

### Week 3: Buyer Research
- 🔲 Create buyer interview script
- 🔲 Identify 10-15 Mittelstand manufacturers to interview
- 🔲 Schedule discovery calls
- 🔲 Document insights and refine value proposition

### Week 4: Trade Fair Research
- 🔲 Research Automatica 2026 booth costs and dates
- 🔲 Research Hannover Messe 2026 options
- 🔲 Connect with VDMA (Verband Deutscher Maschinen- und Anlagenbau)
- 🔲 Plan content strategy for lead generation

## 🛠 Customization

### Update Content
All content is in `index.html`. Each section has German (`data-lang="de"`) and English (`data-lang="en"`) versions. To update:

1. Find the section you want to edit
2. Update both DE and EN versions
3. Save the file
4. Re-deploy (if already live)

### Change Colors
Colors are defined in the `<style>` section at the top:
- Primary blue: `#1a365d`
- Secondary blue: `#2d5a87`
- Green CTA: `#48bb78`

Search and replace these hex codes to rebrand.

### Add Analytics
Add this before `</head>` to track visitors:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

Replace `GA_MEASUREMENT_ID` with your actual Google Analytics ID.

## 📞 Support

Questions? Need help?
- Email: knopp.max@googlemail.com
- Review the strategic plan: `Robofolio_Strategic_Plan.docx`
- Check competitor research: `Robofolio_Competitive_Analysis.xlsx`

## 🎯 Success Metrics

Track these KPIs once live:
- **Traffic**: Unique visitors per month
- **Conversion Rate**: Form submissions / visitors (target: 3-5%)
- **Lead Quality**: Leads that result in integrator matches
- **Response Time**: How fast you respond to submissions (target: <48 hrs)

## 📈 Future Enhancements

Consider adding later:
- Blog for SEO and thought leadership
- Integrator directory/search functionality
- Live chat widget (e.g., Intercom, Drift)
- Testimonials from matched buyers
- Case studies section
- reCAPTCHA to prevent spam
- Multi-step form to increase completion rates
- Exit-intent popup for visitors leaving

---

**Ready to launch?** Start with the Google Sheets setup, then deploy to Netlify! 🚀
