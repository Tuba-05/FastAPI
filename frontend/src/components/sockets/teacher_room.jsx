import { useEffect, useState } from "react";

export default function TeacherDashboard() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/exam/42");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "count") {
        setCount(data.active_students);
      }
    };
  }, []);

  return (
    <div>
      <h1>Teacher Dashboard</h1>
      <h2>Live Students in Exam: {count}</h2>
    </div>
  );
}
