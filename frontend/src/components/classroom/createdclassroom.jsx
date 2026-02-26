import {react} from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Createclassroom = () => {
    const navigate = useNavigate();
    const [className, setClassName] = useState("");
    const [error, setError] = useState("");
    return(
        <>
        </>
    );
}

export default Createclassroom;