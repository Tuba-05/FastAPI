import React, { useState, useEffect, useCallback, useRef } from 'react';
import VCimg from '../../assets/vericode.png';
import { useNavigate } from 'react-router-dom';

const VeriCode = () => {
    const userEmail = localStorage.getItem('userEmail');
    const [veriCode, setVeriCode] = useState("");
    const [timeLeft, setTimeLeft] = useState(0); // ⏳ Timer state
    const timerRef = useRef(null);
    const navigate = useNavigate();

    // Function to start/reset the 60-second timer
    const startTimer = () => {
        setTimeLeft(60); 
    };

    useEffect(() => {
        if (timeLeft > 0) {
            timerRef.current = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
        } else {
            clearTimeout(timerRef.current);
        }
        return () => clearTimeout(timerRef.current); // Cleanup on unmount
    }, [timeLeft]);

    const generate_code = useCallback(() => {
        if (timeLeft > 0) return; // Prevent spamming if timer is active

        fetch('http://127.0.0.1:8000/online-exams/users/otps', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: userEmail })
        })
        .then(res => {
            if (res.ok) startTimer(); // Start timer only if request succeeds
            // alert("Verification code has sent to your email which is valid for 2 minutes");
        });
    }, [userEmail, timeLeft]);

    const handleSubmit = (e) => {
        e.preventDefault(); // ✅ Essential to prevent page reload
        fetch(`http://127.0.0.1:8000/users/update-password`, {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: userEmail, veriCode: veriCode })
        })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                alert(data.message);
                localStorage.setItem("Newpassword", "true");
                navigate("/");
            } else {
                alert(data.message);
            }   
        });
    };

    // Run once on load
    useEffect(() => {
        generate_code();
    }, []);

    return (
        <div style={{ height: 640, width: 1260, position:'fixed', fontfamily: 'Montserrat',
          /*m-l for not mixing with navbar, t&l for placing of DataGrid div*/
          marginLeft: "130px",top:'22px', padding:'10px', overflow: 'hidden',
          /*styling of DataGrid div*/
          border:'7px solid #1cb5abff', borderRadius:'19px', boxSizing:'border-box', 
          /* Glassmorphism effect */
          background: 'rgba(212, 94, 4, 0.15)',   // transparent white
          backdropFilter: 'blur(10px)',              // frosted glass blur
          WebkitBackdropFilter: 'blur(10px)',        // Safari support
          /* Shadow on all sides , r-l-b-t */
          boxShadow:'10px 0 15px rgba(62, 59, 59, 1),-10px 0 15px rgba(62, 60, 60, 1), 0 10px 15px rgba(0,0,0,0.25), 0 -10px 15px rgba(0,0,0,0.25)'    
          , flexWrap: 'wrap', display: 'flex',  justifyContent: 'center',
        }}
        >
            <form style={{ fontWeight: '600', fontSize:'35px',  padding: '20px', display: 'flex', 
            alignItems: 'center', justifyContent: 'center', flexDirection: 'column',
            gap: '15px' }}>
                <label htmlFor="veriCode">Enter Verification Code:</label>
                <input
                    type="text"
                    maxLength={6}
                    id="veriCode"
                    value={veriCode}
                    onChange={(e) => setVeriCode(e.target.value)}
                    placeholder="123456"
                    required
                    style={{ fontSize: '30px', borderRadius: '18px', border: '2px solid #cccccca5',
                             width: '200px', textAlign: 'center', padding: '9px', 
                            }} />
                
                {/* ⏳ Display the countdown */}
                <p style={{ fontSize: '16px', color: timeLeft > 0 ? 'red' : 'green' }}>
                    {timeLeft > 0 ? `Resend available in ${timeLeft}s` : "You can resend the code now"}
                </p>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    <button 
                        type="button"
                        onClick={generate_code}
                        disabled={timeLeft > 0} // 🚫 Disable while timer is running
                        style={{
                            fontSize: '19px',
                            border: '2px solid #e21313ff', 
                            borderRadius: '30px', 
                            width: '140px',
                            opacity: timeLeft > 0 ? 0.5 : 1,
                            cursor: timeLeft > 0 ? 'not-allowed' : 'pointer'
                        }}
                    >
                        Generate Code
                    </button>
                    <button 
                        onClick={handleSubmit}
                        style={{ fontSize: '19px', border: '2px solid #049d3cff', borderRadius: '30px', width: '70px' }}
                    >
                        Verify
                    </button>
                </div>
            </form>
            <div>
                <img src={VCimg} alt="" 
                style={{ width: '100%', height: '90vh'}} />
            </div>
        </div>
    );
};

export default VeriCode;
