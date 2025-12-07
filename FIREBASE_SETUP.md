# Firebase Setup Guide

This guide will walk you through setting up Firebase Firestore and Authentication for the AppointmentPro system.

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project"
3. Enter project name (e.g., "AppointmentPro")
4. Accept terms and click "Create project"
5. Wait for project creation to complete (2-3 minutes)

## Step 2: Enable Firestore Database

1. In Firebase Console, click on "Build" in the sidebar
2. Click "Firestore Database"
3. Click "Create Database"
4. Select "Start in test mode" (for development)
   - **Note:** This allows anyone to read/write data. Switch to production rules before deploying.
5. Select your preferred location
6. Click "Create"

Test mode Firestore rules (for development):
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

For production, use these rules:
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /appointments/{document=**} {
      allow read, write: if request.auth != null;
    }
    match /clients/{document=**} {
      allow read, write: if request.auth.uid == resource.data.user_id || request.auth.token.claims.role == 'admin';
    }
    match /staff/{document=**} {
      allow read, write: if request.auth.token.claims.role == 'admin' || request.auth.token.claims.role == 'manager';
    }
  }
}
```

## Step 3: Enable Authentication

1. In Firebase Console, click "Build" → "Authentication"
2. Click "Get Started"
3. Click on "Email/Password" provider
4. Toggle "Enable" and click "Save"
5. (Optional) Add more providers: Phone, Google, Facebook, etc.

## Step 4: Get Service Account Key

1. Go to "Project Settings" (gear icon in top-right)
2. Click "Service Accounts" tab
3. Make sure "Firebase Admin SDK" is selected
4. Click "Generate New Private Key"
5. A JSON file will download named something like `ProjectName-xxxxx.json`
6. Rename it to `firebase-key.json`
7. Move it to the `backend/` folder in your project

This file contains your Firebase credentials and should be **kept secret** - never commit it to version control.

## Step 5: Configure Environment Variables

1. In `backend/` folder, copy `.env.example` to `.env`
2. Open `firebase-key.json` with a text editor
3. Copy the values into `.env`:

From `firebase-key.json`:
```json
{
  "type": "service_account",
  "project_id": "appointmentpro-abc123",
  "private_key_id": "key-id-here",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQI...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-abc@appointmentpro-abc123.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  ...
}
```

Fill in `.env`:
```env
FIREBASE_TYPE=service_account
FIREBASE_PROJECT_ID=appointmentpro-abc123
FIREBASE_PRIVATE_KEY_ID=key-id-here
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQI...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-abc@appointmentpro-abc123.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=123456789
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
```

## Step 6: Test Firebase Connection

1. Open terminal in `backend/` folder
2. Run: `python app.py`
3. Open browser to: `http://localhost:5000/api/health`
4. Should see: `{"success": true, "message": "Backend is running"}`

If you see Firebase errors, check:
- `firebase-key.json` is in `backend/` folder
- `.env` file has correct values
- Firestore Database is created and running
- Python requirements are installed: `pip install -r requirements.txt`

## Step 7: Create Firestore Collections (Optional)

The app will automatically create collections when first appointment is made, but you can pre-create them:

1. In Firebase Console, go to Firestore Database
2. Click "Start Collection"
3. Create these collections (leave empty, app will add documents):
   - `appointments`
   - `clients`
   - `staff`

## Step 8: Security Considerations

### For Development (Test Mode):
- Keep test mode rules (allow read/write)
- Use `.gitignore` to exclude firebase-key.json:
  ```
  backend/firebase-key.json
  backend/.env
  backend/venv/
  ```

### For Production:
1. Update Firestore rules (see Step 2 above)
2. Generate new service account key for production
3. Set strong Flask SECRET_KEY in `.env`
4. Use environment-specific Firebase projects
5. Enable Firebase Authentication email verification
6. Set up CORS origins in Flask config

## Firestore Database Schema

### Collections Created:

#### 1. `appointments`
```
appointments/{appointmentId}
├── appointment_number: string (APP-YYYYMMDD-XXXX)
├── service_type: string (School/College, Hospital, etc.)
├── client_uid: string (Firebase user ID)
├── client_name: string
├── client_email: string
├── client_phone: string
├── appointment_date: date (YYYY-MM-DD)
├── appointment_time: string (HH:MM)
├── purpose: string
├── status: string (Pending, Confirmed, Completed, Cancelled)
├── notes: string
├── created_at: timestamp
└── updated_at: timestamp
```

#### 2. `clients`
```
clients/{clientId}
├── user_id: string (Firebase UID)
├── email: string
├── name: string
├── phone: string
├── created_at: timestamp
├── last_login: timestamp
└── appointments: array of appointment IDs
```

#### 3. `staff`
```
staff/{staffId}
├── user_id: string (Firebase UID)
├── email: string
├── name: string
├── phone: string
├── role: string (admin, manager, staff)
├── created_at: timestamp
└── last_login: timestamp
```

## Troubleshooting Firebase

### Issue: "Failed to initialize Firebase"
- Check `firebase-key.json` exists in `backend/` folder
- Verify JSON is valid (use JSONLint.com)
- Check `.env` has `FIREBASE_PROJECT_ID` set correctly

### Issue: "Permission denied" when writing to Firestore
- Check Firestore is in test mode (for development)
- Verify Firestore rules allow read/write
- Check user is authenticated via Firebase Auth

### Issue: "Collection not found"
- Firestore doesn't pre-create collections
- Collections are created when first document is added
- You can manually create them in Console (see Step 7)

### Issue: "Invalid service account"
- Download fresh service account key from Firebase Console
- Delete old `firebase-key.json`
- Save new key with correct name
- Update `.env` with new credentials

## Firebase Console Tips

- **Firestore Data:** View all documents in Firestore Database tab
- **Authentication:** View users in Authentication tab
- **Logs:** View errors in Cloud Functions logs (if using)
- **Metrics:** Monitor usage in Usage and Quota section
- **Settings:** Update security rules in Firestore → Rules tab

## Next Steps

1. ✅ Create Firebase project
2. ✅ Enable Firestore and Authentication
3. ✅ Download service account key
4. ✅ Configure .env file
5. ✅ Test Flask backend
6. Start making API calls from frontend

For more details, see the main README.md file.
