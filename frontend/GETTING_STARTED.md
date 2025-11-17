# 🚀 Getting Started with Quantum Health Frontend

Welcome! This guide will get you up and running in **5 minutes**.

## 📋 Before You Start

Make sure you have:
- ✅ **Node.js 18+** installed ([Download here](https://nodejs.org/))
- ✅ **npm** (comes with Node.js)
- ✅ **Backend API** running on port 8000

Check your versions:
```bash
node --version  # Should be v18 or higher
npm --version   # Should be v9 or higher
```

---

## 🎯 Quick Setup (3 steps)

### Step 1: Install Dependencies

```bash
cd frontend-complete
npm install
```

This will install all required packages (~2 minutes).

### Step 2: Configure Environment

```bash
cp .env.example .env
```

The default configuration works out of the box! No changes needed unless your backend runs on a different port.

### Step 3: Start the App

```bash
npm run dev
```

That's it! Your app is now running at **http://localhost:3000** 🎉

---

## 🧪 Test It Out

### 1. Open the App

Visit [http://localhost:3000](http://localhost:3000)

You should see the home page with:
- Hero section
- 3 feature cards (Security, AI, Real-time)
- Patient Portal button
- Doctor Dashboard button

### 2. Test Patient Flow

Click **"Patient Portal"** and fill out:

```
Personal Info:
- Age: 45
- Gender: Male

Medical Info:
- Chief Complaint: "Frequent urination and increased thirst"
- Symptoms: "Excessive thirst, frequent urination, feeling tired"
- Duration: "2 weeks"
- Medical History: "Hypertension, Family history of diabetes"
- Medications: "Lisinopril 10mg"
- Allergies: "None"

Lab Results:
- Glucose: 180
- HbA1c: 7.5
- Blood Pressure: 140/90
- BMI: 28.5
```

Click **"Submit Securely"** and save your appointment ID!

### 3. Test Doctor Flow

Click **"Doctor Dashboard"** and:
1. See your appointment in the list
2. Click on it to view patient data
3. Add notes: "Patient counseled on lifestyle modifications"
4. Click **"Analyze with AI & Approve"**
5. Wait 5-10 seconds for AI analysis
6. ✅ Success!

---

## 📁 Project Structure

Here's what you got:

```
frontend-complete/
│
├── 📄 README.md               ← Project overview
├── 📄 GETTING_STARTED.md      ← This file!
├── 📄 package.json            ← Dependencies
├── 📄 vite.config.js          ← Build config
├── 📄 tailwind.config.js      ← Styling config
├── 📄 setup.sh                ← Automated setup script
│
├── 📁 src/
│   ├── 📁 pages/              ← 4 main pages
│   │   ├── Home.jsx           → Landing page
│   │   ├── PatientPortal.jsx  → Patient intake
│   │   ├── PatientResult.jsx  → View results
│   │   └── DoctorDashboard.jsx → Doctor interface
│   │
│   ├── 📁 services/
│   │   └── api.js             → Backend API calls
│   │
│   ├── App.jsx                → Router setup
│   ├── main.jsx               → Entry point
│   └── index.css              → Global styles
│
├── 📁 public/
│   └── logo.svg               → App logo
│
├── 📁 docs/                   ← Documentation
│   ├── QUICK_START.md
│   ├── DEMO_FLOW.md
│   └── SETUP_GUIDE.md
│
└── 📁 .vscode/                ← VS Code settings
    ├── settings.json
    └── extensions.json
```

---

## 🛠️ Useful Commands

```bash
# Development
npm run dev          # Start dev server (port 3000)
npm run build        # Build for production
npm run preview      # Preview production build

# Code Quality
npm run lint         # Check for code issues

# Utilities
./setup.sh           # Automated setup script
```

---

## 🔗 API Endpoints

Your frontend connects to these backend endpoints:

### Patient
- `POST /api/v1/patient/submit-intake` - Submit medical data
- `GET /api/v1/patient/result/{id}` - Get results

### Doctor
- `GET /api/v1/doctor/appointments` - List appointments
- `GET /api/v1/doctor/record/{id}` - Get patient data
- `POST /api/v1/doctor/record/{id}/analyze-and-approve` - AI analysis

---

## 🐛 Troubleshooting

### "npm: command not found"

Install Node.js from [nodejs.org](https://nodejs.org/)

### "Port 3000 already in use"

```bash
# Kill the process
lsof -ti:3000 | xargs kill -9

# Or change port in vite.config.js
server: {
  port: 3001  // Change this
}
```

### "Cannot connect to backend"

Make sure your backend is running:
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy", ...}
```

### "Module not found" errors

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Tailwind styles not working

```bash
# Restart dev server
npm run dev
```

---

## 📚 Learn More

Check out these docs for more details:

- **README.md** - Project overview and features
- **docs/QUICK_START.md** - 5-minute setup guide
- **docs/DEMO_FLOW.md** - Step-by-step demo walkthrough
- **docs/SETUP_GUIDE.md** - Complete integration guide

---

## 🎨 Customization

### Change Colors

Edit `tailwind.config.js`:

```js
colors: {
  primary: {
    500: '#your-color',  // Change this
  }
}
```

### Add New Pages

1. Create file in `src/pages/YourPage.jsx`
2. Add route in `src/App.jsx`:
```jsx
<Route path="/your-path" element={<YourPage />} />
```

### Modify API URL

Edit `.env`:
```env
VITE_API_URL=http://your-backend-url:port
```

---

## 🚢 Deployment

### Build for Production

```bash
npm run build
```

Creates optimized files in `dist/` folder.

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Deploy to Netlify

1. Push to GitHub
2. Connect repo on [netlify.com](https://netlify.com)
3. Set build command: `npm run build`
4. Set output directory: `dist`

---

## ✅ Checklist

Before your hackathon demo:

- [ ] Frontend runs without errors
- [ ] Backend is connected (port 8000)
- [ ] Patient can submit data
- [ ] Doctor can view appointments
- [ ] AI analysis works
- [ ] Tested complete flow
- [ ] Prepared demo script

---

## 🎉 You're All Set!

Your frontend is ready for the hackathon. Just:

1. ✅ Run `npm install`
2. ✅ Run `npm run dev`
3. ✅ Test patient & doctor flows
4. ✅ Practice your demo

**Good luck with your presentation! 🚀**

---

## 🆘 Need Help?

- Check **docs/** folder for detailed guides
- Review code comments in source files
- Test with sample data in **docs/DEMO_FLOW.md**

---

*Built with ❤️ for your hackathon success*
