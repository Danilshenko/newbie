import { useState } from "react";
import "./productpage.css";

function ProductPage({}) {
  const [quality, setQuality] = useState(1);
  return (
    <div className="product-page">
      <div className="product-page__container">
        <div className="product-page__gallery">
          <div className="product-page__main-image-wrapper">
            <img
              src="https://picsum.photos/600/500"
              alt="Product img"
              className="product-page__main-img"
            />
          </div>
          <div className="product-page__thumbnails">
            <img
              src="https://picsum.photos/100/100?1"
              alt="img thumb"
              className="product-page__thumb"
            />
            <img
              src="https://picsum.photos/100/100?2"
              alt="img thumb"
              className="product-page__thumb"
            />
            <img
              src="https://picsum.photos/100/100?3"
              alt="img thumb"
              className="product-page__thumb"
            />
          </div>
        </div>
        <div className="product-page__details">
          <span className="product-page__category">Electronics</span>
          <h1 className="product-page__title">Premium Wireless Headphones</h1>

          <div className="product-page__price-block">
            <span className="product-page__price">12 500 ₴</span>
            <span className="product-page__old-price">15 000 ₴</span>
          </div>
          <div className="product-page__divider"></div>
          <div className="product-page__description-block">
            <h3>Description</h3>
            <p className="product-page__description">
              High-quality sound with active noise cancellation. Comfortable ear
              cushions for long listening sessions. Up to 40 hours of battery
              life.
            </p>
          </div>
          <div className="product-page__divider"></div>
          <div className="product-page__action-block">
            <div className="product-page__quantity-selector">
              <button
                className="product-page__qty-btn"
                onClick={() => setQuality(quality > 1 ? quality - 1 : 1)}
              >
                -
              </button>
              <span className="product-page__qty-value">{quality}</span>
              <button
                className="product-page__qty-btn"
                onClick={() => setQuality(quality + 1)}
              >
                +
              </button>
            </div>
            <button className="product-page__add-to-cart-btn">
              Add to Cart
            </button>
          </div>
          <div className="product-page__meta">
            <p>SKU: WH-1000XM4</p>
            <p>Availability: In Stock</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductPage;
