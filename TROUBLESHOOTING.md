# Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: "ModuleNotFoundError: No module named 'flask'"

**Error:** When running `python app.py`
```
ModuleNotFoundError: No module named 'flask'
```

**Solutions:**
1. Make sure you're in the `backend` folder
2. Activate the virtual environment:
   ```powershell
   venv\Scripts\activate
   ```
   You should see `(venv)` at the start of your terminal prompt
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Try running again:
   ```powershell
   python app.py
   ```

---

### Issue 2: "FileNotFoundError: [Errno 2] No such file or directory: 'firebase-key.json'"

**Error:** When running backend
```
FileNotFoundError: [Errno 2] No such file or directory: 'firebase-key.json'
```

**Solutions:**
1. Check if `firebase-key.json` exists in `backend/` folder
2. If not, download it from Firebase:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Select your project
   - Settings → Service Accounts → Generate New Private Key
3. Save it as `firebase-key.json` exactly
4. Place it in the `backend/` folder
5. Restart Flask

**Alternative:** Run in demo mode without Firebase
- The app will show a message but continue running
- Use this for testing frontend only

---

### Issue 3: "Port 5000 is already in use"

**Error:**
```
Address already in use
```

**Solutions:**
Option A: Kill the process using port 5000
```powershell
# Find process using port 5000
Get-Process | Where-Object { $_.ProcessName -eq 'python' }

# Kill it (replace PID with actual process ID)
Stop-Process -Id <PID> -Force
```

Option B: Use a different port
```powershell
# In backend folder, edit app.py
# Change the last line from:
# app.run(debug=True, port=5000)
# To:
# app.run(debug=True, port=5001)

python app.py
```

Then update frontend to call `http://localhost:5001` instead of 5000

Option C: Wait for the port to be released
- Sometimes ports take a minute to release
- Try again after 1 minute

---

### Issue 4: "CORS error: Access-Control-Allow-Origin header missing"

**Error in browser console:**
```
Access to XMLHttpRequest at 'http://localhost:5000/api/...' 
from origin 'http://localhost:8000' has been blocked by CORS policy
```

**Solutions:**
1. Make sure Flask backend is running at `http://localhost:5000`
2. Make sure frontend is running at `http://localhost:8000`
3. Hard refresh browser (Ctrl+Shift+R) to clear cache
4. Check `backend/config.py` has correct CORS origins:
   ```python
   CORS_ORIGINS = [
       'http://localhost:3000',
       'http://localhost:8000',
       'http://127.0.0.1:8000',
       'http://127.0.0.1:5000',
   ]
   ```
5. If using different ports, add them to CORS_ORIGINS

---

### Issue 5: "Firebase project not found"

**Error:**
```
firebase_exceptions.NotFoundError: Project ... not found
```

**Solutions:**
1. Check `FIREBASE_PROJECT_ID` in `.env` is correct
   ```powershell
   # Open .env file and verify
   # Should match project ID from Firebase Console
   ```
2. Verify the project exists in [Firebase Console](https://console.firebase.google.com/)
3. Verify you're logged into the right Firebase account
4. Download a new `firebase-key.json` from the correct project
5. Update `.env` with values from the new key file

---

### Issue 6: "Cannot create user: Permission denied"

**Error:**
```
Permission PermissionError: User does not have permission...
```

**Solutions:**
1. Check Firestore rules are in test mode (for development)
   - Go to Firebase Console → Firestore Database → Rules
   - Should see: `allow read, write: if true;`
2. Check Authentication is enabled
   - Go to Firebase Console → Authentication → Make sure Email/Password is enabled
3. Check `.env` has correct FIREBASE_PRIVATE_KEY with newlines:
   ```env
   FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQI...\n-----END PRIVATE KEY-----\n"
   ```
4. Restart Flask backend

---

### Issue 7: "Appointments not saving to database"

**Error:** Appointment created locally but not in Firebase

**Solutions:**
1. Check Firebase Firestore Database is enabled
   - Go to Firebase Console → Build → Firestore Database
   - Should see a database created
2. Check `.env` has correct credentials
3. Check browser Network tab (F12 → Network):
   - Make sure POST request to `/api/appointments` returns 201 or 200
   - If error, check response body for details
4. Check Flask console for error messages
5. Check Firebase Firestore collections
   - Go to Firebase Console → Firestore Database
   - Should see `appointments` collection being created

---

### Issue 8: "Login not working"

**Error:** Can't log in even with correct credentials

**Solutions:**
1. Check user exists in Firebase Authentication
   - Go to Firebase Console → Authentication → Users
   - Should see your test user
2. Check `.env` has correct Firebase credentials
3. Clear browser localStorage:
   ```javascript
   // In browser console (F12)
   localStorage.clear()
   ```
4. Try signing up again with new email
5. Check Flask console for error messages
6. Check Network tab (F12 → Network) → Click login request
   - Look for response error details

---

### Issue 9: "Port 8000 already in use" (Frontend)

**Error:**
```
Address already in use
```

**Solutions:**
Option A: Kill the process
```powershell
Get-Process -Name python | Where-Object { $_.Id -eq <PID> } | Stop-Process
```

Option B: Use different port
```powershell
cd frontend
python -m http.server 8001
# Then open http://localhost:8001
```

Option C: Use VS Code Live Server extension
- Right-click `index.html` → "Open with Live Server"

---

### Issue 10: "JSON.parse: Unexpected token" in browser console

**Error:**
```
Uncaught SyntaxError: Unexpected token < in JSON at position 0
```

**Solutions:**
1. This usually means HTML response instead of JSON
2. Check API endpoint is correct in your frontend code
3. Check Flask backend is running
4. Verify endpoint exists in `app.py`
5. Check request method is correct (GET vs POST)
6. Check request headers include `Content-Type: application/json`

---

### Issue 11: "Appointment number already exists"

**Error:** Can't create appointment with generated number

**Solutions:**
1. This shouldn't happen - numbers are unique with UUID
2. Clear localStorage and try again:
   ```javascript
   localStorage.clear()
   location.reload()
   ```
3. Check backend logs for duplicate key error
4. If persistent, drop and recreate Firestore `appointments` collection

---

### Issue 12: "Email/SMS not being sent"

**Normal behavior in development:** Notifications appear as browser alerts

**To send real emails:**
1. Set `USE_SIMULATION_MODE=False` in `.env`
2. Configure SMTP in `.env`:
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_EMAIL=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```
3. For Gmail, use [App Passwords](https://myaccount.google.com/apppasswords)
4. Restart Flask

**To send real SMS:**
1. Set `USE_SIMULATION_MODE=False` in `.env`
2. Get Twilio account at [twilio.com](https://twilio.com)
3. Add to `.env`:
   ```env
   TWILIO_ACCOUNT_SID=your-account-sid
   TWILIO_AUTH_TOKEN=your-auth-token
   TWILIO_PHONE_NUMBER=+1234567890
   ```
4. Restart Flask

---

### Issue 13: "Cannot find module 'firebase_admin'"

**Error in Flask:**
```
ImportError: No module named 'firebase_admin'
```

**Solutions:**
1. Make sure virtual environment is activated
   ```powershell
   venv\Scripts\activate
   ```
2. Install dependencies
   ```powershell
   pip install -r requirements.txt
   ```
3. Verify firebase-admin is installed
   ```powershell
   pip show firebase-admin
   ```
4. If not listed, install it manually
   ```powershell
   pip install firebase-admin
   ```

---

### Issue 14: "Appointments not appearing in Staff Dashboard"

**Issue:** Staff logs in but sees no appointments

**Solutions:**
1. Check appointments are created and saved (see Issue 7)
2. Check staff user exists and is logged in
3. Clear browser localStorage:
   ```javascript
   localStorage.clear()
   ```
4. Check Firebase Firestore has `appointments` collection with data
5. Check staff dashboard code is querying Firebase correctly
6. Check browser Network tab for API errors

---

### Issue 15: "Time slots not showing"

**Issue:** Availability check returns empty slots

**Solutions:**
1. Check selected date is in the future
2. Check business hours in `backend/config.py`:
   ```python
   'business_hours_start': 9,
   'business_hours_end': 17,
   ```
3. Check slot duration is 30 minutes
4. Try a different date
5. Check Flask console for availability calculation errors

---

## Getting Help

1. **Check Flask Console:** Most errors are printed here
2. **Check Browser Console:** F12 → Console tab for JavaScript errors
3. **Check Network Tab:** F12 → Network to see API requests/responses
4. **Check Firebase Console:** View data and errors there
5. **Review README.md:** Full documentation available
6. **Review logs:** Flask creates logs in `backend/` folder

---

## Basic Debugging Steps

When something doesn't work:

1. **Check if servers are running:**
   ```powershell
   # Test backend
   curl http://localhost:5000/api/health
   
   # Test frontend
   # Open http://localhost:8000 in browser
   ```

2. **Check browser console for errors:**
   - Press F12 in browser
   - Click Console tab
   - Look for red error messages

3. **Check Flask console for errors:**
   - Look at the terminal running `python app.py`
   - Look for red error messages

4. **Check network requests:**
   - F12 → Network tab
   - Perform an action (login, create appointment)
   - Check request/response in Network tab

5. **Restart everything:**
   - Stop Flask (Ctrl+C)
   - Stop frontend server (Ctrl+C)
   - Start Flask again
   - Start frontend again
   - Try again

---

## Still Not Working?

1. Review **README.md** for complete documentation
2. Review **FIREBASE_SETUP.md** for Firebase-specific issues
3. Review **QUICK_START.md** for setup steps
4. Check that all files are in correct locations
5. Ensure Python 3.8+ is installed
6. Ensure all .env values are filled in correctly

---

**Last Updated:** December 2024
**Version:** 1.0.0
