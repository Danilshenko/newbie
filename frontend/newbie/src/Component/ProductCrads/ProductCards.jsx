import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "./productcards.css";

function ProductCards({ category, title, description, price, reviews }) {
  const navigate = useNavigate()
  return (
    <div className="product-card" onClick={() => navigate=("/cardspage")}>
      <span className="product-card__badge">{category || "New"}</span>
      <div className="product-card__image-container">
        <img
          src="https://picsum.photos/300/200"
          alt='photo cards'
          className="product-card__img"
        />
      </div>
      <div className="product-card__content">
        <h4 className="product-card__title">{title}</h4>
        <p className="product-card__description">{description}</p>
        <div className="product-card__rating">
          <span className="product-card__stars">★★★★★</span>
          <span className="product-card__reviews">{reviews}</span>
        </div>
        <div className="product-card__footer">
          <span className="product-card__price">{price}₴</span>
          <button className="product-card__add-btn" onClick={(e) => e.stopPropagation()}>Add to Cart</button>
        </div>
      </div>
    </div>
  );
}

export default ProductCards;
