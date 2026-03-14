import './apiRequest.css'

function ApiRequest(){

    async function getUsers(){
        try{
            const response = await fetch('https://linsey-torporific-peevishly.ngrok-free.dev/users')
            if(!response.ok) throw new Error('Ошибка сети');
            const data = await response.json();
            console.log(data);
        }catch(error){
            console.error(error);
        }
    }

    function handleChange(e){
        console.log(e.target.value);
    }

    return(
        <div className="main-block">
            <div className='form-block'>
                <input className='form' 
                onChange={handleChange}/>
                <button 
                className="click-request"
                onClick={getUsers}
                >Click
                </button>
            </div>
        </div>
    )
}

export default ApiRequest;