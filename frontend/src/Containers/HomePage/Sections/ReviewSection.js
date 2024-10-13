// ReviewSection.js
import React from 'react';
import './ReviewSection.css';

const ReviewSection = () => {
  const reviews = [
    {
      customerName: 'Dawn',
      stars: 5,
      description: 'This business is above and beyond! They catered for all my demanding needs in such a short time! They managed to organise my gluten free engagement cake in about a week or less and were very approachable and reliable. The cake tastes very delicious and looks really good too! Very affordable too. Will definitely reach out again. Keep it up guys you are amazing x'
    },
    {
      customerName: 'Maisie',
      stars: 5,
      description: 'We have purchased many cakes from Magnolia cakes, and they always exceed all our expectations! Their filling are delicious and designs always gorgeous, Maggie is very professional and meticulous when she makes her cakes. We have no hesitation recommending anyone to go there.'
    },
    {
      customerName: 'Mourisha',
      stars: 5,
      description: 'I just happen to try their cupcakes as a friend of mine suggested. To my surprise Maggie did an awesome job with the way they were made to taste less sweet and kid friendly. She sure scored with her buttercream and the toppings. We all enjoyed the combination of the salted caramel frosting and the soft spongy chocolate cupcake. 😍😍 They were super yummy I could still remember the taste of them while giving typing this 😋 Such finesse 😊'
    },
    {
        customerName: 'Saeed',
        stars: 5,
        description: 'Beautifully made custom cake and great customer service. So glad with my order, tasted so fresh and will definitely come back again! Highly recommended'
    }
  ];

  return (
    <div className="review-section">
      <div className="reviews-wrapper">
        {/* Render the reviews twice to create a seamless loop */}
        {reviews.map((review, index) => (
          <div key={index} className="review-card">
            <div className="name-and-stars">
              <h3 className="customer-name">{review.customerName}</h3>
              <p className="stars">{'★'.repeat(review.stars)}</p>
            </div>
            <p className="review-description">{review.description}</p>
          </div>
        ))}
        {/* Duplicate reviews */}
        {reviews.map((review, index) => (
          <div key={`dup-${index}`} className="review-card">
            <div className="name-and-stars">
              <h3 className="customer-name">{review.customerName}</h3>
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