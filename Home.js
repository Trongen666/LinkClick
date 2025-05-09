// src/components/Homepage.js
import React from 'react';
import '../styles/home.css';

function Homepage() {
  // Function to handle navigation when clicking on dashboard images
  const handleNavigation = (path) => {
    window.location.href = path;
  };

  return (
    <div className="container">
      {/* Navigation Menu */}
      <nav className="nav-container">
        <a href="/" className="nav-link">Home</a>
        <a href="/tutorials" className="nav-link">Tutorials</a>
        <a href="/resources" className="nav-link">Resources</a>
        <a href="/services" className="nav-link">Services</a>
        <a href="/about-us/faq" className="nav-link">About Us/FAQ</a>
        <a href="/login" className="nav-link">Login</a>
        <a href="/signup" className="nav-link">Signup</a>
      </nav>
      
      {/* Logo and Tagline */}
      <div className="logo-container">
        <div className="logo-icon">
          <span className="logo-letter">L</span>
        </div>
        <div className="logo-text">
          <h1>LinkClick</h1>
          <p className="logo-tagline">simple & one step access for everyone</p>
        </div>
      </div>
      
      {/* Why LinkClick Section with Video */}
      <div className="why-section">
        <h2>Why LinkClick?</h2>
        <div className="down-arrow">
          <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <polyline points="19 12 12 19 5 12"></polyline>
          </svg>
        </div>
        
        {/* Video Player */}
        <div className="video-container">
          <video 
            controls 
            className="video-player"
            src="/vedios/linkclick_intro.mp4" // Path to your video in public folder
          >
            Your browser does not support the video tag.
          </video>
        </div>
      </div>
      
      {/* Dashboard Sections */}
      <div className="dashboard-section">
        {/* Tutorials Section */}
        <div className="dashboard-item" onClick={() => handleNavigation('/tutorials')}>
          <img 
            src="/images/tutorials.jpg" 
            alt="Older person using computer" 
            className="dashboard-item-image"
          />
          <div className="dashboard-item-content">
            <h3 className="dashboard-item-title">Tutorials</h3>
            <p className="dashboard-item-description">You've never made a website this fast before.</p>
            <button className="dashboard-item-button">Learn More</button>
          </div>
        </div>
        
        {/* Services Section */}
        <div className="dashboard-item" onClick={() => handleNavigation('/services')}>
          <div className="dashboard-item-image-placeholder">
            <span>Image</span>
          </div>
          <div className="dashboard-item-content">
            <h3 className="dashboard-item-title">Services</h3>
            <p className="dashboard-item-description">Explore our range of digital services.</p>
          </div>
        </div>
        
        {/* Notifications Section */}
        <div className="dashboard-item" onClick={() => handleNavigation('/notifications')}>
          <img 
            src="/images/notifications.jpg" 
            alt="Mobile notifications" 
            className="dashboard-item-image"
          />
          <div className="dashboard-item-content">
            <h3 className="dashboard-item-title">Notifications & Reminders</h3>
            <p className="dashboard-item-description">Stay updated with important alerts.</p>
          </div>
        </div>
        
        {/* About Us Section */}
        <div className="about-section">
          <h2>About Us</h2>
          <p className="about-text">
            LinkClick is a simple, senior-friendly digital support platform designed to simplify and centralize access to utility services. 
            It features push-to-call app navigation, QR scanning, billing, mobile bookings, and more.
          </p>
        </div>
        
        {/* FAQ Section */}
        <div className="faq-section">
          <h2>FAQ</h2>
          <div className="faq-container">
            <div className="faq-item">
              <h3 className="faq-question">WHAT IS LINKCLICK?</h3>
              <p className="faq-answer">LinkClick is a simplified web platform for accessing essential services.</p>
            </div>
            <div className="faq-item">
              <h3 className="faq-question">WHO CAN USE LINKCLICK?</h3>
              <p className="faq-answer">Anyone looking for an easy way to access digital services.</p>
            </div>
            <div className="faq-item">
              <h3 className="faq-question">WHAT KIND OF SERVICES ARE COVERED ON LINKCLICK?</h3>
              <p className="faq-answer">Utilities, transportation, healthcare, and more.</p>
            </div>
            <div className="faq-item">
              <h3 className="faq-question">CAN I GET REMINDERS FOR PAYMENTS OR APPOINTMENTS?</h3>
              <p className="faq-answer">Yes, we offer customizable notification services.</p>
            </div>
            <div className="faq-item">
              <h3 className="faq-question">HOW CAN I STORE MY PAYMENT INFORMATION?</h3>
              <p className="faq-answer">Securely through our encrypted platform.</p>
            </div>
            <div className="faq-item">
              <h3 className="faq-question">DO I NEED TO SIGN IN EVERY TIME?</h3>
              <p className="faq-answer">No, you can enable "remember me" for quicker access.</p>
            </div>
            <div className="faq-item">
              <h3 className="faq-question">IS LINKCLICK FREE TO USE?</h3>
              <p className="faq-answer">Basic services are free, with premium features available.</p>
            </div>
            <div className="faq-item">
              <h3 className="faq-question">HOW DO I START USING LINKCLICK?</h3>
              <p className="faq-answer">Sign up for an account and follow our quick setup guide.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Homepage;