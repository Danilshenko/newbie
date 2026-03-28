import { Link } from "react-router-dom";
import { useState } from "react";
import './header.css'

function Header(){

    return(
      <header className="header">
        <span className="logo">NewBie</span>
        <div className="search-bar">
          <input type="text" placeholder="Search..."/>
        </div>
        <div className="header__right-side">
          <div className="header__cart-wrapper">
            <span className="header__cart-icon">🛒</span>
            <span className="header__cart-count">0</span>
          </div>
          <Link className="user-profile" to='/profile'>
            <img className="avatar" src="https://via.placeholder.com/40" alt="Avatar"/>
            <span className="username">@User_Name</span>
            <span className="arrow">▼</span>
          </Link>
        </div>
      </header>
    )
}

export default Header;