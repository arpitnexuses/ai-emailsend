# 🚀 Vercel Deployment Guide

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Account**: Your code should be in a GitHub repository
3. **Vercel CLI** (optional): `npm i -g vercel`

## 📋 Required Environment Variables

Set these in your Vercel dashboard under **Settings > Environment Variables**:

### Required:
- `OPENAI_API_KEY` - Your OpenAI API key

### Optional (for email functionality):
- `EMAIL_USER` - Your Gmail address
- `EMAIL_PASSWORD` - Your Gmail app password

## 🔧 Deployment Steps

### Method 1: Vercel Dashboard (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push origin main
   ```

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect it's a Python app

3. **Configure Environment Variables**:
   - In your project dashboard, go to **Settings > Environment Variables**
   - Add all required variables listed above

4. **Deploy**:
   - Click "Deploy"
   - Vercel will build and deploy your app

### Method 2: Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Set Environment Variables**:
   ```bash
   vercel env add OPENAI_API_KEY
   vercel env add EMAIL_USER
   vercel env add EMAIL_PASSWORD
   ```

## 📁 Required Files for Deployment

Your repository should contain:
- ✅ `app.py` - Main Flask application
- ✅ `browser_use.py` - Agent class
- ✅ `vercel.json` - Vercel configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `runtime.txt` - Python version
- ✅ `templates/index.html` - Frontend template
- ✅ `static/js/app.js` - Frontend JavaScript
- ✅ `service_account.json` - Google Sheets credentials

## ⚠️ Important Notes

### 1. **Serverless Limitations**:
- Each request creates a new Agent instance
- No persistent connections between requests
- Maximum execution time: 10 seconds (free) / 5 minutes (pro)

### 2. **Email Campaign Limitations**:
- Long-running email campaigns may timeout
- Consider breaking large campaigns into smaller batches
- Monitor Vercel function execution times

### 3. **Google Sheets Authentication**:
- `token.pickle` will be recreated on each deployment
- First request may require OAuth authentication
- Consider using service account authentication for production

### 4. **Environment Variables**:
- Never commit sensitive data to Git
- Use Vercel's environment variable system
- Test locally with `.env` file

## 🔍 Troubleshooting

### Common Issues:

1. **Import Errors**:
   - Check `requirements.txt` has all dependencies
   - Ensure Python version in `runtime.txt` is correct

2. **Environment Variables**:
   - Verify all variables are set in Vercel dashboard
   - Check variable names match exactly

3. **Google Sheets Access**:
   - Ensure `service_account.json` is in repository
   - Verify spreadsheet is shared with service account email

4. **Function Timeouts**:
   - Email campaigns may timeout on free tier
   - Consider upgrading to Pro plan for longer execution times

## 🎯 Production Recommendations

1. **Upgrade to Vercel Pro** for:
   - Longer function execution times (up to 5 minutes)
   - Better performance and reliability

2. **Use Service Account Authentication**:
   - More reliable than OAuth for serverless
   - No user interaction required

3. **Implement Queue System**:
   - For large email campaigns
   - Consider using external queue service

4. **Monitor Usage**:
   - Track Vercel function execution times
   - Monitor API usage and costs

## 📞 Support

If you encounter issues:
1. Check Vercel deployment logs
2. Verify environment variables are set correctly
3. Test locally first with `python app.py`
4. Check Google Sheets permissions and service account setup 