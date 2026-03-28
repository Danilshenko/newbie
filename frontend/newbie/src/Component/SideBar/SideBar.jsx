import './sidebar.css';

function  Sidebar(){
  return (
    <section className="catalog-sidebar">
      <div className="sidebar__header">
        <span className="sidebar__filter-icon">▽</span>
        <h2 className="sidebar__title">Filters</h2>
      </div>
      <div className="sidebar__section">
        <div className="sidebar__section-header">
          <h3 className="sidebar__section-title">Categories</h3>
          <span className="sidebar__arrow sidebar__arrow--up">⌃</span>
        </div>
        <div className="sidebar__list">
          {[
            { name: 'Electronics', count: 156 },
            { name: 'Clothing', count: 89 },
            { name: 'Books', count: 234 },
            { name: 'Home & Garden', count: 67 },
            { name: 'Sports', count: 45 },
            { name: 'Beauty', count: 78 }
          ].map((category) => (
            <label key={category.name} className="sidebar__checkbox-item">
              <input type="checkbox" className="sidebar__checkbox" />
              <span className="sidebar__category-name">{category.name}</span>
              <span className="sidebar__category-count">{category.count}</span>
            </label>
          ))}
        </div>
      </div>
      <div className="sidebar__section">
        <div className="sidebar__section-header">
          <h3 className="sidebar__section-title">Price Range</h3>
          <span className="sidebar__arrow sidebar__arrow--up">⌃</span>
        </div>
        <div className="sidebar__price-slider-container">
          <input 
            type="range" 
            min="0" 
            max="1000" 
            defaultValue="500"
            className="sidebar__price-slider" 
          />
          <div className="sidebar__price-labels">
            <span>$0</span>
            <span>$1000</span>
          </div>
        </div>
      </div>
      <div className="sidebar__section">
        <div className="sidebar__section-header">
          <h3 className="sidebar__section-title">Minimum Rating</h3>
          <span className="sidebar__arrow sidebar__arrow--up">⌃</span>
        </div>
        <div className="sidebar__list">
          {[4, 3, 2, 1].map((stars) => (
            <label key={stars} className="sidebar__checkbox-item">
              <input type="checkbox" className="sidebar__checkbox" />
              <span className="sidebar__category-name">Stars</span>
            </label>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Sidebar;