# Vercel Environment Variables Setup

## 🔧 Required Environment Variables

You need to set these environment variables in your Vercel dashboard:

### **1. OPENAI_API_KEY** (REQUIRED)
- **What it is**: Your OpenAI API key for GPT-4 access
- **How to get it**: 
  1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
  2. Create a new API key
  3. Copy the key (starts with `sk-`)

**Value example:**
```
sk-1234567890abcdef1234567890abcdef1234567890abcdef
```

### **2. GOOGLE_SERVICE_ACCOUNT_JSON** (REQUIRED)
- **What it is**: Your Google Service Account credentials for Google Sheets access
- **How to get it**:
  1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. Create a new project or select existing one
  3. Enable Google Sheets API
  4. Create a Service Account
  5. Download the JSON key file
  6. Copy the ENTIRE content of the JSON file

**Value example:**
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}
```

### **3. EMAIL_USER** (OPTIONAL - for sending emails)
- **What it is**: Your Gmail address for sending emails
- **How to get it**: Your Gmail address

**Value example:**
```
yourname@gmail.com
```

### **4. EMAIL_PASSWORD** (OPTIONAL - for sending emails)
- **What it is**: Your Gmail app password (NOT your regular password)
- **How to get it**:
  1. Enable 2-factor authentication on your Google account
  2. Go to Google Account settings → Security
  3. Generate an "App Password" for "Mail"
  4. Use the generated password

**Value example:**
```
abcd efgh ijkl mnop
```

## 🚀 How to Set Environment Variables in Vercel

### **Step 1: Go to Vercel Dashboard**
1. Visit [vercel.com](https://vercel.com)
2. Sign in and select your project
3. Go to Settings → Environment Variables

### **Step 2: Add Each Variable**
For each environment variable:

1. **Name**: Enter the variable name (e.g., `OPENAI_API_KEY`)
2. **Value**: Paste the value
3. **Environment**: Select "Production" (and optionally "Preview" and "Development")
4. **Click "Add"**

### **Step 3: Deploy**
After adding all variables, redeploy your project.

## 🔍 Testing Your Setup

After deployment, you can test if everything is working:

1. **Visit your deployed URL**
2. **Check the browser console** for any error messages
3. **Use the test connection endpoint**: `https://your-app.vercel.app/api/test-connection`

## ⚠️ Important Notes

### **Security:**
- Never share your API keys
- Use app passwords for Gmail (not regular passwords)
- Keep your service account JSON secure

### **Google Sheets Setup:**
- Make sure your Google Sheet is shared with the service account email
- The spreadsheet ID is hardcoded in your app: `1dfm728PBOjBzr2c1OVdPG-9xau6kIoMabeXjM7I8Wes`
- If you want to use a different sheet, update the `spreadsheet_id` in `browser_use.py`

### **Troubleshooting:**
- If you get authentication errors, check that your service account JSON is complete
- If emails aren't sending, verify your Gmail app password is correct
- If the app crashes, check the Vercel function logs for error details

## 📋 Complete Checklist

Before deploying, ensure you have:

- [ ] OpenAI API key
- [ ] Google Service Account JSON file
- [ ] Gmail address (if sending emails)
- [ ] Gmail app password (if sending emails)
- [ ] Google Sheet shared with service account
- [ ] All environment variables set in Vercel
- [ ] Project deployed to Vercel 