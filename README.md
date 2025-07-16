# Email Campaign Manager

A modern web application for managing and sending personalized email campaigns using AI. This system allows you to input a pitch template and automatically personalize it for each contact in your Google Sheets.

## Features

- 📧 **AI-Powered Personalization**: Uses GPT-4 to personalize your pitch for each contact
- 📊 **Real-time Dashboard**: Track campaign statistics and results
- 🎯 **Contact Management**: Select specific contacts or send to all
- 📈 **Campaign Analytics**: View detailed results and email previews
- 🔄 **Google Sheets Integration**: Automatically syncs with your Google Sheets
- ✨ **Modern UI**: Beautiful, responsive interface built with Tailwind CSS
- 🔧 **Connection Testing**: Test all integrations before sending campaigns
- 📝 **Pitch Examples**: Pre-built templates to get you started quickly

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Environment

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
EMAIL_USER=your_gmail_address@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

### 3. Setup Google Sheets

1. Create a Google Sheet with these columns:
   - First Name
   - Last Name
   - Email
   - Company Name
   - Website
   - Pitch (auto-filled)
   - Status (auto-filled)

2. Share the sheet with your service account email
3. Update `spreadsheet_id` in `browser_use.py`

### 4. Start the Application

**Option 1: Use the startup script (recommended)**
```bash
python3 start_campaign.py
```

**Option 2: Start directly**
```bash
python3 app.py
```

The application will be available at `http://localhost:5000`

## How to Use

### 1. Test Your Setup

Click the "Test Connection" button in the header to verify:
- Google Sheets connection
- OpenAI API access
- Email configuration
- Contact count

### 2. Create Your Campaign

1. **Enter Your Pitch**: Write a base pitch template or click "Load Example" for a sample
2. **Select Contacts**: Choose which contacts to email (already sent contacts are disabled)
3. **Send Campaign**: Click "Send Campaign" to start the email automation

### 3. Monitor Results

- Real-time updates show campaign progress
- View detailed results with email previews
- Check status of each email (Sent/Failed)
- Results are automatically saved to your Google Sheet

## API Endpoints

### GET /api/contacts
Returns all contacts from the Google Sheet

### POST /api/send-campaign
Sends emails to selected contacts with personalized content

**Request Body:**
```json
{
  "pitch": "Your pitch template here",
  "contact_ids": [1, 2, 3]
}
```

### GET /api/campaign-status
Returns campaign statistics

### GET /api/test-connection
Tests all integrations and returns status

## File Structure

```
├── app.py                 # Flask backend API
├── start_campaign.py      # Startup script with environment checks
├── browser_use.py         # Email automation logic
├── main_new.py           # Original script (for reference)
├── templates/
│   └── index.html        # Main frontend template
├── static/
│   └── js/
│       └── app.js        # Frontend JavaScript
├── requirements.txt       # Python dependencies
├── service_account.json   # Google Service Account credentials
└── .env                  # Environment variables
```

## Troubleshooting

### Common Issues

1. **"Google Sheets not properly initialized"**
   - Check that `service_account.json` exists and is valid
   - Verify the spreadsheet ID is correct
   - Ensure the service account has access to the sheet

2. **"Email credentials not found"**
   - Check that `EMAIL_USER` and `EMAIL_PASSWORD` are set in `.env`
   - Use an App Password for Gmail, not your regular password

3. **"Failed to send campaign"**
   - Check your internet connection
   - Verify your OpenAI API key is valid
   - Ensure you have sufficient OpenAI credits

### Debug Mode

To run in debug mode with more detailed error messages:

```bash
export FLASK_ENV=development
python3 app.py
```

### Environment Setup

For Gmail App Password:
1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password for "Mail"

## Security Notes

- Never commit your `.env` file or `service_account.json` to version control
- Use App Passwords for Gmail instead of your regular password
- Keep your OpenAI API key secure
- Regularly rotate your credentials

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. 