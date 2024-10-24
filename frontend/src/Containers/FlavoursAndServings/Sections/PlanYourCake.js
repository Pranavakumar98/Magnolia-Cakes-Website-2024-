import React from "react";
import "./PlanYourCake.css";

const PlanYourCake = ({ flavServInfo }) => (
  <div className="plan-your-cake">
    <h1>Plan Your Cake</h1>

    {/* Cake description and image */}
    <div className="description-and-image">
      <p className="description description-plan-cake">
        At Magnolia Cake Shop, we transform cake-making into an art, creating
        desserts that are both stunning and delicious. Our custom cakes, perfect
        for any occasion, are tailored to your vision, ensuring a delightful
        experience for every guest. With a range of sizes and styles, we craft
        each cake with care and love to make your special moments even sweeter,
        so you can focus on creating cherished memories.
      </p>
      {/* Cake image with tier details */}
      <div className="image">
        <img src={flavServInfo.image4} alt="Cake" />
        <div className="cake-tier-texts">
          {/* Display tier information */}
          <div className="cake-tier">
            <p>6" & 8" Tier: 40 servings (rectangles)</p>
          </div>
          <div className="cake-tier">
            <p>8" & 10" Tier: 66 servings (rectangles)</p>
          </div>
          <div className="cake-tier">
            <p>6", 8", & 10" Tier: 80 servings (rectangles)</p>
          </div>
        </div>
      </div>
    </div>
  </div>
);

export default PlanYourCake;
