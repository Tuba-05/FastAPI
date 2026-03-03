import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {getWorkingBaseURL} from "../UrlFetch/UrlFetch.jsx";

/* ── Inline icons (no extra deps needed) ── */
const IconUser = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
  </svg>
);
const IconMail = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
  </svg>
);
const IconLock = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
  </svg>
);
const IconKey = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6"/><path d="m15.5 7.5 3 3L22 7l-3-3"/>
  </svg>
);
const IconEye = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
  </svg>
);
const IconEyeOff = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
    <line x1="1" y1="1" x2="23" y2="23"/>
  </svg>
);
const IconArrow = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>
  </svg>
);

/* ── Styles ── */
const styles = `
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

  *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

  :root {
    --p1: #110e20;
    --p2: #463183;
    --p3: #8270bf;
    --p4: #b58bfa; 
    --p5: #4a3c80; 
    --p6: #ede9fe;

    --bg0: #07050f;
    --bg1: #0d0920;
    --bg2: #130d30;
    --bg3: #1a1040;

    --glass:        rgba(255, 255, 255, 0.72);
    --glass-border: rgba(34, 89, 196, 0.14);
    --glass-shine:  rgba(255, 255, 255, 0.95);
    --glass-blur:   32px;

    --txt1: #20077c;
    --txt2: rgb(7, 7, 9);
    --txt3: rgba(4, 4, 4, 0.95);

    --inp-bg:    rgba(124, 92, 232, 0.09);
    --inp-bd:    rgba(167, 139, 250, 0.25);
    --inp-focus: rgba(124, 92, 232, 0.18);

    --glow1: rgba(91, 50, 214, 0.55);
    --glow2: rgba(124, 92, 232, 0.35);

    --ease: cubic-bezier(0.4, 0, 0.2, 1);
    --spring: cubic-bezier(0.22, 1, 0.36, 1);
  }

  .auth-root {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    font-family: 'Outfit', sans-serif;
    background: var(--bg0);
  }

  /* ── Background ── */
  .auth-bg {
    position: absolute;
    inset: 0;
    background:
      radial-gradient(ellipse 90% 70% at 10% -10%, rgba(59, 31, 168, 0.5) 0%, transparent 55%),
      radial-gradient(ellipse 70% 60% at 90% 110%,  rgba(91, 50, 214, 0.4) 0%, transparent 55%),
      radial-gradient(ellipse 50% 40% at 50%  50%,  rgba(124, 92, 232, 0.12) 0%, transparent 65%),
      linear-gradient(175deg, var(--bg0) 0%, var(--bg1) 30%, var(--bg2) 60%, var(--bg3) 100%);
  }

  /* Grid lines */
  .auth-bg::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(rgba(167, 139, 250, 0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(167, 139, 250, 0.04) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 80%);
  }

  /* Floating orbs */
  .orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(90px);
    pointer-events: none;
    animation: orbDrift 14s var(--ease) infinite alternate;
  }
  .orb-1 {
    width: 600px; height: 600px;
    top: -200px; left: -150px;
    background: radial-gradient(circle, rgba(59,31,168,0.4) 0%, transparent 65%);
  }
  .orb-2 {
    width: 500px; height: 500px;
    bottom: -150px; right: -120px;
    background: radial-gradient(circle, rgba(91,50,214,0.35) 0%, transparent 65%);
    animation-delay: -7s;
    animation-direction: alternate-reverse;
  }
  .orb-3 {
    width: 300px; height: 300px;
    top: 50%; left: 55%;
    background: radial-gradient(circle, rgba(124,92,232,0.2) 0%, transparent 65%);
    animation-delay: -3.5s;
  }

  @keyframes orbDrift {
    from { transform: translate(0, 0) scale(1); }
    to   { transform: translate(25px, 18px) scale(1.06); }
  }

  /* Grain */
  .auth-grain {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    opacity: 0.028;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    background-size: 200px 200px;
  }

  /* ── Card ── */
  .auth-wrap {
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: 460px;
    padding: 20px;
  }

  .auth-card {
    background: var(--glass);
    backdrop-filter: blur(var(--glass-blur)) saturate(180%) brightness(1.05);
    -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(180%) brightness(1.05);
    border: 1px solid var(--glass-border);
    border-top-color: var(--glass-shine);
    border-radius: 26px;
    box-shadow:
      0 0 0 1px rgba(86, 164, 213, 0.75),
      0 35px 80px rgba(171, 168, 183, 0.9),
      0 12px 35px rgba(106, 101, 101, 0.5),
      inset 0 1px 0 rgba(196,181,253,0.14),
      inset 0 -1px 0 rgba(59,31,168,0.1);
    padding: 48px 44px 44px;
    position: relative;
    overflow: hidden;
    animation: cardIn 0.7s var(--spring) both;
  }

  /* Top shimmer line */
  .auth-card::before {
    content: '';
    position: absolute;
    top: 0; left: 8%; right: 8%;
    height: 1px;
    background: linear-gradient(90deg,
      transparent,
      rgba(167,139,250,0.6),
      rgba(196,181,253,1),
      rgba(167,139,250,0.6),
      transparent
    );
  }

  /* Purple radial bloom */
  .auth-card::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 26px;
    background:
      radial-gradient(ellipse 75% 35% at 50% 0%,   rgba(124,92,232,0.13) 0%, transparent 70%),
      radial-gradient(ellipse 55% 25% at 50% 100%,  rgba(59,31,168,0.08) 0%, transparent 70%);
    pointer-events: none;
  }

  @keyframes cardIn {
    from { opacity: 0; transform: translateY(32px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0)    scale(1); }
  }

  /* ── Logo mark ── */
  .logo-mark {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 24px;
  }
  .logo-icon {
    width: 42px; height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--p1) 0%, var(--p3) 100%);
    box-shadow: 0 4px 20px var(--glow1), inset 0 1px 0 rgba(255,255,255,0.2);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    position: relative;
    flex-shrink: 0;
  }
  .logo-icon::after {
    content: '';
    position: absolute;
    inset: 1px;
    border-radius: 10px;
    background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent 60%);
  }
  .logo-text {
    font-size: 15px;
    font-weight: 700;
    color: var(--txt1);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
  }
  .logo-text span {
    color: var(--p4);
  }

  /* ── Header ── */
  .auth-header { margin-bottom: 32px; }

  .auth-title {
    font-size: 28px;
    font-weight: 800;
    color: var(--txt1);
    letter-spacing: -0.6px;
    line-height: 1.15;
    margin-bottom: 8px;
  }
  .auth-title em {
    font-style: normal;
    background: linear-gradient(90deg, var(--p4), var(--p5));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .auth-subtitle {
    font-size: 14px;
    color: var(--txt2);
    line-height: 1.6;
    font-weight: 400;
  }

  /* ── Form ── */
  .auth-form { display: flex; flex-direction: column; gap: 16px; }

  .field { display: flex; flex-direction: column; gap: 7px; animation: fieldIn 0.5s var(--spring) both; }
  .field:nth-child(1) { animation-delay: 0.08s; }
  .field:nth-child(2) { animation-delay: 0.14s; }
  .field:nth-child(3) { animation-delay: 0.20s; }
  .field:nth-child(4) { animation-delay: 0.26s; }

  @keyframes fieldIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .field-label {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11.5px;
    font-weight: 600;
    color: var(--txt3);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding-left: 2px;
  }
  .field-label svg { color: var(--p4); flex-shrink: 0; }

  .input-wrap {
    position: relative;
    display: flex;
    align-items: center;
  }

  .auth-input {
    width: 100%;
    padding: 14px 18px;
    padding-right: 44px;
    border: 1px solid var(--inp-bd);
    border-radius: 14px;
    background: var(--inp-bg);
    backdrop-filter: blur(8px);
    font-family: 'Outfit', sans-serif;
    font-size: 15px;
    font-weight: 400;
    color: var(--txt1);
    outline: none;
    transition: border-color 0.25s var(--ease), background 0.25s var(--ease), box-shadow 0.25s var(--ease), transform 0.25s var(--ease);
  }
  .auth-input::placeholder { color: var(--txt3); }
  .auth-input:focus {
    border-color: var(--p3);
    background: var(--inp-focus);
    box-shadow: 0 0 0 3px rgba(124,92,232,0.25), 0 2px 12px rgba(0,0,0,0.3);
    transform: translateY(-1px);
  }

  /* Eye toggle */
  .eye-btn {
    position: absolute;
    right: 14px;
    background: none;
    border: none;
    cursor: pointer;
    color: var(--txt3);
    display: flex;
    align-items: center;
    padding: 4px;
    border-radius: 6px;
    transition: color 0.2s;
  }
  .eye-btn:hover { color: var(--p4); }

  /* ── Forgot ── */
  .forgot-row {
    display: flex;
    justify-content: flex-end;
    margin-top: -4px;
  }
  .forgot-link {
    font-size: 13px;
    font-weight: 500;
    color: var(--txt3);
    text-decoration: none;
    transition: color 0.2s;
    background: none;
    border: none;
    cursor: pointer;
    font-family: 'Outfit', sans-serif;
  }
  .forgot-link:hover { color: var(--p5); }

  /* ── Submit ── */
  .submit-btn {
    position: relative;
    margin-top: 6px;
    padding: 15px 24px;
    border: none;
    border-radius: 14px;
    cursor: pointer;
    font-family: 'Outfit', sans-serif;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.02em;
    color: #fff;
    background: linear-gradient(135deg, var(--p1) 0%, var(--p2) 45%, var(--p3) 100%);
    box-shadow:
      0 4px 24px var(--glow1),
      0 2px 8px rgba(0,0,0,0.4),
      inset 0 1px 0 rgba(255,255,255,0.18);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    overflow: hidden;
    transition: transform 0.25s var(--ease), box-shadow 0.25s var(--ease), filter 0.25s;
    animation: fieldIn 0.5s 0.34s var(--spring) both;
  }

  /* Shimmer sweep */
  .submit-btn::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(105deg, transparent 35%, rgba(255,255,255,0.18) 50%, transparent 65%);
    transform: translateX(-100%);
    transition: transform 0.55s var(--ease);
  }
  .submit-btn:hover::before { transform: translateX(100%); }
  .submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 36px var(--glow1), 0 4px 16px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.22);
    filter: brightness(1.1);
  }
  .submit-btn:active {
    transform: translateY(0);
    filter: brightness(0.96);
    box-shadow: 0 2px 12px var(--glow2), 0 1px 4px rgba(0,0,0,0.3);
  }

  .btn-arrow {
    display: flex;
    align-items: center;
    transition: transform 0.25s var(--ease);
  }
  .submit-btn:hover .btn-arrow { transform: translateX(3px); }

  /* ── Divider ── */
  .auth-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 4px 0;
    color: var(--txt3);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }
  .auth-divider::before,
  .auth-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.15), transparent);
  }

  /* ── Switch ── */
  .auth-switch {
    text-align: center;
    margin-top: 22px;
    padding-top: 20px;
    border-top: 1px solid rgba(167,139,250,0.1);
    animation: fieldIn 0.5s 0.4s var(--spring) both;
  }
  .auth-switch p { font-size: 14px; color: var(--txt2); }

  .switch-btn {
    background: none;
    border: none;
    font-family: 'Outfit', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: var(--p4);
    cursor: pointer;
    margin-left: 4px;
    transition: color 0.2s, text-shadow 0.2s;
    text-decoration: none;
  }
  .switch-btn:hover {
    color: var(--p5);
    text-shadow: 0 0 14px rgba(167,139,250,0.6);
  }

  /* ── Badge ── */
  .mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 10px;
    border-radius: 20px;
    background: rgba(124,92,232,0.15);
    border: 1px solid rgba(167,139,250,0.2);
    font-size: 11px;
    font-weight: 600;
    color: var(--p4);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 10px;
    font-family: 'JetBrains Mono', monospace;
  }
  .mode-badge::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--p4);
    box-shadow: 0 0 6px var(--p3);
    animation: pulse 2s infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
  }

  /* ── Loading spinner ── */
  .spinner {
    width: 16px; height: 16px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    flex-shrink: 0;
  }
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  .submit-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none !important;
    filter: none !important;
  }

  /* ── Responsive ── */
  @media (max-width: 480px) {
    .auth-wrap { padding: 16px; }
    .auth-card  { padding: 36px 28px 32px; border-radius: 20px; }
    .auth-title { font-size: 24px; }
    .auth-input { font-size: 16px; }
  }`

/* ── Component ── */
export default function AuthPage() {
  const [BASE_URL, setBASE_URL] = useState(null);
  useEffect(() => {
    getWorkingBaseURL().then(url => {
      setBASE_URL(url);
    });
  }, []);

  console.log("API Base URLs:", BASE_URL);
  const [isLogin, setIsLogin] = useState(true);
  const [showPw,  setShowPw]  = useState(false);
  const [showKey, setShowKey] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({ username: "", email: "", password: "", admin_key: "" });

  const navigate    = useNavigate();
  const Newpassword = localStorage.getItem("Newpassword") || "false";

  const handleInputChange = (e) =>
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSubmit = async () => {
    try {
      setLoading(true);
      if (isLogin) {
        if (!formData.email || !formData.password) { alert("Please fill all fields."); return; }
        const response = await fetch(`${BASE_URL}/online-exams/users/login/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password,
            admin_secret_key: formData.admin_key,
            ChangePassword: Newpassword,
          }),
        });
        const data = await response.json();
        if (data.success) {
          localStorage.setItem("username",     data.data.username);
          localStorage.setItem("userEmail",    data.data.email);
          localStorage.setItem("access_token", data.data.access_token);
          alert(data.message);
          navigate("/classentry");
        } else {
          alert(data.message);
        }
      } else {
        if (!formData.username || !formData.email || !formData.password) { alert("Please fill all fields."); return; }
        const response = await fetch(`${BASE_URL}/online-exams/users/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: formData.username,
            email: formData.email,
            password: formData.password,
            admin_secret_key: formData.admin_key,
          }),
        });
        const data = await response.json();
        if (data.success) {
          alert(data?.message);
          setIsLogin(true);
          setFormData(prev => ({ ...prev, password: "", admin_key: "" }));
        } else {
          alert(data.message);
        }
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const switchMode = () => {
    setIsLogin(p => !p);
    setFormData({ username: "", email: "", password: "", admin_key: "" });
  };

  const trigger_verif_code = (e) => {
    e.preventDefault();
    if (formData.email) {
      localStorage.setItem("userEmail", formData.email);
      navigate("/VeriCode");
    } else {
      alert("Please fill email first.");
    }
  };

  return (
    <>
      <style>{styles}</style>

      <div className="auth-root">
        {/* Background layers */}
        <div className="auth-bg" />
        <div className="orb orb-1" />
        <div className="orb orb-2" />
        <div className="orb orb-3" />
        <div className="auth-grain" />

        <div className="auth-wrap">
          <div className="auth-card">

            {/* Logo */}
            <div className="logo-mark">
              <div className="logo-icon">🎓</div>
              <span className="logo-text">GradeGate<span> X </span></span>
            </div>

            {/* Header */}
            <div className="auth-header">
              <div className="mode-badge">
                {isLogin ? "Sign In" : "New Account"}
              </div>
              <h1 className="auth-title">
                {isLogin ? (<>Welcome <em>back</em></>) : (<>Start OR Join <em>classroom</em> today</>)}
              </h1>
              <p className="auth-subtitle">
                {isLogin
                  ? <>Where learning gets serious.<br />Join your classes and ace those exams!</>
                  : <>Create your account and step into a world of seamless learning and exam success.<br />Let's get you started!</>}
              </p>
            </div>

            {/* Form */}
            <div className="auth-form">

              {/* Username — signup only */}
              {!isLogin && (
                <div className="field">
                  <label className="field-label"><IconUser /> Username</label>
                  <div className="input-wrap">
                    <input
                      type="text" id="username" name="username"
                      value={formData.username} onChange={handleInputChange}
                      className="auth-input" placeholder="Choose a username"
                    />
                  </div>
                </div>
              )}

              {/* Email */}
              <div className="field">
                <label className="field-label"><IconMail /> Email Address</label>
                <div className="input-wrap">
                  <input
                    type="email" id="email" name="email"
                    value={formData.email} onChange={handleInputChange}
                    className="auth-input" placeholder="you@example.com"
                  />
                </div>
              </div>

              {/* Password */}
              <div className="field">
                <label className="field-label"><IconLock /> Password</label>
                <div className="input-wrap">
                  <input
                    type={showPw ? "text" : "password"} id="password" name="password"
                    value={formData.password} onChange={handleInputChange}
                    className="auth-input" placeholder="Enter your password"
                  />
                  <button className="eye-btn" type="button" onClick={() => setShowPw(p => !p)}>
                    {showPw ? <IconEyeOff /> : <IconEye />}
                  </button>
                </div>
              </div>

              {/* Admin key */}
              <div className="field">
                <label className="field-label"><IconKey /> Admin Key</label>
                <div className="input-wrap">
                  <input
                    type={showKey ? "text" : "password"} id="admin_key" name="admin_key"
                    value={formData.admin_key} onChange={handleInputChange}
                    className="auth-input" placeholder="Enter admin key"
                  />
                  <button className="eye-btn" type="button" onClick={() => setShowKey(p => !p)}>
                    {showKey ? <IconEyeOff /> : <IconEye />}
                  </button>
                </div>
              </div>

              {/* Forgot password */}
              {isLogin && (
                <div className="forgot-row">
                  <a href="#" className="forgot-link" onClick={trigger_verif_code}>
                    Forgot password?
                  </a>
                </div>
              )}

              {/* Submit */}
              <button type="button" className="submit-btn" onClick={handleSubmit} disabled={loading}>
                {loading
                  ? <><div className="spinner" /> {isLogin ? "Signing In…" : "Creating Account…"}</>
                  : <>{isLogin ? "Sign In" : "Create Account"}<span className="btn-arrow"><IconArrow /></span></>
                }
              </button>
            </div>

            {/* Switch mode */}
            <div className="auth-switch">
              <p>
                {isLogin ? "Don't have an account?" : "Already have an account?"}
                <button type="button" className="switch-btn" onClick={switchMode}>
                  {isLogin ? "Sign Up" : "Sign In"}
                </button>
              </p>
            </div>

          </div>
        </div>
      </div>
    </>
  );
}

