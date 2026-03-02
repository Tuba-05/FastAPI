import { useState } from "react";
import { useNavigate } from "react-router-dom";

const ClassroomEntry = () => {
  const [mode, setMode]           = useState(null);
  const [joincode, setCode]       = useState("");
  const [className, setClassName] = useState("");
  const [classCode, setClassCode] = useState("");
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState("");
  const [success, setSuccess]     = useState(false);
  const navigate  = useNavigate();
  const token_id  = localStorage.getItem("access_token");

  // ── Called only when user clicks submit ──
  const handleAction = async () => {
    // Validation first — stop if empty
    if (mode === "join"   && !joincode.trim())   return setError("Please enter a class code");
    if (mode === "create" && !className.trim())  return setError("Please enter a class name");
    if (mode === "create" && !classCode.trim())  return setError("Please enter a class code");

    setError("");
    setLoading(true);

    try {
      if (mode === "join") {
        // API call — only fires when user submits join form
        const res  = await fetch("http://localhost:8000/online-exams/classroom/join", {
          method:  "POST",
          headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token_id}` },
          body:    JSON.stringify({ code: joincode, token_id: token_id }),
        });
        const data = await res.json();
        if (data.success) {
          localStorage.setItem("class_code", joincode); // Store class code for later use in classroom
          localStorage.setItem("classroom_id", data.data.classroom_id); // Store classroom ID for later use
          localStorage.setItem("token_id", data.data.token_id); // Store token ID for later use
          setSuccess(true);
          navigate("/classjoin");
        } else {
          setError(data.message || "Failed to join the classroom.");
        }

      } else if (mode === "create") {
        // API call — only fires when user submits create form
        const res  = await fetch("http://localhost:8000/online-exams/classroom/create", {
          method:  "POST",
          headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token_id}` },
          body:    JSON.stringify({ name: className, code: classCode , token_id: token_id}),
        });
        const data = await res.json();
        if (data.success) {
          localStorage.setItem("class_code", classCode); // Store class code for later use in classroom
          localStorage.setItem("classroom_id", data.data.classroom_id); // Store classroom ID for later use
          localStorage.setItem("token_id", data.data.token_id); // Store token ID for later use
          setSuccess(true);
          setTimeout(() => reset(), 2000); // Optional: auto-reset after showing success message
          setMode("join");
          navigate("/classentry");
        } else {
          setError(data.message || "Failed to create the classroom.");
        }
      }
    } catch (err) {
      console.error(err);
      setError("An error occurred. Please try again.");
    } finally {
      setLoading(false); // always runs — clears spinner whether success or fail
    }
  };

  // ── Resets everything back to the mode selection screen ──
  const reset = () => {
    setMode(null); setCode(""); setClassName(""); setClassCode("");
    setError(""); setSuccess(false); setLoading(false);
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }

        .root {
          min-height: 100vh;
          background: #07080f;
          display: flex;
          align-items: center;
          justify-content: center;
          font-family: 'DM Sans', sans-serif;
          position: relative;
          overflow: hidden;
        }

        .blob1 {
          position: absolute;
          width: 500px; height: 500px;
          background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
          top: -100px; left: -80px;
          pointer-events: none;
        }
        .blob2 {
          position: absolute;
          width: 400px; height: 400px;
          background: radial-gradient(circle, rgba(236,72,153,0.08) 0%, transparent 70%);
          bottom: -80px; right: -60px;
          pointer-events: none;
        }
        .grid {
          position: absolute; inset: 0;
          background-image:
            linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);
          background-size: 44px 44px;
          pointer-events: none;
        }

        .card {
          position: relative; z-index: 1;
          background: rgb(200, 199, 203);
          border: 1px solid rgba(46, 155, 180, 0.89);
          border-radius: 28px;
          padding: 52px 44px;
          width: 100%; max-width: 500px;
          backdrop-filter: blur(24px);
          box-shadow: 0 40px 80px rgba(128, 123, 123, 0.58), inset 0 1px 0 rgba(255,255,255,0.05);
          animation: up 0.55s cubic-bezier(0.16,1,0.3,1) both;
        }

        @keyframes up {
          from { opacity: 0; transform: translateY(28px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadein {
          from { opacity: 0; transform: translateY(12px); }
          to   { opacity: 1; transform: translateY(0); }
        }

        .animated { animation: fadein 0.4s cubic-bezier(0.16,1,0.3,1) both; }

        .logo {
          display: flex; align-items: center; gap: 10px;
          margin-bottom: 36px;
        }
        .logo-icon {
          width: 36px; height: 36px;
          background: linear-gradient(135deg, #121214, #8b5cf6);
          border-radius: 10px;
          display: flex; align-items: center; justify-content: center;
          font-size: 1rem;
        }
        .logo-name {
          font-family: 'Syne', sans-serif;
          font-weight: 700; font-size: 1rem;
          color: rgba(89, 40, 174, 0.85);
          letter-spacing: 0.02em;
        }

        .heading {
          font-family: 'Syne', sans-serif;
          font-size: 2.1rem; font-weight: 800;
          color: #100e0e; line-height: 1.15;
          margin-bottom: 10px;
        }
        .heading span {
          background: linear-gradient(135deg, #3345e6, #ec4899);
          -webkit-background-clip: text; -webkit-text-fill-color: transparent;
          background-clip: text;
        }
        .sub {
          color: rgba(0, 0, 0, 0.81);
          font-size: 0.9rem; font-weight: 500;
          line-height: 1.6; margin-bottom: 36px;
        }

        .modes {
          display: grid; grid-template-columns: 1fr 1fr;
          gap: 14px; margin-bottom: 0;
        }
        .mode-card {
          background: rgba(100, 90, 101, 0.15);
          border: 1px solid rgba(138, 91, 167, 0.18);
          border-radius: 18px;
          padding: 24px 20px;
          cursor: pointer;
          transition: all 0.2s ease;
          text-align: left;
        }
        .mode-card:hover {
          border-color: rgba(99,102,241,0.35);
          background: rgba(99,102,241,0.07);
          transform: translateY(-2px);
        }
        .mode-icon { font-size: 1.6rem; margin-bottom: 12px; display: block; }
        .mode-title {
          font-family: 'Syne', sans-serif;
          font-size: 1rem; font-weight: 700;
          color: #7a57d5; margin-bottom: 4px;
        }
        .mode-desc { font-size: 0.78rem; color: rgba(15, 13, 13, 0.59); line-height: 1.5; font-weight: 500; }
        .mode-arrow { display: inline-block; margin-top: 14px; color: rgba(161, 99, 241, 0.74); font-size: 0.8rem; font-weight: 600; letter-spacing: 0.04em; }

        .back-btn {
          display: inline-flex; align-items: center; gap: 6px;
          background: none; border: none;
          color: rgba(23, 21, 21, 0.78);
          font-family: 'DM Sans', sans-serif;
          font-size: 0.82rem; cursor: pointer; font-weight: 500;
          padding: 0; margin-bottom: 28px;
          transition: color 0.2s;
        }
        .back-btn:hover { color: rgba(80, 9, 118, 0.7); }

        .mode-badge {
    
          display: inline-flex; align-items: center; gap: 9px;
          padding: 3px 9px; border-radius: 100px;
          font-size: 0.72rem; font-weight: 600;
          letter-spacing: 0.08em; text-transform: uppercase;
          margin-bottom: 20px;
        }
        .mode-badge.join  { background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.25); color: #818cf8; }
        .mode-badge.create { background: rgba(236,72,153,0.12); border: 1px solid rgba(236,72,153,0.25); color: #f472b6; }
        .badge-dot { width: 6px; height: 6px; border-radius: 50%; animation: pulse 2s ease infinite; }
        .join .badge-dot { background: #7330b7; }
        .create .badge-dot { background: #f472b6; }
        @keyframes pulse {
          0%,100% { opacity:1; transform:scale(1); }
          50%      { opacity:0.4; transform:scale(0.75); }
        }

        .field { margin-bottom: 14px; }
        .field label {
          display: block; color: rgba(17, 11, 11, 0.93);
          font-size: 0.85rem; font-weight: 600;
          letter-spacing: 0.07em; text-transform: uppercase;
          margin-bottom: 8px;
        }
        .field-wrap { position: relative; }
        .field-icon { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); font-size: 0.95rem; pointer-events: none; }
        .field input {
          width: 100%;
          background: rgba(43, 6, 54, 0.05);
          border: 1px solid rgba(255,255,255,0.09);
          border-radius: 13px;
          padding: 14px 16px 14px 44px;
          color: #231616; font-size: 0.95rem;
          font-family: 'DM Sans', sans-serif;
          font-weight: 400; outline: none; transition: all 0.2s;
        }
        .field input::placeholder { color: rgba(25, 11, 11, 0.86); }
        .field input:focus {
          border-color: rgba(86, 47, 176, 0.86);
          background: rgba(99,102,241,0.06);
          box-shadow: 0 0 0 3px rgba(99,102,241,0.08);
        }
        .create-mode .field input:focus {
          border-color: rgba(236,72,153,0.45);
          background: rgba(236,72,153,0.05);
          box-shadow: 0 0 0 3px rgba(236,72,153,0.07);
        }

        .error {
          display: flex; align-items: center; gap: 6px;
          color: #f87171; font-size: 0.8rem;
          margin-bottom: 14px; animation: shake 0.3s ease;
        }
        @keyframes shake {
          0%,100% { transform: translateX(0); }
          25%      { transform: translateX(-5px); }
          75%      { transform: translateX(5px); }
        }

        .submit-btn {
          width: 100%; padding: 15px; border: none; border-radius: 13px;
          font-family: 'Syne', sans-serif; font-size: 0.95rem; font-weight: 700;
          letter-spacing: 0.03em; color: #1b1818; cursor: pointer;
          position: relative; overflow: hidden; transition: all 0.2s; margin-top: 6px;
        }
        .submit-btn.join-btn   { background: linear-gradient(135deg, #151752, #8b5cf6); }
        .submit-btn.create-btn { background: linear-gradient(135deg, #db2777, #ec4899); }
        .submit-btn::before { content: ''; position: absolute; inset: 0; background: linear-gradient(135deg, rgba(255,255,255,0.12), transparent); opacity: 0; transition: opacity 0.2s; }
        .submit-btn:hover::before { opacity: 1; }
        .submit-btn:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(99,102,241,0.3); }
        .submit-btn.create-btn:hover { box-shadow: 0 12px 28px rgba(236,72,153,0.3); }
        .submit-btn:active { transform: translateY(0); }
        .submit-btn:disabled { opacity: 0.55; cursor: not-allowed; transform: none; }

        .spinner {
          display: inline-block; width: 14px; height: 14px;
          border: 2px solid rgba(255,255,255,0.3); border-top-color: #000;
          border-radius: 50%; animation: spin 0.7s linear infinite;
          vertical-align: middle; margin-right: 8px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        .success { text-align: center; animation: fadein 0.4s cubic-bezier(0.16,1,0.3,1) both; }
        .success-ring {
          width: 76px; height: 76px; border-radius: 50%;
          display: flex; align-items: center; justify-content: center;
          font-size: 2rem; margin: 0 auto 20px;
        }
        .success-ring.join   { background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.25); }
        .success-ring.create { background: rgba(236,72,153,0.12); border: 1px solid rgba(236,72,153,0.25); }
        .success-title { font-family: 'Syne', sans-serif; font-size: 1.55rem; font-weight: 800; color: #18063a; margin-bottom: 8px; }
        .success-sub { color: rgba(255,255,255,0.35); font-size: 0.88rem; margin-bottom: 28px; }
        .reset-btn {
          background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
          border-radius: 12px; padding: 11px 24px; color: rgba(255,255,255,0.5);
          font-family: 'DM Sans', sans-serif; font-size: 0.85rem; cursor: pointer; transition: all 0.2s;
        }
        .reset-btn:hover { color: #130226; border-color: rgba(255,255,255,0.18); }
      `}</style>

      <div className="root">
        <div className="blob1" /><div className="blob2" /><div className="grid" />

        <div className="card">
          <div className="logo">
            <div className="logo-icon">🎓</div>
            <span className="logo-name">GradeGate<span> X </span></span>
          </div>

          {/* ── Success ── */}
          {success && (
            <div className="success">
              <div className={`success-ring ${mode}`}>
                {mode === "join" ? "🎉" : "✨"}
              </div>
              <div className="success-title">
                {mode === "join" ? "You're in!" : "Class Created!"}
              </div>
              <div className="success-sub">
                {mode === "join"
                  ? "You've successfully joined the classroom."
                  : `"${className}" is ready for students.`}
              </div>
              <button className="reset-btn" onClick={reset}>← Go back</button>
            </div>
          )}

          {/* ── Selection screen ── */}
          {!mode && !success && (
            <div className="animated">
              <h1 className="heading">What would you<br />like to <span>do?</span></h1>
              <p className="sub">Choose an option below to get started with your classroom.</p>
              <div className="modes">
                <div className="mode-card" onClick={() => setMode("join")}>
                  <span className="mode-icon">🚪</span>
                  <div className="mode-title">Join Class</div>
                  <div className="mode-desc">Enter a code shared by your instructor to join.</div>
                  <span className="mode-arrow">Enter →</span>
                </div>
                <div className="mode-card" onClick={() => setMode("create")}>
                  <span className="mode-icon">🏫</span>
                  <div className="mode-title">Create Class</div>
                  <div className="mode-desc">Set up a new classroom and invite your students.</div>
                  <span className="mode-arrow">Create →</span>
                </div>
              </div>
            </div>
          )}

          {/* ── Join form ── */}
          {mode === "join" && !success && (
            <div className="animated">
              <button className="back-btn" onClick={reset}>← Back</button>
              <div className="mode-badge join"><span className="badge-dot" />Student</div>
              <h1 className="heading">Join a <span>Classroom</span></h1>
              <p className="sub">Enter the code your instructor shared with you.</p>
              <div className="field">
                <label>Class Code</label>
                <div className="field-wrap">
                  <span className="field-icon">🔑</span>
                  <input
                    type="text" placeholder="e.g. ABC-1234"
                    value={joincode}
                    onChange={(e) => { setCode(e.target.value); setError(""); }}
                    onKeyDown={(e) => e.key === "Enter" && handleAction()}
                  />
                </div>
              </div>
              {error && <div className="error">⚠ {error}</div>}
              <button className="submit-btn join-btn" onClick={handleAction} disabled={loading}>
                {loading ? <><span className="spinner" />Joining...</> : "Join Classroom →"}
              </button>
            </div>
          )}

          {/* ── Create form ── */}
          {mode === "create" && !success && (
            <div className="animated create-mode">
              <button className="back-btn" onClick={reset}>← Back</button>
              <div className="mode-badge create"><span className="badge-dot" />Teacher</div>
              <h1 className="heading">Create a <span style={{background:"linear-gradient(135deg,#f472b6,#ec4899)", WebkitBackgroundClip:"text", WebkitTextFillColor:"transparent"}}>Classroom</span></h1>
              <p className="sub">Set up your classroom and share the code with students.</p>
              <div className="field">
                <label>Class Name</label>
                <div className="field-wrap">
                  <span className="field-icon">📚</span>
                  <input
                    type="text" placeholder="e.g. Mathematics Grade 10"
                    value={className}
                    onChange={(e) => { setClassName(e.target.value); setError(""); }}
                  />
                </div>
              </div>
              <div className="field">
                <label>Class Code</label>
                <div className="field-wrap">
                  <span className="field-icon">🔒</span>
                  <input
                    type="text" placeholder="e.g. MATH-2024"
                    value={classCode}
                    onChange={(e) => { setClassCode(e.target.value); setError(""); }}
                    onKeyDown={(e) => e.key === "Enter" && handleAction()}
                  />
                </div>
              </div>
              {error && <div className="error">⚠ {error}</div>}
              <button className="submit-btn create-btn" onClick={handleAction} disabled={loading}>
                {loading ? <><span className="spinner" />Creating...</> : "Create Classroom →"}
              </button>
            </div>
          )}

        </div>
      </div>
    </>
  );
};

export default ClassroomEntry;
