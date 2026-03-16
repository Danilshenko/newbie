    import './styleForm.css';
    import { Link } from 'react-router-dom';
    import { toast } from 'react-toastify';
    import { useState } from 'react';

    function Register(){
        const [username, setUsername] = useState('');
        const [password, setPassword] = useState('');
        const [email, setEmail] = useState('');

        function changeUsername(e){
            const result = e.target.value.replace(/[^a-zA-Z0-9]/g, '')
            setUsername(result);
        }

        function changeEmail(e){
            const result = e.target.value.replace(/[^a-zA-Z0-9@.]/g, '')
            setEmail(result);
        }
        function changePassword(e){ 
            const result = e.target.value.replace(/[^a-zA-Z0-9]/g, '')
            setPassword(result);
        }

        async function postUsers(){
            // If input
            if(!username.trim() || !email.trim() || !password.trim()){
                toast.error("Please fill in all fields!");
                return;
            } 
            if(username.length > 15){
                toast.error("Nickname is more than 15 characters long");
                return;
            }
            if(email.length > 30){
                toast.error("Email is more than 30 characters long")
                return;
            }
            if(password.length < 6){
                toast.error("Password must be at least 6 characters long")
                return;
            }
            // POST request
            try{
                const response = await fetch('https://newbie-9.onrender.com/users', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username, password, email})
                })
                const data = await response.json();
                if(response.ok){
                    toast.success("Register Compited");
                } else{
                    toast.error("A user with this nickname or email already exists.")
                }
                console.log(data)
            }catch(err){
                toast.warning("No connection to the server")
            }
        }

        return(
            <div className="main-block">
                <div className='register-block'>
                    <div className='text-block'>
                        <h1 className='text-block__top'>Register with email</h1>
                        <p className='text-block__buttom'>Make a new doc to bring your words, fata,
                        and teams together. For free</p>
                    </div>
                    <div className='form-block'>
                        <div className='input-group'>
                        <img src='/icons/User.svg' alt='icon'/>
                        <input className='username-form'  
                        onChange={changeUsername} 
                        placeholder='Username'
                        maxLength="15"
                        value={username}
                        required/>
                        </div>
                        <div className='input-group'>
                        <img src='/icons/Email.svg' alt='icon'/>
                        <input className='email-form' 
                        onChange={changeEmail} 
                        placeholder='Email'
                        maxLength="30"
                        value={email}
                        required/>
                        </div>
                        <div className='input-group'>
                        <img src='/icons/Password.svg' alt='icon'/>
                        <input className='password-form'
                        type='password'
                        onChange={changePassword} 
                        placeholder='Password'
                        maxLength="20"
                        value={password}
                        required/>
                        </div>
                        <button 
                        className="btn-register"
                        onClick={postUsers}>Register</button>
                        <div className="auth-footer">
                            <span>Already have an account?</span>
                            <Link className="footer-btn" to='/login'>Log in</Link>
                        </div>
                    </div>
                </div>
            </div>
        )
    }


    export default Register;