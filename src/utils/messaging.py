from twilio.rest import Client
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class MessageService:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')  # Changed to match .env.example
        
        if not all([self.account_sid, self.auth_token, self.from_number]):
            print(f"Missing Twilio credentials:")
            print(f"TWILIO_ACCOUNT_SID: {'Set' if self.account_sid else 'Missing'}")
            print(f"TWILIO_AUTH_TOKEN: {'Set' if self.auth_token else 'Missing'}")
            print(f"TWILIO_PHONE_NUMBER: {'Set' if self.from_number else 'Missing'}")
            self.client = None
        else:
            try:
                self.client = Client(self.account_sid, self.auth_token)
            except Exception as e:
                print(f"Error initializing Twilio client: {str(e)}")
                self.client = None

    def send_message(self, to_number: str, message: str) -> dict:
        """Send a message using Twilio"""
        if not self.client:
            error_msg = "Twilio client not initialized. Check credentials."
            print(error_msg)
            return {"success": False, "error": error_msg}
        
        try:
            print(f"Attempting to send message to {to_number} from {self.from_number}")
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            print(f"Message sent successfully. SID: {message.sid}")
            return {"success": True, "message_sid": message.sid}
        except Exception as e:
            error_msg = f"Failed to send message: {str(e)}"
            print(error_msg)
            return {"success": False, "error": error_msg}

    def format_phone_number(self, phone: str) -> str:
        """Format phone number to E.164 format"""
        if not isinstance(phone, str):
            phone = str(phone)
            
        # Remove any non-digit characters except plus sign
        phone = ''.join(c for c in phone if c.isdigit() or c == '+')
        
        # Remove leading plus if present
        if phone.startswith('+'):
            phone = phone[1:]
        
        # Add country code if not present
        if not phone.startswith('61'):
            phone = '61' + phone.lstrip('0')
        
        return f"+{phone}"
