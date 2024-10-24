import React from "react";
import "./SquareCakeServingGuide.css";

const SquareCakeServingGuide = ({ flavServInfo }) => (
  <div className="serving-guide2">
    <div className="serving-row2">
      {/* Serving details for square cakes */}
      <div className="serving-details2">
        <h1>Square Cake Serving Guide</h1>
        <p
          className="description"
          style={{ maxWidth: "90%", textAlign: "start" }}
        >
          For those seeking a contemporary twist, our square cakes offer a sleek
          and modern design that stands out. Perfect for any celebration, they
          are as versatile as they are stylish. Use the chart below to easily
          plan your servings, ensuring every guest gets a perfect slice of your
          special cake.
        </p>
      </div>
      {/* Square cake image */}
      <img
        src={flavServInfo.image6}
        alt="Square Cake Serving"
        className="serving-image"
        style={{ maxHeight: "500px" }}
      />
    </div>

    {/* Square Cake Serving Table */}
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
          {/* Table rows for square cake serving sizes */}
          <tr>
            <td className="top-none left-none">6"</td>
            <td className="left-none">12</td>
            <td className="right-none">18</td>
          </tr>
          <tr>
            <td className="left-none">8"</td>
            <td>25</td>
            <td className="right-none">30</td>
          </tr>
          <tr>
            <td className="left-none">10"</td>
            <td>35</td>
            <td className="right-none">50</td>
          </tr>
          <tr>
            <td className="left-none">12"</td>
            <td>45</td>
            <td className="right-none">70</td>
          </tr>
          <tr>
            <td className="left-none">14"</td>
            <td>65</td>
            <td className="right-none">100</td>
          </tr>
          <tr>
            <td className="left-none bottom-none">16"</td>
            <td className="bottom-none">85</td>
            <td className="right-none bottom-none">130</td>
          </tr>
        </tbody>
      </table>
    </div>

    {/* Square cake serving size note */}
    <p className="serving-note">
      "Serving sizes are based on standard portions measuring 1.5 inches x 2
      inches, along with smaller coffee portions of approximately 1 inch x 2
      inches. Always plan for a little extra cake to ensure everyone gets a
      taste!"
    </p>
  </div>
);

export default SquareCakeServingGuide;
