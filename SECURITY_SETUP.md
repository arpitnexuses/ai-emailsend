# Security Setup Guide

## 🔐 How to Handle Sensitive Files

### **Local Development Setup**

For local development, keep these files in your project directory but **NEVER commit them**:

1. **`.env.local`** - Your OpenAI API key
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   ```

2. **`service_account.json`** - Google Service Account credentials
   - Download from Google Cloud Console
   - Contains private keys for Google Sheets access

3. **`token.pickle`** - Google OAuth tokens
   - Automatically generated when you first authenticate
   - Contains access and refresh tokens

### **Production Deployment (Vercel)**

For production, use environment variables instead of files:

1. **Set these environment variables in Vercel dashboard:**
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `GOOGLE_SERVICE_ACCOUNT_JSON` - The entire content of your service_account.json file (as JSON string)
   - `EMAIL_USER` - Your Gmail address (optional)
   - `EMAIL_PASSWORD` - Your Gmail app password (optional)

2. **How to set GOOGLE_SERVICE_ACCOUNT_JSON:**
   ```bash
   # Copy the content of your service_account.json file
   cat service_account.json
   # Copy the entire JSON output and paste it as the environment variable value
   ```

### **File Structure**

```
AI-BrowserAgent/
├── .gitignore              # Prevents sensitive files from being committed
├── .env.local              # Local environment variables (NOT committed)
├── service_account.json    # Google credentials (NOT committed)
├── token.pickle           # OAuth tokens (NOT committed)
├── app.py                 # Flask application
├── browser_use.py         # Updated to support both local files and env vars
└── ... (other files)
```

### **How the Code Works**

The updated `browser_use.py` now supports both scenarios:

1. **Production**: Uses `GOOGLE_SERVICE_ACCOUNT_JSON` environment variable
2. **Development**: Falls back to local `service_account.json` and `token.pickle` files

### **Security Best Practices**

✅ **DO:**
- Keep sensitive files locally for development
- Use environment variables for production
- Never commit `.env.local`, `service_account.json`, or `token.pickle`
- Use app passwords for Gmail (not your regular password)

❌ **DON'T:**
- Commit sensitive files to git
- Share your API keys or credentials
- Use regular Gmail passwords (use app passwords instead)

### **Troubleshooting**

**If you get authentication errors:**
1. Check that your `service_account.json` is valid
2. Ensure the Google Sheets API is enabled in Google Cloud Console
3. Verify the spreadsheet ID is correct
4. Make sure the service account has access to the spreadsheet

**If environment variables aren't working:**
1. Check that the JSON is properly formatted
2. Ensure there are no extra spaces or characters
3. Verify the environment variable name is exactly `GOOGLE_SERVICE_ACCOUNT_JSON`

### **Getting Google Service Account Credentials**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API
4. Create a Service Account
5. Download the JSON key file
6. Share your Google Sheet with the service account email

### **Getting Gmail App Password**

1. Enable 2-factor authentication on your Google account
2. Go to Google Account settings → Security
3. Generate an "App Password" for "Mail"
4. Use this password in your `EMAIL_PASSWORD` environment variable 