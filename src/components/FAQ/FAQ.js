import React from "react";
import { Helmet } from "react-helmet";

const FAQ = () => {
  return (
    <div>
      <Helmet>
        <title>LinkClick FAQ</title>
      </Helmet>
      <h2>Frequently Asked Questions</h2>
      <div>
        <h4>What is LinkClick?</h4>
        <p>LinkClick is a digital support platform...</p>

        <h4>Who can use LinkClick?</h4>
        <p>Anyone who needs assistance navigating online services.</p>

        <h4>What tutorials are available?</h4>
        <p>We provide easy guides for WhatsApp, Netflix, Zoom, and more.</p>
      </div>
    </div>
  );
};

export default FAQ;
