import React, { useEffect, useState } from 'react';
import './FooterSection.css';
import ShopMap from "Components/ShopMap/ShopMap";

// SocialMediaLink component to handle individual social media links with images
const SocialMediaLink = ({ socialMedia, account_name, account_link }) => {
  const getIcon = (platform) => {
    switch (platform.toLowerCase()) {
      case 'facebook':
        return '/images/fb-icon.png';
      case 'instagram':
        return '/images/insta-icon.png';
      default:
        return '';
    }
  };

  return (
    <div className="social-media-link">
      <img src={getIcon(socialMedia)} alt={`${socialMedia} icon`} className="social-icon" />
      <a href={account_link} target="_blank" rel="noopener noreferrer" className="social-link">
        {account_name}
      </a>
    </div>
  );
};

const FooterSection = ({ api }) => {
  const [location, setLocation] = useState({
    section_heading: "OUR LOCATION",
    location_address: "Melbourne, VIC 3752",
  });
  const [contactInfo, setContactInfo] = useState({
    section_heading: "CONTACT US",
  });
  const [businessHrs, setBusinessHrs] = useState([]);
  const [socialMedias, setSocialMedias] = useState([]);

  useEffect(() => {
    // Fetch business location
    api
      .get("/api/footer-location/")
      .then((response) => {
        setLocation(response.data);
      })
      .catch((error) => console.error("Error fetching location:", error));

    // Fetch contact information
    api
      .get("/api/footer-contact-us/")
      .then((response) => {
        setContactInfo(response.data);
      })
      .catch((error) => console.error("Error fetching contact info:", error));

    // Fetch business hours
    api
      .get("/api/footer-business-hrs/")
      .then((response) => {
        setBusinessHrs(response.data.business_hrs_info.split('\n')); // Split into an array by line
      })
      .catch((error) => console.error("Error fetching business hours:", error));

    // Fetch social media information
    api
      .get("/api/social-medias/")
      .then((response) => {
        setSocialMedias(response.data);
      })
      .catch((error) => console.error("Error fetching social media info:", error));
  }, [api]);

  return (
    <footer className="footer-container">
      <div className="footer-content">
        <div className="footer-column">
          <h4>Shop</h4>
          <ul>
            <li><a href="https://magnoliacake.com.au/online-store" target="_blank" rel="noopener noreferrer">Store</a></li>
            <li><a href="https://magnoliacake.com.au/workshop" target="_blank" rel="noopener noreferrer">Workshop classes</a></li>
            <li><a href="https://magnoliacake.com.au/flavours-and-servings" target="_blank" rel="noopener noreferrer">Flavours & Servings</a></li>
          </ul>
        </div>
        <div className="footer-column">
          <h4>{contactInfo.section_heading}</h4>
          <ul>
            <li><a href="https://magnoliacake.com.au/contact-us" target="_blank" rel="noopener noreferrer">Contact us</a></li>
            <li><a href="https://magnoliacake.com.au/get-a-quote" target="_blank" rel="noopener noreferrer">Get a quote</a></li>
            <li><a href="https://magnoliacake.com.au/faq" target="_blank" rel="noopener noreferrer">Faq</a></li>
          </ul>
        </div>
        <div className="footer-column">
          <h4>{location.section_heading}</h4>
          <p>{location.location_address}</p>
        </div>
        <div className="footer-column">
          <h4>Follow us:</h4>
          <div className="social-medias">
            {socialMedias.map((platform) => (
              <SocialMediaLink
                key={platform.id}
                socialMedia={platform.social_media_platform}
                account_name={platform.account_name}
                account_link={platform.account_link}
              />
            ))}
          </div>
        </div>
        <div className="footer-column">
          <h4>Opening Hours:</h4>
          <div className="business-hours">
            {businessHrs.map((info, index) => (
              <p key={index}>{info}</p>
            ))}
          </div>
          <ShopMap /> {/* Restored ShopMap component */}
        </div>
      </div>
      <div className="footer-bottom">
        <p>
          Email: contact@magnoliacake.com.au &nbsp;&nbsp;
          Phone: 0422-733-882 &nbsp;&nbsp;
          <a href="https://magnoliacake.com.au/terms-and-conditions" target="_blank" rel="noopener noreferrer">Terms and conditions</a> &nbsp;&nbsp;
          ABN 50910846907
        </p>
        <p>Copyright © 2024 Magnolia Cakes and Cupcakes</p>
      </div>
    </footer>
  );
};

export default FooterSection;
