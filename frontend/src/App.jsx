import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Auth from './components/Auth/auth.jsx'
import ExamRoom from './components/exam_room/exam_room.jsx'
import TeacherRoom from './components/teacher_room/teacher_room.jsx'
function App() {

  return (
    <>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Auth/>} ></Route>
        <Route path="Exam-Room" element={<ExamRoom />}></Route>
      </Routes>
    </BrowserRouter>  
    </>
  )
}

export default App
