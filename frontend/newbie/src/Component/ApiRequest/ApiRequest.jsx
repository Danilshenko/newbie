import './apiRequest.css'

function ApiRequest(){

    async function getPost(){
        const response =  await fetch('./users.db');
        const data = await response.json();
        console.log(data);
    }

    function handleChanhe(e){
        console.log(e.target.value);
    }

    return(
        <div className="main-block">
            <div className='form-block'>
            <input className='form' onChange={(e) => handleChanhe(e)}/>
            <button 
            className="click-request"
            onClick={() => getPost()}
            >Click
            </button>
            </div>
        </div>
    )
}

export default ApiRequest;