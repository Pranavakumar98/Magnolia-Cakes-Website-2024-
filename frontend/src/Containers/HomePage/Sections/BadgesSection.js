import React, { useEffect, useState } from "react";
import { parseStringToParagraphsByNewline } from "utils/parseStringsToArray";
import "./BadgesSection.css";

const BadgesSection = ({ api }) => {
    const [badges, setBadges] = useState([
      {
        symbol: null,
        title: "Loading...",
        description: "Loading...",
      },
    ]);
  
    useEffect(() => {
      api
        .get("/api/badges/")
        .then((response) => {
          // Set the retrieved badges content in the state
          const responseData = response.data;
          setBadges(responseData.badges); // Assuming response contains an array of badges
        })
        .catch((error) => {
          console.error("Error fetching badges:", error);
        });
    }, [api]);
  
    return (
      <div className="badges-section">
        {badges.map((badge, index) => (
          <div key={index} className="badge-item">
            {badge.symbol && (
              <img
                className="badge-icon"
                src={badge.symbol}
                alt={`${badge.title} icon`}
              />
            )}
            <h3>{badge.title}</h3>
            <p>{badge.description}</p>
          </div>
        ))}
      </div>
    );
  };
  
  export default BadgesSection;