import './App.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Register from './Component/RegisterRequest/Register';
import Login from './Component/LoginRequest/Login'

function App() {
  return (
    <Router>
    <div className="main-app">
      <Routes>
        <Route path='/' element={<Navigate to='/register'/>}/>
        <Route path='/register' element={<Register/>}/>
        <Route path='/login' element={<Login/>}/>
      </Routes>
    </div>
    </Router>
  );
}

export default App;
