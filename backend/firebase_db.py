"""
Firebase Database Helper Module
"""
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime, timedelta
import uuid
from config import FIREBASE_CONFIG

class FirebaseDB:
    def __init__(self):
        self.db = None
        self.initialize()
    
    def initialize(self):
        """Initialize Firebase Admin SDK"""
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(FIREBASE_CONFIG['serviceAccountKey'])
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
        except Exception as e:
            print(f"Firebase initialization error: {e}")
    
    # ============ APPOINTMENT OPERATIONS ============
    
    def create_appointment(self, service_type, client_data, appointment_data):
        """Create a new appointment"""
        try:
            appointment_number = self.generate_appointment_number()
            
            appointment = {
                'appointment_number': appointment_number,
                'service_type': service_type,
                'client_name': client_data.get('client_name'),
                'client_email': client_data.get('client_email'),
                'client_phone': client_data.get('client_phone'),
                'appointment_date': appointment_data.get('appointment_date'),
                'appointment_time': appointment_data.get('appointment_time'),
                'purpose': appointment_data.get('purpose', ''),
                'status': 'Pending',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Save to Firestore
            doc_ref = self.db.collection('appointments').document()
            doc_ref.set(appointment)
            
            return {
                'success': True,
                'appointment_number': appointment_number,
                'appointment_id': doc_ref.id,
                'data': appointment
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_appointments(self, service_type=None, status=None, date=None):
        """Retrieve appointments with optional filters"""
        try:
            query = self.db.collection('appointments')
            
            if service_type:
                query = query.where('service_type', '==', service_type)
            if status:
                query = query.where('status', '==', status)
            if date:
                query = query.where('appointment_date', '==', date)
            
            docs = query.stream()
            appointments = []
            for doc in docs:
                appt = doc.to_dict()
                appt['id'] = doc.id
                appointments.append(appt)
            
            return {'success': True, 'data': appointments}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_appointment_by_id(self, appointment_id):
        """Get a specific appointment"""
        try:
            doc = self.db.collection('appointments').document(appointment_id).get()
            if doc.exists:
                appt = doc.to_dict()
                appt['id'] = doc.id
                return {'success': True, 'data': appt}
            else:
                return {'success': False, 'error': 'Appointment not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def update_appointment_status(self, appointment_id, new_status):
        """Update appointment status"""
        try:
            self.db.collection('appointments').document(appointment_id).update({
                'status': new_status,
                'updated_at': datetime.now().isoformat()
            })
            return {'success': True, 'message': f'Appointment updated to {new_status}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_appointment(self, appointment_id):
        """Delete/cancel an appointment"""
        try:
            self.db.collection('appointments').document(appointment_id).delete()
            return {'success': True, 'message': 'Appointment deleted'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def check_availability(self, service_type, appointment_date, appointment_time):
        """Check if a time slot is available"""
        try:
            query = self.db.collection('appointments').where('service_type', '==', service_type) \
                                                       .where('appointment_date', '==', appointment_date) \
                                                       .where('appointment_time', '==', appointment_time) \
                                                       .where('status', 'in', ['Pending', 'Confirmed'])
            docs = query.stream()
            count = len(list(docs))
            
            return {
                'success': True,
                'available': count == 0,
                'booked_count': count
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ============ USER OPERATIONS ============
    
    def create_client_user(self, email, password, name, phone):
        """Create a new client user"""
        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=name
            )
            
            # Store additional user data in Firestore
            self.db.collection('clients').document(user.uid).set({
                'uid': user.uid,
                'email': email,
                'name': name,
                'phone': phone,
                'created_at': datetime.now().isoformat(),
                'role': 'client'
            })
            
            return {'success': True, 'uid': user.uid}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_staff_user(self, email, password, name, phone, role):
        """Create a new staff user"""
        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=name
            )
            
            self.db.collection('staff').document(user.uid).set({
                'uid': user.uid,
                'email': email,
                'name': name,
                'phone': phone,
                'role': role,
                'created_at': datetime.now().isoformat()
            })
            
            return {'success': True, 'uid': user.uid}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_user_by_email(self, email, user_type='client'):
        """Get user by email"""
        try:
            collection = 'clients' if user_type == 'client' else 'staff'
            docs = self.db.collection(collection).where('email', '==', email).stream()
            
            for doc in docs:
                user = doc.to_dict()
                user['id'] = doc.id
                return {'success': True, 'data': user}
            
            return {'success': False, 'error': 'User not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_user_by_uid(self, uid, user_type='client'):
        """Get user by UID"""
        try:
            collection = 'clients' if user_type == 'client' else 'staff'
            doc = self.db.collection(collection).document(uid).get()
            
            if doc.exists:
                user = doc.to_dict()
                return {'success': True, 'data': user}
            else:
                return {'success': False, 'error': 'User not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ============ UTILITY FUNCTIONS ============
    
    def generate_appointment_number(self):
        """Generate a unique appointment number (APP-YYYYMMDD-XXXX)"""
        from datetime import datetime
        date_str = datetime.now().strftime('%Y%m%d')
        unique_id = str(uuid.uuid4())[:4].upper()
        return f"APP-{date_str}-{unique_id}"
    
    def get_available_slots(self, service_type, appointment_date, duration_mins=30):
        """Get available time slots for a given date"""
        try:
            from config import APP_SETTINGS
            
            # Get all booked appointments for the date
            booked = self.db.collection('appointments') \
                           .where('service_type', '==', service_type) \
                           .where('appointment_date', '==', appointment_date) \
                           .where('status', 'in', ['Pending', 'Confirmed']) \
                           .stream()
            
            booked_times = set()
            for doc in booked:
                booked_times.add(doc.get('appointment_time'))
            
            # Generate available slots
            slots = []
            start_hour = APP_SETTINGS['business_hours_start']
            end_hour = APP_SETTINGS['business_hours_end']
            slot_duration = APP_SETTINGS['slot_duration_minutes']
            
            current_time = datetime.strptime(f"{start_hour:02d}:00", "%H:%M")
            end_time = datetime.strptime(f"{end_hour:02d}:00", "%H:%M")
            
            while current_time < end_time:
                time_str = current_time.strftime("%H:%M")
                if time_str not in booked_times:
                    slots.append(time_str)
                current_time += timedelta(minutes=slot_duration)
            
            return {'success': True, 'slots': slots}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_statistics(self):
        """Get appointment statistics"""
        try:
            # Total appointments
            total = len(list(self.db.collection('appointments').stream()))
            
            # Pending appointments
            pending = len(list(self.db.collection('appointments').where('status', '==', 'Pending').stream()))
            
            # Confirmed appointments
            confirmed = len(list(self.db.collection('appointments').where('status', '==', 'Confirmed').stream()))
            
            # Completed appointments
            completed = len(list(self.db.collection('appointments').where('status', '==', 'Completed').stream()))
            
            return {
                'success': True,
                'total_appointments': total,
                'pending': pending,
                'confirmed': confirmed,
                'completed': completed
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Initialize database
firebase_db = FirebaseDB()
