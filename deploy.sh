#!/bin/bash

# 🚀 Vercel Deployment Script
echo "🚀 Preparing for Vercel deployment..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found!"
    echo "Please initialize git and add your files:"
    echo "  git init"
    echo "  git add ."
    echo "  git commit -m 'Initial commit'"
    exit 1
fi

# Check if all required files exist
echo "📋 Checking required files..."

required_files=(
    "app.py"
    "browser_use.py"
    "vercel.json"
    "requirements.txt"
    "runtime.txt"
    "templates/index.html"
    "static/js/app.js"
)

missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Missing required files:"
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
    exit 1
fi

echo "✅ All required files found!"

# Check if .env file exists (for local testing)
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found (this is okay for deployment)"
    echo "   Make sure to set environment variables in Vercel dashboard:"
    echo "   - OPENAI_API_KEY"
    echo "   - EMAIL_USER (optional)"
    echo "   - EMAIL_PASSWORD (optional)"
fi

# Check git status
echo "📊 Git status:"
git status --porcelain

# Ask user to commit changes
echo ""
echo "📝 Do you want to commit and push changes? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "💾 Committing changes..."
    git add .
    git commit -m "Ready for Vercel deployment"
    
    echo "📤 Pushing to GitHub..."
    git push origin main
    
    echo ""
    echo "✅ Code pushed to GitHub!"
    echo ""
    echo "🌐 Next steps:"
    echo "1. Go to https://vercel.com"
    echo "2. Click 'New Project'"
    echo "3. Import your GitHub repository"
    echo "4. Set environment variables in Vercel dashboard"
    echo "5. Deploy!"
    echo ""
    echo "📋 Required environment variables:"
echo "   - OPENAI_API_KEY"
echo "   - GOOGLE_SERVICE_ACCOUNT_JSON (for Google Sheets access)"
echo "   - EMAIL_USER (optional)"
echo "   - EMAIL_PASSWORD (optional)"
else
    echo "⏭️  Skipping git operations"
    echo ""
    echo "📋 Manual deployment steps:"
    echo "1. git add ."
    echo "2. git commit -m 'Ready for deployment'"
    echo "3. git push origin main"
    echo "4. Deploy to Vercel"
fi

echo ""
echo "🎯 Deployment files ready!"
echo "📁 Files included:"
echo "   ✅ app.py - Flask application"
echo "   ✅ browser_use.py - Agent class"
echo "   ✅ vercel.json - Vercel configuration"
echo "   ✅ requirements.txt - Python dependencies"
echo "   ✅ runtime.txt - Python version"
echo "   ✅ templates/index.html - Frontend"
echo "   ✅ static/js/app.js - Frontend JavaScript"
echo "   ✅ Environment variables - Google Sheets credentials (GOOGLE_SERVICE_ACCOUNT_JSON)" 