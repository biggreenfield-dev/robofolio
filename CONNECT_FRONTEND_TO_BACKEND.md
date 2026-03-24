# Connect Frontend to Real Backend API

This guide shows you exactly what to change in `index-ai.html` to make it call your real backend instead of simulating responses.

---

## 🔧 Changes Needed

You need to update 3 functions in the JavaScript section of `index-ai.html`:

1. **Website analysis** - Make real API call to analyze website
2. **Photo analysis** - Make real API call to analyze photos
3. **Form submission** - Make real API call to submit lead

---

## Change #1: Website Analysis (Real API Call)

### Find this code (around line 1100-1150):

```javascript
// Website analysis
document.getElementById('analyzeWebsiteBtn').addEventListener('click', async function() {
    const url = document.getElementById('websiteUrl').value;

    if (!url) {
        alert(document.documentElement.lang === 'de' ?
            'Bitte geben Sie eine Website-URL ein' :
            'Please enter a website URL');
        return;
    }

    // Show loading
    document.getElementById('websiteLoading').classList.add('active');
    this.disabled = true;

    try {
        // TODO: Call AI API to analyze website
        // For now, simulate with timeout
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Simulated extracted data
        const extracted = {
            companyName: 'Müller Maschinenbau GmbH',
            industry: 'Automotive Parts Manufacturing',
            location: 'Munich, Bavaria, Germany',
            size: '€50M-€100M revenue'
        };
```

### Replace with:

```javascript
// Website analysis
document.getElementById('analyzeWebsiteBtn').addEventListener('click', async function() {
    const url = document.getElementById('websiteUrl').value;

    if (!url) {
        alert(document.documentElement.lang === 'de' ?
            'Bitte geben Sie eine Website-URL ein' :
            'Please enter a website URL');
        return;
    }

    // Show loading
    document.getElementById('websiteLoading').classList.add('active');
    this.disabled = true;

    try {
        // REAL API CALL
        const response = await fetch('http://localhost:5000/api/analyze-website', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        const result = await response.json();

        if (!result.success) {
            throw new Error(result.error || 'Analysis failed');
        }

        // Use real extracted data from API
        const extracted = {
            companyName: result.data.company_name || 'Unknown',
            industry: result.data.industry || 'Unknown',
            location: result.data.location || 'Unknown',
            size: result.data.company_size || 'Unknown'
        };
```

---

## Change #2: Photo Analysis (Real API Call)

### Find this code (around line 1230-1280):

```javascript
async function analyzePhotos() {
    document.getElementById('photoLoading').classList.add('active');

    try {
        // TODO: Call AI API to analyze photos
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Simulated extracted data
        const extracted = {
            processType: 'Manual pick & place operation',
            workspace: '~4m x 3m, standard factory floor',
            environment: 'Indoor, standard temperature, good lighting'
        };
```

### Replace with:

```javascript
async function analyzePhotos() {
    document.getElementById('photoLoading').classList.add('active');

    try {
        // REAL API CALL
        const formData = new FormData();

        // Add all uploaded photos to FormData
        uploadedPhotos.forEach((file, index) => {
            formData.append('photos', file);
        });

        const response = await fetch('http://localhost:5000/api/analyze-photos', {
            method: 'POST',
            body: formData  // Don't set Content-Type, browser will set it with boundary
        });

        if (!response.ok) {
            throw new Error('Photo analysis failed');
        }

        const result = await response.json();

        if (!result.success) {
            throw new Error(result.error || 'Analysis failed');
        }

        // Use real extracted data from API
        const extracted = {
            processType: result.data.process_type || 'Unknown',
            workspace: result.data.workspace_dimensions || 'Unknown',
            environment: result.data.environment_type || 'Unknown'
        };
```

---

## Change #3: Form Submission (Real API Call)

### Find this code (around line 1390-1420):

```javascript
// Form submission
document.getElementById('leadForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = document.documentElement.lang === 'de' ? 'Wird gesendet...' : 'Submitting...';

    try {
        // TODO: Submit to backend
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Show success message
        document.getElementById('leadForm').style.display = 'none';
        document.querySelector('.progress-container').style.display = 'none';
        document.getElementById('successContainer').classList.add('active');

    } catch (error) {
```

### Replace with:

```javascript
// Form submission
document.getElementById('leadForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = document.documentElement.lang === 'de' ? 'Wird gesendet...' : 'Submitting...';

    try {
        // Collect all form data
        const leadData = {
            // Extracted data from AI
            ...formData.extractedData,

            // User inputs
            primary_goal: document.getElementById('primary-goal').value,
            timeline: document.querySelector('input[name="timeline"]:checked')?.value,
            budget_range: document.getElementById('budget-range').value,
            budget_status: document.querySelector('input[name="budget-status"]:checked')?.value,
            authority: document.querySelector('input[name="authority"]:checked')?.value,
            contact_name: document.getElementById('contact-name').value,
            contact_title: document.getElementById('contact-title').value,
            contact_email: document.getElementById('contact-email').value,
            contact_phone: document.getElementById('contact-phone').value,

            // Language
            language: document.documentElement.lang
        };

        // REAL API CALL
        const response = await fetch('http://localhost:5000/api/submit-lead', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(leadData)
        });

        if (!response.ok) {
            throw new Error('Submission failed');
        }

        const result = await response.json();

        if (!result.success) {
            throw new Error(result.error || 'Submission failed');
        }

        // Show success message
        document.getElementById('leadForm').style.display = 'none';
        document.querySelector('.progress-container').style.display = 'none';
        document.getElementById('successContainer').classList.add('active');

    } catch (error) {
```

---

## 🚀 Quick Steps to Apply Changes

### Option A: Manual Edit (Recommended)

1. Open `index-ai.html` in your code editor (VS Code, Sublime, etc.)
2. Find each code section above (use Cmd+F / Ctrl+F to search)
3. Replace with the new code
4. Save the file
5. Test!

### Option B: Use Search & Replace

1. Open `index-ai.html`
2. Search for: `// TODO: Call AI API to analyze website`
3. Replace that entire function with Change #1
4. Repeat for Changes #2 and #3
5. Save

---

## ✅ Testing After Changes

### 1. Make sure backend is running:

```bash
python backend_api.py
```

### 2. Open updated index-ai.html in browser:

```bash
# On macOS:
open index-ai.html

# On Linux:
xdg-open index-ai.html

# On Windows:
start index-ai.html
```

### 3. Test website analysis:

- Enter a real website (try: `https://www.bmw.com`)
- Click "Analyze"
- Wait 30-60 seconds (real AI analysis!)
- Should see extracted company info

### 4. Check browser console for errors:

- Right-click page → "Inspect" → "Console" tab
- Should not see any red errors
- Should see API requests succeeding

---

## 🐛 Troubleshooting

### Error: "Failed to fetch"

**Problem:** Frontend can't connect to backend

**Fix:**
1. Make sure backend is running: `python backend_api.py`
2. Check URL is correct: `http://localhost:5000`
3. Check CORS is enabled in backend (it already is in our code)

### Error: "API request failed"

**Problem:** Backend returned an error

**Fix:**
1. Check backend terminal for error messages
2. Make sure ANTHROPIC_API_KEY is set
3. Test API key works: `curl http://localhost:5000/health`

### Website analysis returns "Unknown"

**Problem:** AI couldn't extract information

**Fix:**
1. Try a different website with clearer information
2. Check backend logs for specific errors
3. Website might be blocking scraping - this is normal for some sites

### Photos not analyzing

**Problem:** Photo upload/analysis failing

**Fix:**
1. Make sure photos are < 10MB each
2. Use JPG or PNG format
3. Check browser console for specific errors
4. Make sure FormData is being sent correctly

---

## 🎯 Next Step

After making these changes and testing locally, move to:
**IMPLEMENTATION_CHECKLIST.md → Step 4: Test End-to-End**

---

**Questions? Issues? Let me know and I'll help debug!** 🚀
