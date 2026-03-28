import './App.css';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Register from './Component/RegisterRequest/Register';
import Login from './Component/LoginRequest/Login'
import Main from './Component/Main/Main'
import Verify from './Component/Verify/Verify';
import Profile from './Component/Profile/Profile';
import ProductPage from './Component/ProductPage/ProductPage';

function App() {
  return (
    <Router>
    <div className="main-app">
      <Routes>
        <Route path='/' element={<Navigate to='/login'/>}/>
        <Route path='/register' element={<Register/>}/>
        <Route path='/login' element={<Login/>}/>
        <Route path='/main' element={<Main/>}/>
        <Route path='/verify' element={<Verify/>}/>
        <Route path='/profile' element={<Profile/>}/>
        <Route path='/cardspage' element={<ProductPage/>}/>

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
// 1 страница,регистрация,2 страница логин,3 подтверждение почты,3.1 сайт,4 профиль,4.1 корзина,, verify-email,,favorites(для корзины),,