import { useState } from "react";
import CartItem from "../CartItem/CartItem";
import './cart.css'

function Cart({ cartId, isOpen, onClose}){
  const [quality, setQuality] = useState(1);

  function addQuality(clickAddQuelity){
    setQuality(quality + clickAddQuelity);
  }
  
  const qualityTotal = cartId.reduce((acc, result) => acc + result.quality, 0);
  const resultPrice = cartId.reduce((acc, result) => acc + result.price * quality, 0);

  console.log(resultPrice)
  // function sumPrice(item){
  //   const total = setQuality(item.reduce((acc, total) => acc + total.quality ,0))
  //   const result = setPrice(item.reduce((acc, result) => acc + result.price * result.quality, 0))
  // }

    return(
        <div className={`cart-overlay ${isOpen ? 'active' : ''}`} onClick={onClose}>
      <div className="cart-container" onClick={(e) => e.stopPropagation()}>
        <div className="cart-header">
          <h3>Shopping Cart</h3>
          <button className="close-cart-btn" onClick={onClose}>✕</button>
        </div>
        <div className="cart-content">
          {(cartId.map(item => 
            (<CartItem quality={item.quality} sumQuality={addQuality} id={item.id} img={item.img} title={item.title} price={item.price}/>)
          ))}
        </div>
        <div className="cart-footer">
          <span className="cart-footer__price">Price: {qualityTotal}₴</span>
          <button className="cart-footer__btn">Proceed to Checkout</button>
        </div>
      </div>
    </div>
    )
}
export default Cart;