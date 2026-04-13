import './profile.css'

function Profile() {
  return (
    <div className="container">
      <div className="card">
        <div className="header-info">
          <div className="profil-avatar">
            <img src="https://picsum.photos/300/200" alt="avatar icon" />
            <span className="online"></span>
          </div>
          <div className="user-info">
            <h2>{localStorage.getItem('username') || 'Undefined'}</h2>
            <p>{localStorage.getItem('email') || 'Undefined'}</p>
            <span className="badge">Verified User</span>
          </div>
          <button className="edit-btn">Edit</button>
        </div>
        <hr />
        <div className="block">
          <h3>Account Info</h3>
          <p>Full Name: {localStorage.getItem('username') || 'Undefined'} </p>
          <p>Email: {localStorage.getItem('email') || 'Undefined'}</p>
          <p>Joined: March 2026</p>
        </div>
        <div className="block">
          <h3>Activity</h3>
          <div className="stats">
            <div className="stat">
              <h4>12</h4>
              <p>Orders</p>
            </div>
            <div className="stat">
              <h4>3</h4>
              <p>Cart</p>
            </div>
            <div className="stat">
              <h4>8</h4>
              <p>Favorites</p>
            </div>
          </div>
        </div>
        <div className="block">
          <h3>Settings</h3>
          <button className="setting-btn">Change Password</button>
          <button className="setting-btn logout">Logout</button>
        </div>
      </div>
    </div>
  );
}

export default Profile;
