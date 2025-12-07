"""
Notification System for Email and SMS
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import NOTIFICATION_CONFIG
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.email_config = NOTIFICATION_CONFIG
        self.twilio_client = None
        self.initialize_twilio()
    
    def initialize_twilio(self):
        """Initialize Twilio client if credentials are available"""
        try:
            if self.email_config['twilio_account_sid'] and self.email_config['twilio_auth_token']:
                from twilio.rest import Client
                self.twilio_client = Client(
                    self.email_config['twilio_account_sid'],
                    self.email_config['twilio_auth_token']
                )
        except Exception as e:
            print(f"Twilio initialization failed: {e}. SMS notifications will be simulated.")
    
    def send_appointment_confirmation(self, appointment_data, send_email=True, send_sms=True):
        """Send appointment confirmation via email and SMS"""
        try:
            client_email = appointment_data.get('client_email')
            client_phone = appointment_data.get('client_phone')
            client_name = appointment_data.get('client_name')
            appointment_number = appointment_data.get('appointment_number')
            appointment_date = appointment_data.get('appointment_date')
            appointment_time = appointment_data.get('appointment_time')
            service_type = appointment_data.get('service_type')
            
            message_body = f"""
Dear {client_name},

Your appointment has been successfully booked!

Appointment Details:
- Appointment Number: {appointment_number}
- Service: {service_type}
- Date: {appointment_date}
- Time: {appointment_time}

Please arrive 10 minutes early. If you need to reschedule, please contact us with your appointment number.

Thank you,
AppointmentPro Team
            """
            
            results = {}
            
            if send_email and client_email:
                results['email'] = self.send_email(
                    to_email=client_email,
                    subject=f"Appointment Confirmation - {appointment_number}",
                    body=message_body
                )
            
            if send_sms and client_phone:
                results['sms'] = self.send_sms(
                    phone_number=client_phone,
                    message=f"AppointmentPro: Your appointment {appointment_number} is confirmed for {appointment_date} at {appointment_time}."
                )
            
            return {
                'success': True,
                'message': 'Notifications sent successfully',
                'results': results
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_email(self, to_email, subject, body):
        """Send email notification"""
        try:
            # If SMTP credentials are configured, send real email
            if self.email_config['smtp_username'] and self.email_config['smtp_password']:
                msg = MIMEMultipart()
                msg['From'] = self.email_config['email_from']
                msg['To'] = to_email
                msg['Subject'] = subject
                
                msg.attach(MIMEText(body, 'plain'))
                
                server = smtplib.SMTP(
                    self.email_config['smtp_server'],
                    self.email_config['smtp_port']
                )
                server.starttls()
                server.login(
                    self.email_config['smtp_username'],
                    self.email_config['smtp_password']
                )
                server.send_message(msg)
                server.quit()
                
                return {'success': True, 'message': f'Email sent to {to_email}'}
            else:
                # Simulate email sending for development
                print(f"[EMAIL SIMULATION] To: {to_email}")
                print(f"[EMAIL SIMULATION] Subject: {subject}")
                print(f"[EMAIL SIMULATION] Body: {body}")
                return {'success': True, 'message': f'Email simulated for {to_email}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_sms(self, phone_number, message):
        """Send SMS notification"""
        try:
            # If Twilio is configured, send real SMS
            if self.twilio_client:
                sms = self.twilio_client.messages.create(
                    body=message,
                    from_=self.email_config['twilio_phone_number'],
                    to=phone_number
                )
                return {
                    'success': True,
                    'message': f'SMS sent to {phone_number}',
                    'sms_id': sms.sid
                }
            else:
                # Simulate SMS sending for development
                print(f"[SMS SIMULATION] To: {phone_number}")
                print(f"[SMS SIMULATION] Message: {message}")
                return {'success': True, 'message': f'SMS simulated for {phone_number}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_reminder(self, appointment_data):
        """Send appointment reminder"""
        try:
            client_email = appointment_data.get('client_email')
            client_phone = appointment_data.get('client_phone')
            appointment_number = appointment_data.get('appointment_number')
            appointment_date = appointment_data.get('appointment_date')
            appointment_time = appointment_data.get('appointment_time')
            
            reminder_message = f"Reminder: Your appointment {appointment_number} is scheduled for {appointment_date} at {appointment_time}."
            
            results = {}
            
            if client_email:
                results['email'] = self.send_email(
                    to_email=client_email,
                    subject=f"Appointment Reminder - {appointment_number}",
                    body=reminder_message
                )
            
            if client_phone:
                results['sms'] = self.send_sms(
                    phone_number=client_phone,
                    message=reminder_message
                )
            
            return {
                'success': True,
                'message': 'Reminders sent successfully',
                'results': results
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_status_update(self, appointment_data, new_status):
        """Send status update notification"""
        try:
            client_email = appointment_data.get('client_email')
            appointment_number = appointment_data.get('appointment_number')
            
            message_body = f"""
Your appointment {appointment_number} status has been updated to: {new_status}

If you have any questions, please contact us with your appointment number.

AppointmentPro Team
            """
            
            if client_email:
                return self.send_email(
                    to_email=client_email,
                    subject=f"Appointment Status Update - {appointment_number}",
                    body=message_body
                )
            else:
                return {'success': True, 'message': 'Status update notification prepared'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Initialize notification service
notification_service = NotificationService()
