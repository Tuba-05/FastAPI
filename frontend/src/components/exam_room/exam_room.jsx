import { useEffect, useState } from "react";

export default function StudentExam() {
  const [count, setCount] = useState(0);
  const [socket, setSocket] = useState(null);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const username = localStorage.getItem("acess_token")
    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/exam/42?token=${token}`);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "count") {
        setCount(data.active_students);
      }

      if (data.type === "event") {
        showToast(data.message);
      }
    };

    setSocket(ws);
    return () => ws.close();
  }, []);

  const showToast = (msg) => {
    setToast(msg);

    setTimeout(() => {
      setToast(null);
    }, 3000); // disappears after 3 seconds
  };

  const submitExam = () => {
    socket.send(JSON.stringify({
      action: "submit_exam",
      student: "Tuba"
    }));
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h2>Live Exam Room</h2>
      <h3>Students currently taking exam: {count}</h3>

      <button onClick={submitExam}>Submit Exam</button>

      {/* Toast Message */}
      {toast && (
        <div style={{
          position: "fixed",
          bottom: "20px",
          right: "20px",
          backgroundColor: "#333",
          color: "#fff",
          padding: "12px 20px",
          borderRadius: "6px",
          transition: "opacity 0.5s"
        }}>
          {toast}
        </div>
      )}
    </div>
  );
}

