import React from "react";
import List from "../List";
import "./OurFlavour.css";

const OurFlavours = ({ flavServInfo, flavServLists }) => (
  <div className="flavours-and-servings">
    <h1 style={{ fontFamily: "Alkarta" }}>{flavServInfo.heading3}</h1>
    <p className="description">{flavServInfo.description3}</p>
    <div className="flav-serv-lists">
      {/* Rendering list of flavours and servings */}
      {flavServLists.map((flavServList) => (
        <List
          key={flavServList.title}
          listTitle={flavServList.title}
          listOptions={flavServList.list}
        />
      ))}
    </div>
    {/* Extra information points */}
    <ul className="extra-info">
      {flavServInfo.extra_points.map((point) => (
        <li key={flavServInfo.extra_points.indexOf(point)}>{point}</li>
      ))}
    </ul>
  </div>
);

export default OurFlavours;
