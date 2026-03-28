import { useState, useEffect } from "react";
import { toast } from "react-toastify";
import "./verify.css";

function Verify() {
  const [code, setCode] = useState(['']);

  function handleClick(index, value) {
    const newCode = [...code];
    newCode[index] = value;
    console.log(newCode);
    setCode(newCode);
  }

  useEffect(() => {

  });

  async function clickFunction() {
    if (!code < 4) {
      const result = [...code].join("");
      try{
        const response = await fetch(
          "https://newbie0.onrender.com/verify-email",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ result }),
          },
        );
        const data = await response.json();
        if(response.ok){
          localStorage.setItem('token', data.access_token)
          toast.success('Email confirmed')
        }else{
          toast.error('Invalid code')
        }
        console.log(data);
      } catch(error){
        toast.error('Fill in all fields')
      }

      }
  }
  return (
    <div className="verify-card">
      <div className="verify-text__block">
        <h1 className="verify-title">Verify your Email</h1>
        <p className="verify-subtitle">
          We sent a 4-digit code to:
          <br />
          <span className="user-email">{localStorage.getItem('email')}</span>
          <br />
          Enter it below to activate your account.
        </p>
      </div>
      <div className="code-block">
        <div className="code-input-group">
          <input
            onChange={(e) =>
              handleClick(0, e.target.value.replace(/[^0-9]/g, ""))
            }
            type="text"
            value={code[0]}
            className="code-input"
            maxLength="1"
            placeholder="0"
          />
          <input
            onChange={(e) =>
              handleClick(1, e.target.value.replace(/[^0-9]/g, ""))
            }
            type="text"
            value={code[1]}
            className="code-input"
            maxLength="1"
            placeholder="0"
          />
          <input
            onChange={(e) =>
              handleClick(2, e.target.value.replace(/[^0-9]/g, ""))
            }
            type="text"
            value={code[2]}
            className="code-input"
            maxLength="1"
            placeholder="0"
          />
          <input
            onChange={(e) =>
              handleClick(3, e.target.value.replace(/[^0-9]/g, ""))
            }
            type="text"
            value={code[3]}
            className="code-input"
            maxLength="1"
            placeholder="0"
          />
        </div>
        <button className="btn-confirm" onClick={() => clickFunction()}>
          Confirm Code
        </button>
        <div className="resend-link">
          Didn't get the code? <a href="#">Resend</a>
        </div>
      </div>
    </div>
  );
}

export default Verify;
