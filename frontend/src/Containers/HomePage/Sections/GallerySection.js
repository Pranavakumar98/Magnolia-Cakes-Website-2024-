import React, { useEffect, useState } from "react";
import GalleryGridItem from "Components/GalleryGridItem/GalleryGridItem";
import { getGalleryCategoryParam } from "utils/getGalleryCategoryParam";
import { everyFirst, everyNth } from "utils/getEveryNthElementInArray";
import { getSortedObjectsByAscId } from "utils/getSortedObjects";

import "./GallerySection.css";

const GallerySection = ({ api }) => {
  const [heading, setHeading] = useState("Loading...");
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    api
      .get("/api/homepage-gallery/")
      .then((response) => {
        // Set the retrieved content in the state
        setHeading(response.data.heading);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });

    api
      .get("/api/gallery/categories/")
      .then((response) => {
        setCategories(getSortedObjectsByAscId(response.data));
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, [api]);

  return (
    <div className="gallery-section-wrapper">
      <h2>{heading}</h2>
      {categories.length <= 0 && <p>Loading...</p>}
      {categories.length > 0 && (
        <div className="gallery-row">
          {/* Left Column */}
          <div className="gallery-column left-column">
            {everyFirst(categories).map((category, index) => {
              let sizeClass = "medium-image"; // Default to medium size
              if (index === 0) {
                sizeClass = "large-image"; // First image is large
              } else if (index === 1) {
                sizeClass = "small-image"; // Second image is small
              } 
              return (
                <GalleryGridItem
                  key={category.id}
                  src={category.picture}
                  alt={category.name}
                  title={
                    <div className="line-text-container">
                      <div className="text">{category.name}</div>
                      <div className="circle"></div>
                    </div>
                  }
                  link={
                    "/gallery/?category=" + getGalleryCategoryParam(category.name)
                  }
                  className={sizeClass} /* Apply the size class */
                />
              );
            })}
          </div>
  
          {/* Right Column */}
          <div className="gallery-column right-column">
            {everyNth(categories, 2).map((category) => (
              <GalleryGridItem
                key={category.id}
                src={category.picture}
                alt={category.name}
                title={
                  <div className="line-text-container">
                    <div className="text">{category.name}</div>
                    <div className="circle"></div>
                  </div>
                }
                link={
                  "/gallery/?category=" + getGalleryCategoryParam(category.name)
                }
                className="right-image"
                isOnRight={true}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};  

export default GallerySection;
