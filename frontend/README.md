# Quantum Health Frontend

Modern, minimalist React frontend for the Quantum-Secure Clinical AI platform.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📋 Prerequisites

- Node.js 18+ and npm
- Backend API running on port 8000

## 🎯 Features

### Patient Portal
- ✅ Medical intake form with validation
- ✅ Lab results input (optional)
- ✅ Mock encryption before submission
- ✅ Appointment ID generation
- ✅ Results viewing page

### Doctor Dashboard
- ✅ Appointment list with status
- ✅ Patient data decryption & review
- ✅ Medical history display
- ✅ Lab results visualization
- ✅ AI analysis integration (Gemini)
- ✅ Doctor notes input
- ✅ Approval workflow

### Design
- ✅ Modern minimalist UI
- ✅ Fully responsive (mobile-ready)
- ✅ Loading states & animations
- ✅ Error handling
- ✅ Tailwind CSS styling

## 📁 Project Structure

```
frontend-complete/
├── public/
│   └── logo.svg              # App logo
├── src/
│   ├── pages/
│   │   ├── Home.jsx          # Landing page
│   │   ├── PatientPortal.jsx # Patient intake form
│   │   ├── PatientResult.jsx # View results
│   │   └── DoctorDashboard.jsx # Doctor interface
│   ├── services/
│   │   └── api.js            # API integration
│   ├── components/           # Reusable components (future)
│   ├── utils/                # Utility functions (future)
│   ├── App.jsx               # Main app with routing
│   ├── main.jsx              # Entry point
│   └── index.css             # Global styles
├── docs/                     # Documentation
├── package.json              # Dependencies
├── vite.config.js            # Vite configuration
├── tailwind.config.js        # Tailwind configuration
└── README.md                 # This file
```

## 🔧 Available Scripts

```bash
# Development
npm run dev          # Start dev server (port 3000)

# Production
npm run build        # Build for production
npm run preview      # Preview production build

# Code Quality
npm run lint         # Run ESLint
```

## 🔗 API Integration

The frontend connects to these FastAPI endpoints:

### Patient APIs
- `POST /api/v1/patient/submit-intake` - Submit encrypted medical data
- `GET /api/v1/patient/result/{appointment_id}` - Get consultation results

### Doctor APIs
- `GET /api/v1/doctor/appointments?doctor_id={uuid}` - List appointments
- `GET /api/v1/doctor/record/{appointment_id}` - Get patient record
- `POST /api/v1/doctor/record/{appointment_id}/analyze-and-approve` - AI analysis

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

### Backend Requirements

Make sure your backend is:
- Running on port 8000
- CORS enabled for `http://localhost:3000`
- Using the correct API endpoints

## 🎨 Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.3 | UI framework |
| Vite | 5.3 | Build tool |
| Tailwind CSS | 3.4 | Styling |
| React Router | 6.26 | Navigation |
| Axios | 1.7 | HTTP client |
| Lucide React | 0.263 | Icons |

## 🧪 Testing the Application

### Test Patient Flow

1. Navigate to **Patient Portal**
2. Fill out the form with sample data:

```
Age: 45
Gender: Male
Chief Complaint: Frequent urination and increased thirst
Symptoms: Excessive thirst, frequent urination, fatigue
Duration: 2 weeks
Medical History: Hypertension, Family history of diabetes
Glucose: 180
HbA1c: 7.5
Blood Pressure: 140/90
```

3. Submit and save the appointment ID

### Test Doctor Flow

1. Navigate to **Doctor Dashboard**
2. Click on the appointment
3. Review patient data
4. Add notes
5. Click "Analyze with AI & Approve"
6. Wait for AI analysis (5-10 seconds)

## 🐛 Troubleshooting

### Port 3000 already in use

```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or change port in vite.config.js
```

### Cannot connect to backend

```bash
# Check backend is running
curl http://localhost:8000/health

# Should return: {"status": "healthy", ...}
```

### Styles not loading

```bash
# Clear cache and restart
rm -rf node_modules/.vite
npm run dev
```

### Dependencies not installing

```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🚢 Deployment

### Build for Production

```bash
npm run build
```

This creates a `dist/` folder with optimized files.

### Deploy to Vercel/Netlify

1. Connect your GitHub repository
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Add environment variable: `VITE_API_URL=https://your-backend-url.com`

## 🎯 Demo Mode

- No authentication required (hackathon demo)
- Uses Dr. Sarah Chen as default doctor
- Mock encryption for demonstration
- Sample doctor ID: `11111111-1111-1111-1111-111111111111`

## 📝 Code Quality

### ESLint

```bash
npm run lint
```

### Code Style

- Use functional components
- Use React hooks
- Keep components small and focused
- Comment complex logic
- Use meaningful variable names

## 🤝 Contributing

This is a hackathon project. For improvements:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

Built for hackathon demonstration purposes.

## 🙏 Acknowledgments

- **React Team** - UI framework
- **Vite** - Lightning-fast build tool
- **Tailwind Labs** - CSS framework
- **Lucide** - Beautiful icons

---

## 🎉 You're Ready!

Just run `npm install` and `npm run dev` to get started!

For detailed setup instructions, see the `docs/` folder.

**Good luck with your hackathon! 🚀**
