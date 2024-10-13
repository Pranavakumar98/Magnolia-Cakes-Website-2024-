import React, { useEffect, useState } from "react";
import "./CupcakesBanner.css";

const CupcakesBanner = ({ api }) => {
  const [banner, setBanner] = useState(null);
  const [clickCount, setClickCount] = useState(0); 

  useEffect(() => {
    api
      .get("/api/homepage-welcome/")
      .then((response) => {
        setBanner(response.data.banner);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, [api]);

  
  const handleClick = () => {
    setClickCount((prevCount) => prevCount + 1);

    
    if (clickCount + 1 === 10) {
      window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley";
    }

    
    if (clickCount + 1 === 20) {
      performAction();
      setClickCount(0); 
    }
  };

  
  const performAction = () => {
    
    
  };

  return (
    <>
      {banner && (
        <div
          className="cupcakes-banner"
          style={{ backgroundImage: `url(${banner})` }}
          onClick={handleClick} 
        />
      )}
    </>
  );
};

export default CupcakesBanner;
