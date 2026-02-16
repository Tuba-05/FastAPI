import { useEffect, useRef, useState } from "react";

export default function StudentExam() {
  const [count, setCount] = useState(0);
  const [toast, setToast] = useState(null);
  const socketRef = useRef(null); // Holds the WebSocket connection

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
    navigate("/");
    }

    if (!token) {
      alert("Not authenticated");
      return;
    }
    // creating websocket
    const ws = new WebSocket(
      `ws://127.0.0.1:8000/ws/exam/42?token=${token}`
    );

    socketRef.current = ws; // Save socket

    ws.onopen = () => {
      console.log("Connected to exam room"); // when connection is successful
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data); // Every message from backend arrives here

      // updates live student count
      if (data.type === "count") {
        setCount(data.active_students);
      }

      // handles join/leave toast
      if (data.type === "event") {
        showToast(data.message);
      }

      // shows submission toast
      if (data.type === "submission") {
        showToast(data.message);
      }
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err); // error handling
    };

    ws.onclose = () => {
      console.log("Disconnected from exam room"); // On disconnect
    };

    return () => {
      ws.close(); // user leaves page→socket closes→backend detects disconnect
    };
  }, []);

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(null), 3000);
  };

  const submitExam = () => {
    // Prevents sending before connection is ready.
    if (
      socketRef.current &&
      socketRef.current.readyState === WebSocket.OPEN
    ) {
      socketRef.current.send(
        JSON.stringify({ action: "submit_exam" })
      );
    }
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h2>Live Exam Room</h2>
      <h3>Students currently taking exam: {count}</h3>

      <button onClick={submitExam}>Submit Exam</button>

      {toast && (
        <div
          style={{
            position: "fixed",
            bottom: "20px",
            right: "20px",
            backgroundColor: "#333",
            color: "#fff",
            padding: "12px 20px",
            borderRadius: "6px",
          }}
        >
          {toast}
        </div>
      )}
    </div>
  );
}
