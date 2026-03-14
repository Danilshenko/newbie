import './apiRequest.css'

function ApiRequest(){

    async function getPost(){
        const response =  await fetch('./users.db');
        const data = await response.json()
        console.log(data)
    }

    return(
        <div className="main-block">
            <button 
            className="click-request"
            onClick={() => getPost()}
            >Click
            </button>
        </div>
    )
}

export default ApiRequest;