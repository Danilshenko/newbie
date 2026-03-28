import { toast } from "react-toastify";
import { useState, useEffect } from "react";
import Header from "../Header/Header";
import SideBar from "../SideBar/SideBar";
import ProductCards from "../ProductCrads/ProductCards";
import ProductData from '../../data/cards.json';
import "./main.css";

function Main() {
  const [count, setCount] = useState(0);
  const [username, setUsername] = useState("");
  const [countLength, setCountLength] = useState(0);

  useEffect(() => {
    async function getUsersData() {
      const token = localStorage.getItem("token");
      console.log(token);
      if (!token || token === "undefined") return;

      try {
        const response = await fetch("https://newbie0.onrender.com/me", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (response.ok) {
          const data = await response.json();
          setCount(data.basket.length);
          setUsername(data.username);
        }
      } catch (err) {
        console.error(err);
        setCount(count);
        toast.error("No response from the server");
      }
    }
    getUsersData();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
  <>
      <Header/>
      <main>
      <SideBar/>
      <section className="column-cards">
        {ProductData.map((item) => (
          <ProductCards
          key={item.id}
          title={item.title}
          description={item.description}
          price={item.price}
          reviews={item.reviews}
          />
        ))}
      </section>
      </main>
  </>
  );
}

export default Main;
