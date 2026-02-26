import React from "react";

const Classjoin = () => {

    

    
    return (
        <>
        <div
            style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
                    height: "50vh", backgroundColor: "#f0f0f0",}} >

            <h1 style={{ fontSize: "2.5rem", marginBottom: "20px" }}>Join Class</h1>
            <div style={{ fontSize: "1.2rem", color: "#555", marginBottom: "30px" }}>
                Please enter the class code provided by your instructor to join the class.
            </div>
            <div style={{ display: "flex", gap: "10px" }}>
                <input
                    type="text"
                    placeholder="Enter Class Code"
                    style={{ padding: "10px", fontSize: "1rem", borderRadius: "5px", border: "1px solid #ccc" }}
                />
                <button
                    style={{ padding: "10px 20px", fontSize: "1rem", borderRadius: "5px", border: "none", backgroundColor: "#007bff", color: "#fff", cursor: "pointer" }}
                >
                    Join
                </button>
            </div>
        </div>
        </>
    );
}

export default Classjoin;