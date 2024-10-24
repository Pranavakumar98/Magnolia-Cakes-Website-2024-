import React from "react";
import "./RoundCakeServingGuide.css";

const RoundCakeServingGuide = ({ flavServInfo }) => (
  <div className="serving-guide">
    <div className="serving-row">
      {/* Round cake image */}
      <img
        src={flavServInfo.image5}
        alt="Round Cake Serving"
        className="serving-image"
        style={{ maxHeight: "500px" }}
      />
      {/* Serving details for round cakes */}
      <div className="serving-details">
        <h1>Round Cake Serving Guide</h1>
        <p className="description" style={{ maxWidth: "70%" }}>
          Our round cakes offer elegance and flexibility, whether you're serving
          a small or large gathering. Refer to the chart below to determine the
          best size for your event.
        </p>
      </div>
    </div>

    {/* Round Cake Serving Table */}
    <div className="serving-table-container">
      <table className="serving-table">
        <thead>
          <tr>
            <th className="top-none left-none">Size</th>
            <th className="top-none">Standard Serves</th>
            <th className="top-none right-none">Coffee Serves</th>
          </tr>
        </thead>
        <tbody>
          {/* Table rows for round cake serving sizes */}
          <tr>
            <td className="top-none left-none">6"</td>
            <td className="left-none">12</td>
            <td className="right-none">18</td>
          </tr>
          <tr>
            <td className="left-none">8"</td>
            <td>20</td>
            <td className="right-none">25</td>
          </tr>
          <tr>
            <td className="left-none">10"</td>
            <td>30</td>
            <td className="right-none">40</td>
          </tr>
          <tr>
            <td className="left-none">12"</td>
            <td>40</td>
            <td className="right-none">55</td>
          </tr>
          <tr>
            <td className="left-none">14"</td>
            <td>65</td>
            <td className="right-none">75</td>
          </tr>
          <tr>
            <td className="left-none bottom-none">16"</td>
            <td className="bottom-none">75</td>
            <td className="right-none bottom-none">100</td>
          </tr>
        </tbody>
      </table>
    </div>

    {/* Round cake serving size note */}
    <p className="serving-note">
      "These serving sizes are based on standard portions and are meant to serve
      as a general guideline. Keep in mind that cake height, slicing methods,
      and individual preferences may influence the final number of servings. We
      recommend discussing your specific needs with our team to ensure you have
      the perfect cake for your celebration."
    </p>
  </div>
);

export default RoundCakeServingGuide;
