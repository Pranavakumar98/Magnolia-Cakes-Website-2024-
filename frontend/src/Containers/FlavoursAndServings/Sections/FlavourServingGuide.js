import React from "react";
import "./FlavourServingGuide.css";

const FlavoursServingsGuide = ({ flavServInfo }) => (
  <div className="flavours-servings-guide">
    <div className="guide-content">
      <div className="guide-image">
        <img src={flavServInfo?.image1} alt="Cake" />
      </div>
      <div className="guide-text">
        <h1>{flavServInfo.heading1}</h1>
        <p className="guide-top-descp">{flavServInfo.description1}</p>
      </div>
    </div>
  </div>
);

export default FlavoursServingsGuide;
