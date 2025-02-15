# Cleaning Business Management System

A comprehensive management system for cleaning businesses built with Streamlit and FastAPI.

## Features

- Client Management
- Team Member Management
- Automated Rostering
- SMS Notifications
- Invoicing System
- GST Handling
- Payment Tracking

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your configuration details

5. Initialize the database:
   ```bash
   python src/models/init_db.py
   ```

6. Run the application:
   ```bash
   streamlit run src/app.py
   ```

## Environment Variables

Create a `.env` file with the following variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/cleaning_business
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
JWT_SECRET_KEY=your_secret_key
```

## Project Structure

```
cleaning_business_system/
├── src/
│   ├── models/        # Database models
│   ├── routes/        # API routes
│   ├── utils/         # Utility functions
│   ├── templates/     # HTML templates
│   └── app.py         # Main Streamlit application
├── static/
│   ├── css/          # Stylesheets
│   └── js/           # JavaScript files
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```
