from bs4 import BeautifulSoup
import requests
import time
import asyncio
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import platform
import subprocess
import re
import json
import pickle
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class Agent:
    def __init__(self, task, llm):
        print("🔧 Initializing Agent for manual use only...")
        self.task = task
        self.llm = llm
        self.driver = None
        self.sheet = None
        self.spreadsheet_id = "1dfm728PBOjBzr2c1OVdPG-9xau6kIoMabeXjM7I8Wes"
        self.setup_services()
        print("✅ Agent initialized successfully - NO EMAILS SENT - waiting for manual commands only.")

    def setup_services(self):
        try:
            print("\n🔧 Setting up services (NO EMAILS WILL BE SENT)...")
            
            # Setup Google Sheets with OAuth2 (this is what we actually need)
            print("\n🔧 Setting up Google Sheets connection...")
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            creds = None
            
            # The file token.pickle stores the user's access and refresh tokens
            if os.path.exists('token.pickle'):
                print("Found existing token.pickle, loading credentials...")
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            
            # If there are no (valid) credentials available, let the user log in
            if not creds or not creds.valid:
                print("No valid credentials found, starting OAuth flow...")
                if creds and creds.expired and creds.refresh_token:
                    print("Refreshing expired credentials...")
                    creds.refresh(Request())
                else:
                    print("Starting new OAuth flow...")
                    if not os.path.exists('service_account.json'):
                        print("Error: service_account.json not found!")
                        return
                    
                    print("Loading client secrets from service_account.json...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'service_account.json', SCOPES)
                    print("Starting local server for OAuth...")
                    creds = flow.run_local_server(port=8080)
                
                print("Saving credentials to token.pickle...")
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            
            print("Authorizing with Google Sheets...")
            gc = gspread.authorize(creds)
            print(f"Opening spreadsheet with ID: {self.spreadsheet_id}")
            self.sheet = gc.open_by_key(self.spreadsheet_id).sheet1
            print("✅ Successfully connected to Google Sheets!")
            print("⚠️  REMEMBER: NO EMAILS WILL BE SENT UNTIL USER CLICKS 'SEND CAMPAIGN'")
            
            # Chrome driver is not needed for email campaigns, so we skip it
            print("ℹ️  Chrome driver not needed for email campaigns - skipping browser setup")
            
        except Exception as e:
            print(f"\n❌ Error in setup_services: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            print(f"Full error traceback:\n{traceback.format_exc()}")
            raise

    async def send_email(self, to_email, subject, body):
        """Send a single email - ONLY CALLED MANUALLY"""
        try:
            print(f"\n📧 MANUAL EMAIL SEND to: {to_email}")
            
            # Get email credentials from environment variables
            sender_email = os.getenv('EMAIL_USER')
            sender_password = os.getenv('EMAIL_PASSWORD')
            
            if not sender_email or not sender_password:
                print("Error: Email credentials not found in environment variables")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to Gmail's SMTP server
            print("Connecting to Gmail SMTP server...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            
            # Login
            print("Logging in to Gmail...")
            server.login(sender_email, sender_password)
            
            # Send email
            print("Sending email...")
            server.send_message(msg)
            
            # Close connection
            server.quit()
            print("✅ Email sent successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            return False

    async def send_campaign_emails(self, pitch, contact_ids):
        """Send emails to specific contacts with personalized content - ONLY CALLED WHEN USER CLICKS BUTTON"""
        try:
            print(f"\n🚀 USER CLICKED SEND CAMPAIGN - Starting manual email campaign...")
            print(f"📝 Pitch: {pitch[:50]}...")
            print(f"👥 Selected contacts: {contact_ids}")
            
            if not self.sheet:
                return "Error: Google Sheets not properly initialized. Please check service_account.json setup."
            
            print("Getting all values from sheet...")
            all_values = self.sheet.get_all_values()
            if len(all_values) <= 1:  # Only header row
                return "No data found in the sheet."
            
            print(f"Processing {len(contact_ids)} selected contacts...")
            
            results = []
            
            # Process selected contacts
            for i, contact_id in enumerate(contact_ids, 1):
                if contact_id <= len(all_values) - 1:
                    row = all_values[contact_id]  # contact_id is 1-indexed, so no need to add 1
                    if len(row) >= 5:
                        firstname, lastname, email, company_name, website = row[:5]
                        if email:
                            print(f"Generating email for: {firstname} {lastname} ({email})")
                            
                            # Generate personalized email content using LLM
                            prompt = f"""Write a direct, personal email to {firstname} {lastname} from me (not a third party).
                            Company: {company_name}
                            Website: {website}
                            
                            Base Pitch Inspiration: {pitch}
                            
                            Guidelines:
                            - Write as if you are me directly writing to them
                            - Be personal and engaging
                            - Focus on their company and how we can help
                            - Keep it concise and professional (150-180 words)
                            - Include a clear call to action
                            - Use simple, clear language
                            - Mention interest in partnership
                            - Refer to their company name and website
                            
                            Format:
                            Subject: [Write a compelling subject line]
                            
                            [Write the email body]"""
                            
                            print("Sending prompt to LLM...")
                            response = await self.llm.ainvoke(prompt)
                            email_content = response.content
                            print("Received response from LLM")
                            
                            # Extract subject and body from the response
                            subject = "Follow-up from AI Assistant"
                            body = email_content
                            if "Subject:" in email_content:
                                subject = email_content.split("Subject:")[1].split("\n")[0].strip()
                                body = email_content.split("Subject:")[1].split("\n", 1)[1].strip()
                            
                            # Send the email
                            print(f"Sending email to {email}...")
                            email_sent = await self.send_email(email, subject, body)
                            
                            # Update the sheet with the status and pitch
                            status = "Sent" if email_sent else "Failed"
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            # Update the sheet
                            row_num = contact_id + 1  # +1 because we skipped header
                            self.sheet.update_cell(row_num, 6, body)  # Pitch column
                            self.sheet.update_cell(row_num, 7, f"Status: {status} | Time: {timestamp} | Email: {email}")
                            
                            # Store the generated content
                            results.append({
                                'contact_id': contact_id,
                                'email': email,
                                'name': f"{firstname} {lastname}",
                                'status': status,
                                'timestamp': timestamp,
                                'subject': subject,
                                'body': body
                            })
                            print(f"✅ Successfully processed email for {email}")
                            
                            # Add 50-second delay between emails to prevent rate limiting
                            if contact_id != contact_ids[-1]:  # Don't delay after the last email
                                remaining = len(contact_ids) - i
                                print(f"⏳ Waiting 50 seconds before next email... ({remaining} emails remaining)")
                                await asyncio.sleep(50)
                                print(f"⏰ 50-second delay completed, continuing with next email...")
                        else:
                            print(f"⚠️  Skipping contact {contact_id}: No email address found")
                    else:
                        print(f"⚠️  Skipping contact {contact_id}: Insufficient data")
            
            print(f"\n✅ MANUAL CAMPAIGN COMPLETED: {len(results)} emails sent")
            return results
            
        except Exception as e:
            print(f"\n❌ Error in send_campaign_emails: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            print(f"Full error traceback:\n{traceback.format_exc()}")
            return []

    def get_contacts(self):
        """Get contacts from Google Sheets - NO EMAILS SENT"""
        try:
            print("📋 Getting contacts from Google Sheets (NO EMAILS SENT)...")
            if not self.sheet:
                return []
            
            all_values = self.sheet.get_all_values()
            if len(all_values) <= 1:
                return []
            
            contacts = []
            for i, row in enumerate(all_values[1:], 1):
                if len(row) >= 5:
                    firstname, lastname, email, company_name, website = row[:5]
                    if email:
                        contacts.append({
                            'id': i,
                            'firstname': firstname,
                            'lastname': lastname,
                            'email': email,
                            'company_name': company_name,
                            'website': website,
                            'status': row[6] if len(row) > 6 else '',
                            'pitch': row[5] if len(row) > 5 else ''
                        })
            
            print(f"✅ Found {len(contacts)} contacts (NO EMAILS SENT)")
            return contacts
        except Exception as e:
            print(f"❌ Error getting contacts: {str(e)}")
            return []

    def get_campaign_status(self):
        """Get campaign status - NO EMAILS SENT"""
        try:
            print("📊 Getting campaign status (NO EMAILS SENT)...")
            if not self.sheet:
                return {"total_contacts": 0, "sent": 0, "failed": 0, "pending": 0}
            
            all_values = self.sheet.get_all_values()
            if len(all_values) <= 1:
                return {"total_contacts": 0, "sent": 0, "failed": 0, "pending": 0}
            
            total_contacts = 0
            sent_count = 0
            failed_count = 0
            
            for row in all_values[1:]:
                if len(row) >= 5 and row[2]:  # Check if email exists
                    total_contacts += 1
                    if len(row) > 6 and "Status: Sent" in row[6]:
                        sent_count += 1
                    elif len(row) > 6 and "Status: Failed" in row[6]:
                        failed_count += 1
            
            status = {
                "total_contacts": total_contacts,
                "sent": sent_count,
                "failed": failed_count,
                "pending": total_contacts - sent_count - failed_count
            }
            
            print(f"✅ Campaign status: {status} (NO EMAILS SENT)")
            return status
        except Exception as e:
            print(f"❌ Error getting campaign status: {str(e)}")
            return {"total_contacts": 0, "sent": 0, "failed": 0, "pending": 0} 