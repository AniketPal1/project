# AppointmentPro - Complete Appointment Management System

A full-stack appointment booking and management system built with HTML/CSS/JavaScript frontend and Python Flask backend with Firebase integration.

## Project Structure

```
project/
├── frontend/
│   ├── *.html (15 pages: dashboard, login, staff pages, service pages)
│   ├── navbar-footer.html (component template)
│   └── (CSS and JavaScript embedded in HTML files)
│
└── backend/
    ├── app.py (Main Flask application)
    ├── config.py (Configuration and environment settings)
    ├── firebase_db.py (Firestore database operations)
    ├── notifications.py (Email and SMS notification service)
    ├── requirements.txt (Python dependencies)
    ├── .env (Environment variables - create from .env.example)
    ├── .env.example (Template for environment variables)
    ├── frontend_integration.py (JavaScript API client code)
    └── README.md (This file)
```

## Features

### Frontend
- **15 HTML Pages** with responsive design using Tailwind CSS
  - Main dashboard with service grid
  - Client authentication (login/signup)
  - Staff authentication and management dashboard
  - 9 Service-specific booking pages (School, Hospital, Company, Doctor, Advocate, Teacher, Cafe, Barber, Bank)
  - Navigation bar and footer with social media links

- **Appointment Management**
  - Book appointments with automatic appointment number generation (APP-YYYYMMDD-XXXX)
  - Select date and time with availability checking
  - Appointment status management (Pending, Confirmed, Completed, Cancelled)
  - Email and SMS notification simulation

- **Authentication**
  - Client signup/login with flip-card animation
  - Staff signup/login with role selection (Admin, Manager, Staff)
  - Session persistence using localStorage

### Backend (Flask + Firebase)
- **REST API** with 12+ endpoints
  - Authentication (client & staff signup/login)
  - Appointment CRUD operations
  - Availability checking
  - Statistics dashboard
  - Health check

- **Database**
  - Firestore for real-time data storage
  - Firebase Authentication for user management
  - Collections: appointments, clients, staff

- **Notifications**
  - Email support (SMTP or simulation mode)
  - SMS support (Twilio or simulation mode)
  - Appointment confirmations and reminders

## Quick Start

### Prerequisites
- Python 3.8+ installed
- Node.js (optional, for local server)
- Firebase project with Firestore enabled
- Twilio account (optional, for SMS)
- SMTP credentials (optional, for email)

### Step 1: Backend Setup

#### 1.1 Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 1.2 Firebase Configuration
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing project
3. Enable Firestore Database (Start in test mode for development)
4. Enable Authentication (Email/Password)
5. Go to Project Settings → Service Accounts
6. Click "Generate New Private Key"
7. Save the downloaded JSON file as `firebase-key.json` in the `backend/` folder

#### 1.3 Environment Configuration
```bash
# Copy example file
cp .env.example .env

# Edit .env with your Firebase credentials
```

Edit `backend/.env` with values from your Firebase service account JSON:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Firebase Configuration (from firebase-key.json)
FIREBASE_TYPE=service_account
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs

# Optional: SMTP Configuration (for real email)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Optional: Twilio Configuration (for real SMS)
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# Notification Settings
USE_SIMULATION_MODE=True  # Set to False if using real SMTP/Twilio
```

#### 1.4 Run Flask Backend
```bash
# Option 1: Using flask command
flask run

# Option 2: Using Python directly
python app.py

# Option 3: Using Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

The backend will start at `http://localhost:5000`

### Step 2: Verify Backend is Running
```bash
# Test health endpoint
curl http://localhost:5000/api/health
# Should return: {"success": true, "message": "Backend is running"}
```

### Step 3: Frontend Setup

#### 3.1 Serve Frontend Files
Option A: Using Python's built-in server
```bash
cd frontend
python -m http.server 8000
```

Option B: Using Node.js http-server
```bash
npm install -g http-server
cd frontend
http-server -p 8000
```

Option C: Using VS Code Live Server extension
- Right-click on `index.html` → "Open with Live Server"

#### 3.2 Access the Application
Open your browser to:
- **Frontend:** `http://localhost:8000`
- **Backend API:** `http://localhost:5000/api`

### Step 4: Test the System

#### Test Client Signup/Login
```bash
curl -X POST http://localhost:5000/api/auth/client-signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "client@example.com",
    "password": "password123",
    "name": "John Doe",
    "phone": "123-456-7890"
  }'
```

#### Test Creating an Appointment
```bash
# First, get access token from login response
curl -X POST http://localhost:5000/api/appointments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "service_type": "School/College",
    "client_name": "John Doe",
    "client_email": "client@example.com",
    "client_phone": "123-456-7890",
    "appointment_date": "2025-12-20",
    "appointment_time": "14:00",
    "purpose": "Enrollment"
  }'
```

## API Endpoints

### Authentication
- `POST /api/auth/client-signup` - Client registration
- `POST /api/auth/client-login` - Client login
- `POST /api/auth/staff-signup` - Staff registration
- `POST /api/auth/staff-login` - Staff login

### Appointments
- `POST /api/appointments` - Create appointment
- `GET /api/appointments` - List appointments (with filters)
- `GET /api/appointments/<id>` - Get single appointment
- `PUT /api/appointments/<id>/status` - Update appointment status
- `DELETE /api/appointments/<id>` - Delete appointment

### Utilities
- `GET /api/availability` - Check available time slots
- `GET /api/statistics` - Get dashboard statistics
- `GET /api/health` - Health check

## Frontend Integration with Backend

### JavaScript API Client
Include the API client in your HTML files:

```html
<script src="path-to-api-client.js"></script>
```

Usage example:
```javascript
// Create API instance
const api = new AppointmentProAPI();

// Create appointment
const result = await api.createAppointment({
    service_type: 'School/College',
    client_name: 'John Doe',
    client_email: 'john@example.com',
    client_phone: '123-456-7890',
    appointment_date: '2025-12-20',
    appointment_time: '14:00',
    purpose: 'Enrollment'
});

if (result.success) {
    console.log('Appointment created:', result.data.appointment_number);
} else {
    console.error('Error:', result.error);
}
```

See `backend/frontend_integration.py` for complete API client code.

## Configuration

### Business Hours
Default: 9 AM - 5 PM, 30-minute slots
Edit in `backend/config.py`:
```python
APP_SETTINGS = {
    'business_hours_start': 9,
    'business_hours_end': 17,
    'slot_duration': 30  # minutes
}
```

### Notification Settings
- **Simulation Mode (Default):** Shows notifications as browser alerts
- **Email:** Configure SMTP in `.env` file
- **SMS:** Configure Twilio in `.env` file

## Deployment

### Docker Deployment
Coming soon - Docker setup files

### Heroku Deployment
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Add Firebase credentials
heroku config:set FIREBASE_PROJECT_ID=your-project-id
heroku config:set FIREBASE_PRIVATE_KEY="your-private-key"
# ... set other env vars

# Deploy
git push heroku main
```

### AWS Deployment
Coming soon - AWS setup instructions

## Troubleshooting

### Issue: "Firebase credentials not found"
**Solution:** Ensure `firebase-key.json` is in the `backend/` folder and properly formatted.

### Issue: "CORS error when calling API from frontend"
**Solution:** 
- Ensure backend is running at `http://localhost:5000`
- Update `CORS_ORIGINS` in `backend/config.py` if using different port
- Check browser console for exact CORS error message

### Issue: "Appointments not saving to database"
**Solution:** 
- Verify Firebase Firestore is enabled in Firebase Console
- Check `.env` file has correct Firebase credentials
- Look for errors in Flask console

### Issue: "Emails/SMS not being sent"
**Solution:** 
- Check `USE_SIMULATION_MODE=True` in `.env` (alerts shown instead)
- For real emails: set `USE_SIMULATION_MODE=False` and configure SMTP in `.env`
- For real SMS: configure Twilio credentials in `.env`

## Development Tips

### Enable Debug Mode
```python
# In backend/config.py
DEBUG = True
```

### View Firestore Console
- Go to [Firebase Console](https://console.firebase.google.com/)
- Select your project → Firestore Database
- View real-time data updates

### Monitor API Requests
- Backend logs all requests to console and file
- Use browser Network tab (F12 → Network) to see requests/responses

### Hot Reload Flask
```bash
# Already enabled if FLASK_DEBUG=True
# Flask will automatically reload on code changes
```

## File Descriptions

### Frontend Files (HTML)
- `dashboeard.html` - Main landing dashboard with service grid
- `index.html` - Home page entry point
- `login.html` - Client authentication with signup/login
- `staff-login.html` - Staff authentication
- `staff-dashboard.html` - Staff appointment management dashboard
- `school.html`, `hospital.html`, `company.html`, `doctor.html`, `advocate.html`, `teacher.html`, `cafe.html`, `barber.html`, `bank.html` - Service-specific booking pages

### Backend Files (Python)
- `app.py` - Main Flask application with API endpoints
- `config.py` - Configuration, environment variables, constants
- `firebase_db.py` - Database wrapper for Firestore operations
- `notifications.py` - Email and SMS notification service

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review Flask console logs for error messages
3. Check browser Network tab for API response errors
4. Verify Firebase credentials are correct

## License

This project is provided as-is for educational and commercial use.

## Next Steps

1. ✅ Set up Firebase project
2. ✅ Configure `.env` file
3. ✅ Start Flask backend
4. ✅ Serve frontend files
5. ✅ Test API endpoints
6. ⏳ Integrate frontend to call API (see frontend_integration.py for JavaScript code)
7. ⏳ Configure real email/SMS (optional)
8. ⏳ Deploy to production

---

**Last Updated:** December 2024
**Version:** 1.0.0
