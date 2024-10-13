import React from "react";
import "./BadgesSection.css";

const BadgesSection = () => {
  const badges = [
    {
      symbol: "/images/badge-cake.png",  // Cake icon
      title: "Cakes and Cupcakes",
      description: "We do custom cakes and cupcakes to suit your every need."
    },
    {
      symbol: "/images/badge-mixing.png",  // Mixing icon
      title: "Locally Sourced Ingredients",
      description: "We use high-quality ingredients hand-picked for the best taste."
    },
    {
      symbol: "/images/badge-heart.png",  // Heart icon
      title: "Love & Care",
      description: "Every cake I create is a cherished slice of someone's special moment."
    },
    {
      symbol: "/images/badge-plant.png",  // Gluten-free icon
      title: "Gluten-Free Friendly",
      description: "We meet any dietary restrictions with our cakes."
    }
  ];

  return (
    <div className="badges-section">
      {badges.map((badge, index) => (
        <div key={index} className="badge-item">
          <img
            className="badge-icon"
            src={badge.symbol}
            alt={`${badge.title} icon`}
          />
          <h3>{badge.title}</h3>
          <p>{badge.description}</p>
        </div>
      ))}
    </div>
  );
};

export default BadgesSection;
