import React, { useState, useEffect } from 'react';
import './ReviewSection.css';

const ReviewSection = ({ api }) => {
  const [reviews, setReviews] = useState([]);
  const [error, setError] = useState(null);  // Error state

  useEffect(() => {
    // Fetch reviews from the API using Axios
    api
      .get('/api/reviews/')
      .then((response) => {
        setReviews(response.data);  // Set the fetched reviews
      })
      .catch((error) => {
        console.error("Error fetching reviews:", error);
        setError(error.message);  // Set error state if API call fails
      });
  }, [api]);

  if (error) {
    return <div>Error loading reviews: {error}</div>;
  }

  return (
    <div className="review-section">
      <div className="reviews-wrapper">
        {reviews.map((review, index) => (
          <div key={index} className="review-card">
            <div className="name-and-stars">
              <h3 className="customer-name">{review.customer_name}</h3>
              <p className="stars">{'★'.repeat(review.stars)}</p>
            </div>
            <p className="review-description">{review.description}</p>
          </div>
        ))}
        {/* Duplicate reviews for the carousel effect */}
        {reviews.map((review, index) => (
          <div key={`dup-${index}`} className="review-card">
            <div className="name-and-stars">
              <h3 className="customer-name">{review.customer_name}</h3>
              <p className="stars">{'★'.repeat(review.stars)}</p>
            </div>
            <p className="review-description">{review.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ReviewSection;
