import { useEffect, useState } from "react";

export default function StudentExam() {
  const [count, setCount] = useState(0);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/exam/42");
    
    // receives response from backend
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "count") {
        setCount(data.active_students);
      }
    };

    setSocket(ws);

    // when user closes the page
    return () => ws.close(); 
  }, []);

  // submit exam
  const submitExam = () => {
    socket.send(JSON.stringify({
      action: "submit_exam",
      student: "Tuba"
    }));
  };

  return (
    <div>
      <h2>Live Exam Room</h2>
      <h3>Students currently taking exam: {count}</h3>
      <button onClick={submitExam}>Submit Exam</button>
    </div>
  );
}
