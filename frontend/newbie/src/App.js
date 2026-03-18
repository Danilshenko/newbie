import './App.css';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Register from './Component/RegisterRequest/Register';
import Login from './Component/LoginRequest/Login'
import Main from './Component/Main/Main'

function App() {
  return (
    <Router>
    <div className="main-app">
      <Routes>
        <Route path='/' element={<Navigate to='/login'/>}/>
        <Route path='/register' element={<Register/>}/>
        <Route path='/login' element={<Login/>}/>
        <Route path='/profile' element={<Main/>}/>
      </Routes>
        <ToastContainer 
          position="top-right" 
          autoClose={3000}
          hideProgressBar={false} 
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="dark" 
        />
    </div>
    </Router>
  );
}

export default App;
