import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import PatientPortal from './pages/PatientPortal';
import PatientResult from './pages/PatientResult';
import CheckResults from './pages/CheckResults';
import DoctorDashboard from './pages/DoctorDashboard';
import DoctorRecordView from './pages/DoctorRecordView';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/patient" element={<PatientPortal />} />
        <Route path="/check-results" element={<CheckResults />} />
        <Route path="/patient/result/:appointmentId" element={<PatientResult />} />
        <Route path="/doctor" element={<DoctorDashboard />} />
        <Route path="/doctor/record/:appointmentId" element={<DoctorRecordView />} />
      </Routes>
    </Router>
  );
}

export default App;
