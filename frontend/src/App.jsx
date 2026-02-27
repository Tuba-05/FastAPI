import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AuthPage from './components/auth/auth.jsx';
import ExamRoom from './components/sockets/exam_room.jsx';
import VeriCode from './components/VeriCode/VeriCode.jsx';
import Classentry from "./components/classroom/classentry.jsx";
import Classroom from './components/sockets/class_room.jsx';

function App() {

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AuthPage/>} ></Route>
          <Route path="Exam-Room" element={<ExamRoom />}></Route>
          <Route path="/VeriCode" element={<VeriCode/>}></Route>
          <Route path="/classentry" element={<Classentry/>}></Route>
          <Route path="/classjoin" element={<Classroom/>}></Route>
        </Routes>
      </BrowserRouter>  
    </>
  );
}

export default App
