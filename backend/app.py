"""
Flask Application - Appointment Booking System Backend
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from config import Config, FIREBASE_CONFIG
from firebase_db import firebase_db
from notifications import notification_service
import logging

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app, origins=Config.CORS_ORIGINS)
jwt = JWTManager(app)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============ AUTHENTICATION ENDPOINTS ============

@app.route('/api/auth/client-signup', methods=['POST'])
def client_signup():
    """Client registration"""
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['email', 'password', 'name', 'phone']):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        result = firebase_db.create_client_user(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            phone=data['phone']
        )
        
        if result['success']:
            # Create JWT token
            access_token = create_access_token(
                identity=result['uid'],
                additional_claims={'role': 'client'}
            )
            return jsonify({
                'success': True,
                'uid': result['uid'],
                'access_token': access_token,
                'message': 'Registration successful'
            }), 201
        else:
            return jsonify(result), 400
    except Exception as e:
        logger.error(f"Client signup error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/client-login', methods=['POST'])
def client_login():
    """Client login"""
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['email', 'password']):
            return jsonify({'success': False, 'error': 'Email and password required'}), 400
        
        # Verify with Firebase
        from firebase_admin import auth
        try:
            user = auth.get_user_by_email(data['email'])
            # In production, verify password securely
            # This is a simplified version - use Firebase Client SDK for real authentication
            
            access_token = create_access_token(
                identity=user.uid,
                additional_claims={'role': 'client'}
            )
            
            user_data = firebase_db.get_user_by_uid(user.uid, 'client')
            
            return jsonify({
                'success': True,
                'uid': user.uid,
                'access_token': access_token,
                'user': user_data.get('data') if user_data['success'] else {}
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Client login error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/staff-signup', methods=['POST'])
def staff_signup():
    """Staff registration"""
    try:
        data = request.get_json()
        
        required_fields = ['email', 'password', 'name', 'phone', 'role']
        if not all(key in data for key in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        result = firebase_db.create_staff_user(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            phone=data['phone'],
            role=data['role']
        )
        
        if result['success']:
            access_token = create_access_token(
                identity=result['uid'],
                additional_claims={'role': 'staff', 'staff_role': data['role']}
            )
            return jsonify({
                'success': True,
                'uid': result['uid'],
                'access_token': access_token,
                'message': 'Registration successful'
            }), 201
        else:
            return jsonify(result), 400
    except Exception as e:
        logger.error(f"Staff signup error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/staff-login', methods=['POST'])
def staff_login():
    """Staff login"""
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['email', 'password']):
            return jsonify({'success': False, 'error': 'Email and password required'}), 400
        
        from firebase_admin import auth
        try:
            user = auth.get_user_by_email(data['email'])
            
            access_token = create_access_token(
                identity=user.uid,
                additional_claims={'role': 'staff'}
            )
            
            user_data = firebase_db.get_user_by_uid(user.uid, 'staff')
            
            return jsonify({
                'success': True,
                'uid': user.uid,
                'access_token': access_token,
                'user': user_data.get('data') if user_data['success'] else {}
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Staff login error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ APPOINTMENT ENDPOINTS ============

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    """Create a new appointment"""
    try:
        data = request.get_json()
        
        required_fields = ['service_type', 'client_name', 'client_email', 'client_phone', 
                          'appointment_date', 'appointment_time']
        if not all(key in data for key in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Check availability
        availability = firebase_db.check_availability(
            data['service_type'],
            data['appointment_date'],
            data['appointment_time']
        )
        
        if not availability['available']:
            return jsonify({
                'success': False,
                'error': 'Time slot is not available'
            }), 400
        
        # Create appointment
        result = firebase_db.create_appointment(
            service_type=data['service_type'],
            client_data={
                'client_name': data['client_name'],
                'client_email': data['client_email'],
                'client_phone': data['client_phone']
            },
            appointment_data={
                'appointment_date': data['appointment_date'],
                'appointment_time': data['appointment_time'],
                'purpose': data.get('purpose', '')
            }
        )
        
        if result['success']:
            # Send confirmation notification
            notification_service.send_appointment_confirmation(result['data'])
            
            return jsonify({
                'success': True,
                'appointment_number': result['appointment_number'],
                'appointment_id': result['appointment_id'],
                'message': 'Appointment created successfully'
            }), 201
        else:
            return jsonify(result), 400
    except Exception as e:
        logger.error(f"Create appointment error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    """Get appointments with optional filters"""
    try:
        service_type = request.args.get('service_type')
        status = request.args.get('status')
        date = request.args.get('date')
        
        result = firebase_db.get_appointments(
            service_type=service_type,
            status=status,
            date=date
        )
        
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        logger.error(f"Get appointments error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments/<appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """Get a specific appointment"""
    try:
        result = firebase_db.get_appointment_by_id(appointment_id)
        return jsonify(result), 200 if result['success'] else 404
    except Exception as e:
        logger.error(f"Get appointment error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments/<appointment_id>/status', methods=['PUT'])
def update_appointment_status(appointment_id):
    """Update appointment status"""
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'success': False, 'error': 'Status is required'}), 400
        
        result = firebase_db.update_appointment_status(appointment_id, data['status'])
        
        if result['success']:
            # Send status update notification
            appt = firebase_db.get_appointment_by_id(appointment_id)
            if appt['success']:
                appt_data = appt['data']
                appt_data['status'] = data['status']
                notification_service.send_status_update(appt_data, data['status'])
        
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        logger.error(f"Update appointment status error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments/<appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    """Delete/cancel an appointment"""
    try:
        result = firebase_db.delete_appointment(appointment_id)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        logger.error(f"Delete appointment error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/availability', methods=['GET'])
def check_availability():
    """Check appointment availability"""
    try:
        service_type = request.args.get('service_type')
        appointment_date = request.args.get('date')
        
        if not service_type or not appointment_date:
            return jsonify({'success': False, 'error': 'service_type and date are required'}), 400
        
        result = firebase_db.get_available_slots(service_type, appointment_date)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        logger.error(f"Check availability error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ STATISTICS ENDPOINTS ============

@app.route('/api/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    """Get appointment statistics (staff only)"""
    try:
        claims = get_jwt_identity()
        
        result = firebase_db.get_statistics()
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        logger.error(f"Get statistics error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ HEALTH CHECK ============

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'AppointmentPro Backend'
    }), 200

# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# ============ REQUEST/RESPONSE LOGGING ============

@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path}")

@app.after_request
def log_response(response):
    logger.info(f"Response: {response.status_code}")
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
