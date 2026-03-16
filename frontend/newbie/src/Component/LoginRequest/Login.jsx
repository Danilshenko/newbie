import { Link } from 'react-router-dom';
import '../RegisterRequest/styleForm.css'
import { useState } from 'react';

function Login(){
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    function changeEmail(e){
        setEmail(e.target.value)
    }
    function changePassword(e){
        setPassword(e.target.value)
    }

    async function postUsers(){
        try{
            const response = await fetch('https://newbie-9.onrender.com/users', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email, password})
            })
            const data = await response.json();
            console.log(data)
        }catch(err){
            console.error(err)
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
                    onChange={changeEmail} placeholder='Email'/>
                    </div>
                    <div className='input-group'>
                    <img src='/icons/Password.svg' alt='icon'/>
                    <input className='password-form' 
                    onChange={changePassword} placeholder='Password'/>
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
        </div>
    )
}
export default Login;