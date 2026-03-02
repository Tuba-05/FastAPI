import { useEffect, useRef, useState } from "react";

export default function Classroom() {
  const [count, setCount] = useState(0); // Track number of students in room
  const [toast, setToast] = useState(null);
  const [tapcount, settapcount] = useState(0); // Track number of times the button was tapped
  const [clicking, setClicking] = useState(false);
  const socketRef = useRef(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    console.log("Token for WebSocket:", token);
    const classCode = localStorage.getItem("class_code");
    if (!token) {
      alert("Not authenticated");
      return;
    }
    const ws = new WebSocket( `ws://127.0.0.1:8000/ws/classroom/${classCode}?token=${encodeURIComponent(token)}`);

    socketRef.current = ws;

    ws.onopen = () => console.log("Connected to classroom");

    ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === "count") {
        setCount(data.active_students);
        settapcount(data.total_taps);  // ✅ use server's global tap count
        showToast(`${data.tapped_by} tapped! 👆`);  // ✅ tap message
    }
    if (data.type === "event") {
        // setCount(data.active_students);
        showToast(data.message);  // ✅ join/leave message
        setCount(data.active_students ?? 0);       
        settapcount(data.total_taps ?? 0);              

    }
  };

    ws.onerror = (err) => console.error("WebSocket error:", err);
    ws.onclose = () => console.log("Disconnected from classroom");

    return () => ws.close();
  }, []);

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(null), 3000);
  };

  const submitExam = () => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      // Trigger press animation
      setClicking(true);
      setTimeout(() => setClicking(false), 150);
      settapcount(prev => prev + 1);  // ✅ increments on every press
      socketRef.current.send(JSON.stringify({ action: "count_students" }));
    }
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }

        body { background: #07080f; }

        .exam-root {
          min-height: 100vh;
          background: #07080f;
          display: flex; flex-direction: column;
          align-items: center; justify-content: center;
          font-family: 'DM Sans', sans-serif;
          position: relative; overflow: hidden;
          gap: 48px;
        }

        .blob {
          position: absolute;
          border-radius: 50%;
          pointer-events: none;
        }
        .blob1 {
          width: 500px; height: 500px;
          background: radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 70%);
          top: -120px; left: -100px;
        }
        .blob2 {
          width: 350px; height: 350px;
          background: radial-gradient(circle, rgba(236,72,153,0.07) 0%, transparent 70%);
          bottom: -60px; right: -60px;
        }
        .grid {
          position: absolute; inset: 0;
          background-image:
            linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);
          background-size: 44px 44px;
          pointer-events: none;
        }

        /* ── Header ── */
        .header {
          text-align: center; z-index: 1;
          animation: up 0.6s cubic-bezier(0.16,1,0.3,1) both;
        }
        .header h2 {
          font-family: 'Syne', sans-serif;
          font-size: 1rem; font-weight: 700;
          color: rgba(255, 255, 255, 0.76);
          letter-spacing: 0.15em; text-transform: uppercase;
          margin-bottom: 8px;
        }
        .live-badge {
          display: inline-flex; align-items: center; gap: 7px;
          background: rgba(99,102,241,0.12);
          border: 1px solid rgba(99,102,241,0.25);
          color: #959bd7;
          font-size: 0.72rem; font-weight: 500;
          letter-spacing: 0.1em; text-transform: uppercase;
          padding: 5px 13px; border-radius: 100px;
        }
        .live-dot {
          width: 6px; height: 6px;
          background: #818cf8; border-radius: 50%;
          animation: pulse 2s ease infinite;
        }

        /* ── Count display ── */
        .count-display {
          z-index: 1; text-align: center;
          animation: up 0.6s 0.1s cubic-bezier(0.16,1,0.3,1) both;
        }
        .count-label {
          color: rgba(255, 255, 255, 0.94);
          font-size: 0.78rem; font-weight: 500;
          letter-spacing: 0.12em; text-transform: uppercase;
          margin-bottom: 6px;
        }
        .count-number {
          font-family: 'Syne', sans-serif;
          font-size: 3.5rem; font-weight: 800;
          background: linear-gradient(135deg, #fff 40%, rgba(255,255,255,0.4));
          -webkit-background-clip: text; -webkit-text-fill-color: transparent;
          background-clip: text;
          line-height: 1;
          transition: transform 0.1s ease;
        }
        .count-number.bump {
          animation: bump 0.2s cubic-bezier(0.36,0.07,0.19,0.97);
        }
        @keyframes bump {
          0%   { transform: scale(1); }
          40%  { transform: scale(1.12); }
          100% { transform: scale(1); }
        }

        /* ── Counter Button ── */
        .counter-wrap {
          z-index: 1;
          animation: up 0.6s 0.2s cubic-bezier(0.16,1,0.3,1) both;
          display: flex; flex-direction: column;
          align-items: center; gap: 16px;
        }

        .counter-btn {
          width: 140px; height: 140px;
          border-radius: 50%;
          border: none; cursor: pointer;
          position: relative;
          transition: transform 0.1s ease;
          background: none;
          -webkit-tap-highlight-color: transparent;
          outline: none;
        }

        /* Outer ring */
        .counter-btn::before {
          content: '';
          position: absolute; inset: -6px;
          border-radius: 50%;
          border: 1px solid rgba(99, 101, 241, 0.94);
          transition: all 0.15s ease;
        }

        /* Button face */
        .btn-face {
          position: absolute; inset: 0;
          border-radius: 50%;
          background: linear-gradient(145deg, #fdfdfd, #8b8b95);
          box-shadow:
            0 8px 0 #a33086,
            0 12px 20px rgba(99,102,241,0.4),
            inset 0 1px 0 rgba(148, 82, 235, 0.96);
          display: flex; align-items: center; justify-content: center;
          transition: all 0.1s ease;
        }

        .btn-icon {
          font-size: 2.2rem;
          transition: transform 0.1s ease;
          user-select: none;
        }

        /* Pressed state */
        .counter-btn.pressed {
          transform: translateY(6px);
        }
        .counter-btn.pressed .btn-face {
          box-shadow:
            0 2px 0 #3730a3,
            0 4px 10px rgba(99,102,241,0.3),
            inset 0 1px 0 rgba(255,255,255,0.1);
        }
        .counter-btn.pressed::before {
          border-color: rgba(99,102,241,0.4);
          inset: -3px;
        }
        .counter-btn.pressed .btn-icon {
          transform: scale(0.9);
        }

        /* Hover */
        .counter-btn:not(.pressed):hover .btn-face {
          box-shadow:
            0 10px 0 #3730a3,
            0 16px 28px rgba(99,102,241,0.5),
            inset 0 1px 0 rgba(255,255,255,0.2);
        }
        .counter-btn:not(.pressed):hover::before {
          border-color: rgba(99,102,241,0.4);
          inset: -8px;
        }

        .btn-hint {
          color: rgba(255, 255, 255, 0.89);
          font-size: 0.75rem; letter-spacing: 0.06em;
          text-transform: uppercase;
        }

        /* ── Toast ── */
        .toast {
          position: fixed; bottom: 28px; right: 28px;
          background: rgba(255,255,255,0.07);
          border: 1px solid rgba(255,255,255,0.1);
          backdrop-filter: blur(16px);
          color: #fff;
          padding: 12px 20px;
          border-radius: 12px;
          font-size: 0.88rem;
          box-shadow: 0 8px 24px rgba(0,0,0,0.3);
          animation: toastin 0.3s cubic-bezier(0.16,1,0.3,1) both;
          max-width: 260px;
          z-index: 100;
        }
        @keyframes toastin {
          from { opacity: 0; transform: translateY(10px) scale(0.95); }
          to   { opacity: 1; transform: translateY(0) scale(1); }
        }

        @keyframes up {
          from { opacity: 0; transform: translateY(24px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
          0%,100% { opacity:1; transform:scale(1); }
          50%      { opacity:0.4; transform:scale(0.75); }
        }
      `}</style>

      <div className="exam-root">
        <div className="blob blob1" /><div className="blob blob2" /><div className="grid" />

        {/* Header */}
        <div className="header">
          <h2>Live Classroom</h2>
          <div className="live-badge">
            <span className="live-dot" /> Live Session
          </div>
        </div>

        {/* Count */}
        <div className="count-display">
          <div className="count-label">Students in room</div>
          <div className={`count-number`}>{count}</div>
        </div>

        {/* Counter Button */}
        <div className="counter-wrap">
          <button
            className={`counter-btn ${clicking ? "pressed" : ""}`}
            onClick={submitExam}
            onMouseDown={() => setClicking(true)}
            onMouseUp={() => setClicking(false)}
            onMouseLeave={() => setClicking(false)}
            onTouchStart={(e) => { e.preventDefault(); setClicking(true); }}   // ✅ preventDefault stops onClick from firing too
            onTouchEnd={(e) => { e.preventDefault(); setClicking(false); submitExam(); }}  // ✅ only fires once
          >
            <div className="btn-face">
              <span className="btn-icon">👥</span>
            </div>
          </button>
          <span className="btn-hint">Tap to count</span>
          <div className={`count-number ${clicking ? "bump" : ""}`}>{tapcount}</div>
        </div>

        {/* Toast */}
        {toast && <div className="toast">📢 {toast}</div>}
      </div>
    </>
  );
}

