# Google Sheets Integration Setup Guide

This guide will help you connect your Robofolio landing page form to Google Sheets.

## Step 1: Create a Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it "Robofolio Leads"
4. In the first row, add these column headers:
   - A1: `Timestamp`
   - B1: `Name`
   - C1: `Email`
   - D1: `Company`
   - E1: `Industry`
   - F1: `Description`
   - G1: `Language`

## Step 2: Create Google Apps Script

1. In your Google Sheet, click **Extensions** → **Apps Script**
2. Delete any code in the editor
3. Copy and paste the following code:

```javascript
function doPost(e) {
  try {
    // Parse the incoming JSON data
    const data = JSON.parse(e.postData.contents);

    // Get the active spreadsheet
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Append a new row with the form data
    sheet.appendRow([
      data.timestamp || new Date(),
      data.name || '',
      data.email || '',
      data.company || '',
      data.industry || '',
      data.description || '',
      data.language || 'de'
    ]);

    // Send email notification (optional - update with your email)
    const emailAddress = 'knopp.max@googlemail.com'; // UPDATE THIS
    const subject = 'New Robofolio Lead: ' + (data.company || 'Unknown Company');
    const message = `
New lead submission:

Name: ${data.name}
Email: ${data.email}
Company: ${data.company}
Industry: ${data.industry}
Description: ${data.description}
Language: ${data.language}
Timestamp: ${data.timestamp}

---
View all leads: ${SpreadsheetApp.getActiveSpreadsheet().getUrl()}
    `;

    MailApp.sendEmail(emailAddress, subject, message);

    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({ result: 'success' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    // Return error response
    return ContentService
      .createTextOutput(JSON.stringify({ result: 'error', error: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
```

4. **Important**: Update the `emailAddress` variable in the code with your actual email address
5. Click the **Save** icon (💾) and give your project a name like "Robofolio Form Handler"

## Step 3: Deploy the Script

1. Click **Deploy** → **New deployment**
2. Click the gear icon (⚙️) next to "Select type"
3. Choose **Web app**
4. Configure the deployment:
   - **Description**: "Robofolio Lead Capture v1"
   - **Execute as**: Me (your email)
   - **Who has access**: Anyone
5. Click **Deploy**
6. You may need to authorize the script:
   - Click **Authorize access**
   - Choose your Google account
   - Click **Advanced** → **Go to [Project Name] (unsafe)**
   - Click **Allow**
7. **Copy the Web App URL** - it will look like:
   ```
   https://script.google.com/macros/s/AKfycby.../exec
   ```

## Step 4: Update Your Landing Page

1. Open `index.html` in a text editor
2. Find this line (around line 789):
   ```javascript
   const scriptURL = 'YOUR_GOOGLE_APPS_SCRIPT_URL_HERE';
   ```
3. Replace `YOUR_GOOGLE_APPS_SCRIPT_URL_HERE` with your actual Web App URL from Step 3
4. Save the file

## Step 5: Test the Form

1. Open `index.html` in your web browser
2. Fill out the form with test data
3. Click submit
4. Check your Google Sheet - you should see a new row with the test data
5. Check your email - you should receive a notification

## Troubleshooting

### Form submission fails
- Make sure you copied the complete Web App URL including `/exec` at the end
- Check that the deployment is set to "Anyone" can access
- Try redeploying the script (Deploy → Manage deployments → Edit → New version)

### No email notifications
- Verify your email address is correct in the Apps Script code
- Check your spam folder
- Ensure the script has permission to send emails (should be granted during authorization)

### Data not appearing in sheet
- Check that column headers in A1-G1 match exactly as shown in Step 1
- Make sure the sheet is the active sheet (first tab)
- Check the Apps Script execution log (View → Executions) for errors

## Optional Enhancements

### Add more form fields
1. Add the field to your HTML form
2. Add a column header in your Google Sheet
3. Update the `sheet.appendRow([...])` line in the script to include the new field

### Customize email notifications
- Edit the `subject` and `message` variables in the Apps Script
- Add HTML formatting using `MailApp.sendEmail()` with HTML body option

### Add auto-responder
Add this code after the `MailApp.sendEmail()` line to send a confirmation email to the lead:

```javascript
// Send auto-responder to lead
const autoResponseSubject = data.language === 'de'
  ? 'Vielen Dank für Ihre Anfrage bei Robofolio'
  : 'Thank you for your inquiry at Robofolio';

const autoResponseMessage = data.language === 'de'
  ? `Hallo ${data.name},\n\nvielen Dank für Ihre Anfrage! Wir werden uns innerhalb von 48 Stunden bei Ihnen melden.\n\nBeste Grüße,\nDas Robofolio Team`
  : `Hello ${data.name},\n\nThank you for your inquiry! We'll get back to you within 48 hours.\n\nBest regards,\nThe Robofolio Team`;

MailApp.sendEmail(data.email, autoResponseSubject, autoResponseMessage);
```

## Next Steps

Once your form is working:
1. **Host your landing page** on Netlify, Vercel, or GitHub Pages
2. **Connect a custom domain** (e.g., robofolio.com)
3. **Add Google Analytics** to track visitors
4. **Set up form validation** to prevent spam submissions
5. **Create a CRM workflow** in Airtable or Notion to manage leads

## Security Note

The Google Apps Script is set to "Anyone" access because it needs to receive form submissions from your public website. This is safe because:
- The script only accepts POST requests with specific data fields
- It only writes to your designated Google Sheet
- No sensitive data from your Google account is exposed

However, you should:
- Never include API keys or passwords in the script
- Monitor your sheet for spam submissions
- Consider adding reCAPTCHA if you get bot submissions

---

**Need help?** Contact Max at knopp.max@googlemail.com
