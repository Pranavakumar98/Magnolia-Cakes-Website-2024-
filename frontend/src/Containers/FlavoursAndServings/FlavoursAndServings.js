import React, { useEffect, useState } from "react";
import List from "./List";

import "./FlavoursAndServings.css";
import { parseStringToArrayByComma } from "utils/parseStringsToArray";
import FlavoursServingSymphony from "./Sections/FlavourServingSymphony";
import FlavoursServingsGuide from "./Sections/FlavourServingGuide";
import OurFlavours from "./Sections/OurFlavour";
import PlanYourCake from "./Sections/PlanYourCake";
import RoundCakeServingGuide from "./Sections/RoundCakeServingGuide";
import SquareCakeServingGuide from "./Sections/SquareCakeServingGuide";
import DeliverySection from "Containers/HomePage/Sections/DeliverySection";

const FlavoursAndServings = ({ api }) => {
  const [flavServLists, setFlavServLists] = useState([]);
  const [flavServInfo, setFlavServInfo] = useState({
    description1: "",
    description2: "",
    description3: "",
    extra_points: [],
    heading1: "",
    heading2: "",
    heading3: "",
    id: "",
    image1: "",
    image2: "",
    image4: "",
    image5: "",
    image6: "",
  });

  useEffect(() => {
    // Fetch data for the flavour and serving lists
    api
      .get("/api/flavours-and-servings/")
      .then((response) => {
        setFlavServLists(
          response.data.sort((a, b) => a.id - b.id) // Sort the lists by ID
        );
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });

    // Fetch data for flavour and serving information
    api
      .get("/api/flavours-and-servings-info/")
      .then((response) => {
        setFlavServInfo({
          ...response?.data,
          extra_points: parseStringToArrayByComma(response.data.extra_points), // Parse extra points string into an array
        });
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, [api]);

  return (
    <>
      {/* Guide Section */}
      <FlavoursServingsGuide flavServInfo={flavServInfo} />

      {/* Symphony of Flavours Section */}
      <FlavoursServingSymphony flavServInfo={flavServInfo} />

      {/* Our Flavours Section */}
      <OurFlavours flavServInfo={flavServInfo} flavServLists={flavServLists} />

      {/* Plan Your Cake Section */}
      <PlanYourCake flavServInfo={flavServInfo} />

      {/* Round Cake Serving Guide */}
      <RoundCakeServingGuide flavServInfo={flavServInfo} />

      {/* Square Cake Serving Guide */}
      <SquareCakeServingGuide flavServInfo={flavServInfo} />

      <DeliverySection />
    </>
  );
};

export default FlavoursAndServings;
