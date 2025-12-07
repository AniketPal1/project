# Quick Start Guide - 5 Minutes to Run

Get AppointmentPro running in 5 simple steps!

## Prerequisites
- Python 3.8+ installed (from python.org)
- Firebase account (free at firebase.google.com)
- ~10 minutes of time

## Step 1: Download Firebase Credentials (2 minutes)

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" → name it "AppointmentPro" → Create
3. Click "Build" → "Firestore Database" → Create Database
4. Choose "Start in test mode" → Select location → Create
5. Click "Build" → "Authentication" → Get Started
6. Click "Email/Password" → Enable → Save
7. Click Settings (gear icon) → "Service Accounts" tab
8. Click "Generate New Private Key" (downloads a JSON file)
9. Rename it to `firebase-key.json`
10. Move it to the `backend/` folder in your project

**Done! You have your Firebase credentials.**

## Step 2: Create Configuration File (1 minute)

1. In the `backend/` folder, find `.env.example`
2. Make a copy and rename it to `.env`
3. Open `.env` with a text editor
4. Open `firebase-key.json` with text editor
5. Copy the values:
   ```
   FIREBASE_PROJECT_ID: Copy from "project_id" in JSON
   FIREBASE_PRIVATE_KEY_ID: Copy from "private_key_id" in JSON
   FIREBASE_PRIVATE_KEY: Copy from "private_key" in JSON (with quotes)
   FIREBASE_CLIENT_EMAIL: Copy from "client_email" in JSON
   FIREBASE_CLIENT_ID: Copy from "client_id" in JSON
   ```

**Done! Configuration is ready.**

## Step 3: Install Backend (1 minute)

Open PowerShell or Command Prompt and run:

```powershell
cd C:\Users\anike\OneDrive\Desktop\project\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Done! Dependencies are installed.**

## Step 4: Start Backend (1 minute)

Still in PowerShell, run:

```powershell
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

**Backend is running! Keep this terminal open.**

## Step 5: Start Frontend (Open new terminal)

Open a NEW PowerShell/Command Prompt window:

```powershell
cd C:\Users\anike\OneDrive\Desktop\project\frontend
python -m http.server 8000
```

You should see:
```
Serving HTTP on 0.0.0.0 port 8000
```

**Frontend is running! Keep this terminal open.**

## Access the App

Open your browser to: **http://localhost:8000**

🎉 **Your app is running!**

## What to Try

### 1. Test the API
Open a browser to: `http://localhost:5000/api/health`

You should see:
```json
{"success": true, "message": "Backend is running"}
```

### 2. Sign Up as Client
- Click "Log In" on the dashboard
- Click "Sign Up" tab
- Fill in details
- Click "Sign Up"

### 3. Book an Appointment
- Select a service (School, Hospital, etc.)
- Fill in appointment details
- Select date and time
- Click "Book Appointment"
- You'll see your appointment number

### 4. Login as Staff
- Go back to dashboard
- Click "Staff Login" (in settings or footer)
- Sign up as staff with role "Admin"
- View all appointments in the dashboard

## Troubleshooting

### "Port 5000 already in use"
```powershell
# Change port in backend
python app.py --port 5001
# Then update frontend to call http://localhost:5001
```

### "Firebase credentials not found"
- Check `firebase-key.json` is in `backend/` folder
- Check `.env` file has all Firebase values
- Restart Flask backend

### "ModuleNotFoundError: No module named 'flask'"
```powershell
# Make sure venv is activated
venv\Scripts\activate
# Then reinstall
pip install -r requirements.txt
```

### "CORS error in browser console"
- Check backend is running at `http://localhost:5000`
- Check frontend is running at `http://localhost:8000`
- Clear browser cache (Ctrl+Shift+Delete)

## File Locations Recap

```
C:\Users\anike\OneDrive\Desktop\project\
├── README.md (full documentation)
├── FIREBASE_SETUP.md (detailed Firebase guide)
├── frontend/
│   ├── index.html (open in browser)
│   ├── login.html
│   ├── dashboeard.html
│   └── ... (9 service pages)
└── backend/
    ├── app.py (run this)
    ├── firebase-key.json (download from Firebase)
    ├── .env (create from .env.example)
    ├── .env.example
    ├── requirements.txt (pip install)
    ├── config.py
    ├── firebase_db.py
    └── notifications.py
```

## Next Steps

- **Frontend Integration:** Update frontend pages to call Flask API (see backend/frontend_integration.py for JavaScript code)
- **Real Email/SMS:** Configure SMTP and Twilio in `.env` file
- **Production Deployment:** See README.md for Heroku/AWS setup
- **More Features:** See README.md for full API documentation

## Still Having Issues?

1. Check the main **README.md** file for detailed documentation
2. Review **FIREBASE_SETUP.md** for Firebase-specific help
3. Check browser console (F12) for JavaScript errors
4. Check Flask console for backend errors
5. Check that ports 5000 and 8000 are not blocked by firewall

---

**You're all set! Enjoy AppointmentPro! 🎉**

Questions? Check README.md for full documentation.
