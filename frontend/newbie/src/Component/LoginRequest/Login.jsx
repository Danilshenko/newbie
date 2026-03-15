

function Login(){
    async function getUsers(){
        try{
            const response = await fetch('https://newbie-7.onrender.com/users')
            if(!response.ok) throw new Error('Ошибка сети');
            const data = await response.json();
            console.log(data);
        }catch(error){
            console.error(error);
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
                    {/* <div className='input-group'>
                    <img src='./icons/User.svg' alt='icon'/>
                    <input className='username-form'  
                    onChange={changeUsername} placeholder='Username'/>
                    </div> */}
                    {/* <div className='input-group'>
                    <img src='./icons/Email.svg' alt='icon'/>
                    <input className='password-form' 
                    onChange={changeEmail} placeholder='Email'/>
                    </div>
                    <div className='input-group'>
                    <img src='./icons/Password.svg' alt='icon'/>
                    <input className='email-form' 
                    onChange={changePassword} placeholder='Password'/>
                    </div> */}
                    <button     
                    className="btn-login"
                    onClick={getUsers}>Login</button>
                    <div className="auth-footer">
                        <span>Already have an account?</span>
                        <a className="footer-btn" href="/register">Register</a>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default Login;