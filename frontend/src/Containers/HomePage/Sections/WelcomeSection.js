import React, { useEffect, useState } from "react";
import { parseStringToParagraphsByNewline } from "utils/parseStringsToArray";
import "./WelcomeSection.css";

const WelcomeSection = ({ api }) => {
  const [content, setContent] = useState({
    heading: "Loading...",
    paragraph: ["Loading..."],
    image: null,
  });

  useEffect(() => {
    api
      .get("/api/homepage-welcome/")
      .then((response) => {
        const responseData = response.data;
        setContent({
          heading: responseData.heading,
          paragraph: parseStringToParagraphsByNewline(responseData.paragraph),
          image: responseData.image,
        });
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, [api]);

  return (
    <div className="welcome-section">
      <h2>{content.heading}</h2>
      <div className="welcome-body">
        <div className="body-content">
          {content.paragraph.map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
        </div>
        {content.image && (
          <img
            className="welcome-cake"
            src={content.image}
            alt="Decorative Cake"
          />
        )}
      </div>
    </div>
  );
};

export default WelcomeSection;
