import React from "react";
import "./FlavourServingSymphony.css"

const FlavoursServingSymphony = ({ flavServInfo }) => (
  <>
    <div className="flavours-servings-symphony">
      <div className="guide-text">
        <h1>{flavServInfo.heading2}</h1>
        <p className="m-top">{flavServInfo.description2}</p>
      </div>
    </div>
    {/* Image related to the symphony of flavours */}
    <img
      src={flavServInfo.image2}
      style={{ maxHeight: "150px", objectFit: "cover" }}
      alt="Symphony of Flavours"
    />
  </>
);

export default FlavoursServingSymphony;
