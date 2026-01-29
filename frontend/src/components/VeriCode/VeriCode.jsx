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

        fetch('http://127.0.0.1:8000/online-exams/users/otp', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: userEmail })
        })
        .then(res => {
            if (res.ok) startTimer(); // Start timer only if request succeeds
        });
    }, [userEmail, timeLeft]);

    const handleSubmit = (e) => {
        e.preventDefault(); // ✅ Essential to prevent page reload
        fetch(`http://127.0.0.1:8000/users/password`, {
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
        <div style={{ /* your existing styles */ }}>
            <form style={{ /* your existing styles */ }}>
                <label htmlFor="veriCode">Enter Verification Code:</label>
                <input
                    type="text"
                    maxLength={6}
                    id="veriCode"
                    value={veriCode}
                    onChange={(e) => setVeriCode(e.target.value)}
                    placeholder="123456"
                    required
                />
                
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
                            border: '2.5px solid #e21313ff', 
                            borderRadius: '30px', 
                            width: '280px',
                            opacity: timeLeft > 0 ? 0.5 : 1,
                            cursor: timeLeft > 0 ? 'not-allowed' : 'pointer'
                        }}
                    >
                        Generate Code
                    </button>
                    <button 
                        onClick={handleSubmit}
                        style={{ border: '2.5px solid #049d3cff', borderRadius: '30px', width: '120px' }}
                    >
                        Verify
                    </button>
                </div>
            </form>
        </div>
    );
};

export default VeriCode;
