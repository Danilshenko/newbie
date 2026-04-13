import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import { useState } from "react";
import "../RegisterRequest/styleForm.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function changeEmail(e) {
    setEmail(e.target.value);
  }
  function changePassword(e) {
    setPassword(e.target.value);
  }

  async function postUsers() {
    try {
      const response = await fetch("https://newbie0.onrender.com/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (response.ok) {
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("email", email);
        toast.success("Success! Redirecting...");
        setTimeout(() => {
          window.location.href = "/profile";
        }, 3000);
      } else {
        toast.error(data.message || "Wrong email or password");
      }
      console.log(data);
    } catch (err) {
      toast.warning("Server is sleeping. Try again in 1 minute.");
    }
<<<<<<< HEAD
  }
  return (
    <div className="main-block">
      <div className="register-block">
        <div className="text-block">
          <h1 className="text-block__top">Login with email</h1>
          <p className="text-block__buttom">
            Make a new doc to bring your words, fata, and teams together. For
            free
          </p>
=======
    function changePassword(e){
        setPassword(e.target.value)
    }

    async function postUsers(){
        try{
            const response = await fetch('https://newbie0.onrender.com/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email, password})
            })
            const data = await response.json();

            if(response.ok){
                localStorage.setItem('token', data.access_token);
                toast.success("Success! Redirecting...")
                setTimeout(() => {
                    window.location.href = '/profile'
                }, 3000);
            } else{
                toast.error(data.message || "Wrong email or password")
            }
            console.log(data)
        }catch(err){
            toast.warning("Server is sleeping. Try again in 1 minute.")
        } 
    }

    // async function getUsers(){
    //     try{
    //         const response = await fetch('https://newbie-9.onrender.com/users')
    //         if(!response.ok) throw new Error('Ошибка сети');
    //         const data = await response.json();
    //         console.log(data);
    //     }catch(error){
    //         console.error(error);
    //     }
    // }

    return(
        <div className="main-block">
            <div className='register-block'>
                <div className='text-block'>
                    <h1 className='text-block__top'>Login with email</h1>
                    <p className='text-block__buttom'>Make a new doc to bring your words, fata,
                    and teams together. For free</p>
                </div>
                <div className='form-block'>
                    <div className='input-group'>
                    <img src='/icons/Email.svg' alt='icon'/>
                    <input className='email-form' 
                    value={email}
                    onChange={changeEmail} 
                    placeholder='Email'/>
                    </div>
                    <div className='input-group'>
                    <img src='/icons/Password.svg' alt='icon'/>
                    <input className='password-form' 
                    value={password}
                    type='password'
                    onChange={changePassword} 
                    placeholder='Password'/>
                    </div>
                    <button     
                    className="btn-login"
                    onClick={postUsers}>Login</button>
                    <div className="auth-footer">
                        <span>Haven't you created an account yet?</span>
                        <Link className="footer-btn" to="/register">Register</Link>
                    </div>
                </div>
            </div>
>>>>>>> d4f6d77bb1d20c716cba1a2c6ef97004acc72471
        </div>
        <div className="form-block">
          <div className="input-group">
            <img src="/icons/Email.svg" alt="icon" />
            <input
              className="email-form"
              value={email}
              onChange={changeEmail}
              placeholder="Email"
            />
          </div>
          <div className="input-group">
            <img src="/icons/Password.svg" alt="icon" />
            <input
              className="password-form"
              value={password}
              type="password"
              onChange={changePassword}
              placeholder="Password"
            />
          </div>
          <button className="btn-login" onClick={postUsers}>
            Login
          </button>
          <div className="auth-footer">
            <span>Haven't you created an account yet?</span>
            <Link className="footer-btn" to="/register">
              Register
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
