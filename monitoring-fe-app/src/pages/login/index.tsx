import React from "react";
import { useNavigate } from "react-router-dom";

import "./loginStyle.scss";

export default function Login() {
  let navigate = useNavigate();

  return (
    <div className="Login-container">
      <div className="login-body">
        {'login'}      
      </div>
    </div>
  );
}
