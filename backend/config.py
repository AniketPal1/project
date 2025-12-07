"""
Firebase and Flask Configuration
"""
import os
from datetime import timedelta

# Flask Configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'appointment-pro-secret-key-change-in-production'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    JSON_SORT_KEYS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS configuration
    CORS_ORIGINS = ['http://localhost:5500', 'http://localhost:3000', 'http://127.0.0.1:5500']

# Firebase Configuration
FIREBASE_CONFIG = {
    'apiKey': os.environ.get('FIREBASE_API_KEY') or 'YOUR_FIREBASE_API_KEY',
    'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN') or 'your-project.firebaseapp.com',
    'projectId': os.environ.get('FIREBASE_PROJECT_ID') or 'your-project-id',
    'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET') or 'your-project.appspot.com',
    'messagingSenderId': os.environ.get('FIREBASE_MESSAGING_SENDER_ID') or 'YOUR_SENDER_ID',
    'appId': os.environ.get('FIREBASE_APP_ID') or 'YOUR_APP_ID',
    'serviceAccountKey': os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY') or 'firebase-key.json'
}

# Email/SMS Configuration (for notifications)
NOTIFICATION_CONFIG = {
    'email_from': os.environ.get('EMAIL_FROM') or 'noreply@appointmentpro.com',
    'smtp_server': os.environ.get('SMTP_SERVER') or 'smtp.gmail.com',
    'smtp_port': int(os.environ.get('SMTP_PORT') or 587),
    'smtp_username': os.environ.get('SMTP_USERNAME') or '',
    'smtp_password': os.environ.get('SMTP_PASSWORD') or '',
    'twilio_account_sid': os.environ.get('TWILIO_ACCOUNT_SID') or '',
    'twilio_auth_token': os.environ.get('TWILIO_AUTH_TOKEN') or '',
    'twilio_phone_number': os.environ.get('TWILIO_PHONE_NUMBER') or '',
}

# Application Settings
APP_SETTINGS = {
    'business_hours_start': 9,
    'business_hours_end': 17,
    'slot_duration_minutes': 30,
    'max_appointments_per_day': 20,
    'appointment_reminder_hours': 24,
}
