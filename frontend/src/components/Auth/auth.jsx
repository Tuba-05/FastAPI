import React, { useState } from 'react'; // for formData inputs
import "./auth.css";
import { useNavigate } from "react-router-dom"; // to connect HmPg
// importing react-icons
import { HiOutlineMail } from "react-icons/hi";
import { RiLockPasswordLine } from "react-icons/ri";
import { FaUserAlt } from "react-icons/fa";

const auth = () => {
  // assigning navigate function to a variavle
  const navigate = useNavigate();
  const Newpassword = localStorage.getItem("Newpassword") || "false";

  // using usestate for switching b/w login/signup and changing formData respectively.
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: '',
    admin_key: '',
  });
  // function updates form state whenever data is typed in an input field, e -> event obj
  const handleInputChange = (e) => {
    setFormData({
      ...formData, //copies all the existing key–value pairs from formData into the new object
      [e.target.name]: e.target.value
    });
  };
  // when SignUp/ Login buttom clicked
  // -----------------------------------------------------------------------------
  // async → tells JS this function will use asynchronous code. 
  // await → pauses only inside the async function until the Promise resolves.
  // So other code keeps running in the meantime.
  // -----------------------------------------------------------------------------
  const handleSubmit = async () => {
  // for login/ signup part if no external error  
  try {
    if (isLogin) {
      // login
      if (formData.email && formData.password) {
        const response = await fetch("http://127.0.0.1:8000/online-exams/users/login/",// connection for login function of flask bkend
          {
          method: "POST", //sends data in the request body, which is hidden from the URL, making it more secure.
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password,
            admin_secret_key: formData.admin_key,
            ChangePassword: Newpassword
          })
        });
        const data = await response.json();
        if (data.success) {
          // save user info in localStorage for session persistence later used in watchlist page
          localStorage.setItem("username", data.username)
          localStorage.setItem("userEmail", data.email); // user email 
          localStorage.setItem("access_token", data.access_token)
          alert(data.message); // login sucessful
          navigate("/Exam-Room"); // navigate to HmPg
        } else {
          alert(data.message); // login not sucessful
        }
      } 
      else {
        alert("Please fill all fields."); // when any i/p field is empty
      }
    } 
    else {
      // signup
      if (formData.username && formData.email && formData.password) {
        const response = await fetch("http://127.0.0.1:8000/online-exams/users/register/", // connection for signup function of flask bkend
          {
          method: "POST", //sends data in the request body, which is hidden from the URL, making it more secure.
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: formData.username,
            email: formData.email,
            password: formData.password,
            admin_secret_key: formData.admin_key
          })
        });
        const data = await response.json();
        if (data.success) {
          // save user info in localStorage for session persistence later used in watchlist page
          localStorage.setItem("userEmail", data.user.email); // user email 
          alert(data.message); // signup sucessful
          navigate("/"); // navigate to HmPg
        } 
        else {
          alert(data.message); // signup sucessful
        }
      } 
      else {
        alert("Please fill all fields."); // when any i/p field is empty
      }
    }
    } 
    //If something goes wrong inside try block (like network failure,  invalid response, 
    // or coding bug),the code jumps here. The actual error info is stored in error
    // User cant see it only alert(), msg
    catch (error) {
      console.error("Error:", error);
      alert("Something went wrong. Please try again.");
    }
  };

  // function switches b/w login/ signup form
  const switchMode = () => {
    setIsLogin(!isLogin);
    setFormData({
      email: '',
      password: '',
      username: '', 
      admin_key: '',
    });
  };

  // Verification code trigger on clicking forgot password
  const trigger_verif_code = () =>{
    if (formData.email){
      localStorage.setItem("userEmail", formData.email)
      alert("Verification code has sent to your email");
      navigate("/VeriCode"); // navigate to code verification pg
    }
    else{
      alert("Plz fill email first");
    }
    }
  
  return (
    <>
      <div className="auth-page">
        {/* Background with blur overlay */}
        <div className="background-overlay"></div>
        
        <div className="auth-container">
          {/* Glass effect card */}
          <div className="glass-card">
            
            {/* Header */}
            <div className="card-header">
              <h1 className="auth-title">
                {isLogin ? 'Welcome Back' : 'Create Account'}
              </h1>
              <p className="auth-subtitle">
                {/* Conditional rendering */}
                {isLogin 
                  ? 'Sign in to access your investment portfolio' 
                  : 'Join thousands of successful investors'
                }
              </p>
            </div>

            {/* Form */}
            <div className="auth-form">      
              {/* Signup specific fields */}
              {!isLogin && (
                  <div className="input-group ">
                    <label htmlFor="Name"><FaUserAlt /> Userame</label>
                    <input
                      type="text"
                      id="username"
                      name="username"
                      value={formData.username}
                      onChange={handleInputChange} // function copies data {key:value}
                      className="glass-input"
                      placeholder="Enter username"
                    />
                  </div>  
              )}

              {/* Email */}
              <div className="input-group">
                
                <label htmlFor="email"><HiOutlineMail /> Email Address</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange} // function copies data {key:value}
                  className="glass-input"
                  placeholder="Enter email"
                />
              </div>

              {/* Password */}
              <div className="input-group">
                <label htmlFor="password"><RiLockPasswordLine /> Password</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange} // function copies data {key:value}
                  className="glass-input"
                  placeholder="Enter password"
                />
              </div>
              
              {/* Admin key */}
              <div className="input-group">
                <label htmlFor="admin_key"><RiLockPasswordLine /> Admin Key</label>
                <input
                  type="password"
                  id="admin_key"
                  name="admin_key"
                  value={formData.admin_key}
                  onChange={handleInputChange} // function copies data {key:value}
                  className="glass-input"
                  placeholder="Enter admin key"
                />
              </div>
              
              {/* Forgot Password Link (login only) */}
              {isLogin && (
                <div className="forgot-password">
                  <a href="#" className="forgot-link" onClick={trigger_verif_code}>Forgot your password?</a>
                </div>
              )}

              {/* Submit Button */}
              <button type="button" 
              onClick={handleSubmit} // function take data send to backend for verification then further process
              className="glass-button primary">
                {/* Conditional rendering */}
                {isLogin ? 'Sign In' : 'Create Account'} 
              </button>
            </div>

            {/* Switch between Login/Signup */}
            <div className="auth-switch">
              <p>
                {/* Conditional rendering */}
                {isLogin ? "Don't have an account? " : "Already have an account? "}
                <button 
                  type="button" 
                  onClick={switchMode} // function switch b/w login/ signup
                  className="switch-button">
                    {/* Conditional rendering */}
                  {isLogin ? 'Sign Up' : 'Sign In'}
                </button>
              </p>
            </div>

          </div> 
        </div>
      </div>
    </>
  );
};
export default auth;