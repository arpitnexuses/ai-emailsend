from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
import asyncio
import os
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize LLM
llm = ChatOpenAI(model="gpt-4")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Get contacts from Google Sheets - NO EMAILS SENT"""
    try:
        print("📋 Getting contacts from Google Sheets...")
        # Create agent for this request (serverless-friendly)
        agent = Agent(task="Get contacts", llm=llm)
        contacts = agent.get_contacts()
        print(f"✅ Found {len(contacts)} contacts")
        return jsonify({"contacts": contacts})
    except Exception as e:
        print(f"❌ Error getting contacts: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/send-campaign', methods=['POST'])
def send_campaign():
    """Send email campaign with custom pitch - ONLY WHEN USER CLICKS BUTTON"""
    try:
        data = request.json
        pitch = data.get('pitch', '')
        contact_ids = data.get('contact_ids', [])
        
        print(f"🎯 USER CLICKED SEND CAMPAIGN - Pitch: {pitch[:50]}...")
        print(f"📧 Selected contacts: {contact_ids}")
        
        if not pitch:
            return jsonify({"error": "Pitch is required"}), 400
        
        if not contact_ids:
            return jsonify({"error": "At least one contact must be selected"}), 400
        
        # Create agent for this request (serverless-friendly)
        agent = Agent(task="Send email campaign", llm=llm)
        
        # Send emails using the new method - ONLY WHEN USER CLICKS
        print("🚀 Starting manual email campaign...")
        results = asyncio.run(agent.send_campaign_emails(pitch, contact_ids))
        
        if isinstance(results, str):
            # Error occurred
            return jsonify({"error": results}), 500
        
        print(f"✅ Manual campaign completed: {len(results)} emails sent")
        return jsonify({
            "success": True,
            "message": f"Campaign sent to {len(results)} contacts",
            "results": results
        })
        
    except Exception as e:
        print(f"❌ Error in send_campaign: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/campaign-status', methods=['GET'])
def get_campaign_status():
    """Get campaign status and statistics - NO EMAILS SENT"""
    try:
        print("📊 Getting campaign status...")
        # Create agent for this request (serverless-friendly)
        agent = Agent(task="Get campaign status", llm=llm)
        status = agent.get_campaign_status()
        print(f"✅ Status: {status}")
        return jsonify(status)
    except Exception as e:
        print(f"❌ Error getting campaign status: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/test-connection', methods=['GET'])
def test_connection():
    """Test connection to Google Sheets and email - NO EMAILS SENT"""
    try:
        print("🔧 Testing connections...")
        # Create agent for this request (serverless-friendly)
        agent = Agent(task="Test connection", llm=llm)
        
        # Test Google Sheets connection
        if not agent.sheet:
            return jsonify({"error": "Google Sheets not properly initialized"}), 500
        
        all_values = agent.sheet.get_all_values()
        contact_count = len(all_values) - 1 if len(all_values) > 1 else 0
        
        # Test email connection (optional - only if credentials are set)
        email_test = "Not configured"
        if os.getenv('EMAIL_USER') and os.getenv('EMAIL_PASSWORD'):
            email_test = "Configured"
        
        result = {
            "success": True,
            "google_sheets": "Connected",
            "contact_count": contact_count,
            "email_config": email_test,
            "openai": "Connected" if os.getenv('OPENAI_API_KEY') else "Not configured"
        }
        
        print(f"✅ Connection test result: {result}")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Error in test_connection: {str(e)}")
        return jsonify({"error": str(e)}), 500

# For Vercel deployment
if __name__ == '__main__':
    app.run(debug=True, port=5001) 