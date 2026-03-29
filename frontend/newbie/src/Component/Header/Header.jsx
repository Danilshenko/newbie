import { Link } from "react-router-dom";
import { useState } from "react";
import './header.css'

function Header({quality, username}){

    return(
      <header className="header">
        <span className="logo">NewBie</span>
        <div className="search-bar">
          <input type="text" placeholder="Search..."/>
        </div>
        <div className="header__right-side">
          <div className="header__cart-wrapper">
            <span className="header__cart-icon">🛒</span>
            <span className="header__cart-count">{quality}</span>
          </div>
          <Link className="user-profile" to='/profile'>
            <img className="avatar" src="https://via.placeholder.com/40" alt="Avatar"/>
            <span className="username">{username}</span>
            <span className="arrow">▼</span>
          </Link>
        </div>
      </header>
    )
}

export default Header;