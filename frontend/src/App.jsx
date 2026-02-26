import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Auth from './components/auth/auth.jsx';
import ExamRoom from './components/sockets/exam_room.jsx';
import VeriCode from './components/VeriCode/VeriCode.jsx';
import Classjoin from "./components/classroom/classentry.jsx";
import Createclassroom from "./components/classroom/createdclassroom.jsx";
// import TeacherRoom from './components/teacher_room/teacher_room.jsx';

function App() {

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Auth/>} ></Route>
          <Route path="Exam-Room" element={<ExamRoom />}></Route>
          <Route path="/VeriCode" element={<VeriCode/>}></Route>
          <Route path="/classjoin" element={<Classjoin/>}></Route>
          <Route path="/createclassroom" element={<Createclassroom/>}></Route>
        </Routes>
      </BrowserRouter>  
    </>
  );
}

export default App
