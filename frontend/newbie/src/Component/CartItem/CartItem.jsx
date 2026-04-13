
import './cartitem.css'

function CartItem({ quality, sumQuality, img, title, price}) {

  return (
    <>
      <div className="card-item__content">
        <img className="card-item__img" src={img} alt="Cart img"/>
        <div className="product-item-card__footer">
            <h4 className="card-item__title">{title}</h4>
            <span className="card-item__price">{price}₴</span>
            <div className="product-page__quantity-selector">
              <button
                className="cart-page__qty-btn"
                onClick={() => sumQuality(quality > 1 ? quality - 1 : 1)}>
                -
              </button>
              <span className="cart-page__qty-value">{quality}</span>
              <button
                className="cart-page__qty-btn"
                onClick={() => sumQuality(quality + 1)}>
                +
              </button>
            </div>
        </div>
      </div>
    </>
  );
}

export default CartItem;
