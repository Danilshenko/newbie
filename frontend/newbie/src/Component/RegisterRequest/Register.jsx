import './styleForm.css';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import { useState } from 'react';

function Register(){
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');

    function changeUsername(e){
        setUsername(e.target.value);
    }
    function changePassword(e){
        setPassword(e.target.value);
    }
    function changeEmail(e){
        setEmail(e.target.value);
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

    async function postUsers(){
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
                    onChange={changeUsername} placeholder='Username'/>
                    </div>
                    <div className='input-group'>
                    <img src='/icons/Email.svg' alt='icon'/>
                    <input className='email-form' 
                    onChange={changeEmail} placeholder='Email'/>
                    </div>
                    <div className='input-group'>
                    <img src='/icons/Password.svg' alt='icon'/>
                    <input className='password-form' 
                    onChange={changePassword} placeholder='Password'/>
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