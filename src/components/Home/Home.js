import { useState } from 'react';

export default function Homepage() {
  // Function to handle navigation when clicking on dashboard images
  const handleNavigation = (path) => {
    // Using window.location for navigation
    window.location.href = path;
  };

  return (
    <div className="flex flex-col items-center w-full">
      {/* Navigation Menu */}
      <nav className="w-full flex justify-end p-4 space-x-4 text-sm">
        <a href="/" className="hover:underline">Home</a>
        <a href="/tutorials" className="hover:underline">Tutorials</a>
        <a href="/resources" className="hover:underline">Resources</a>
        <a href="/services" className="hover:underline">Services</a>
        <a href="/about-us/faq" className="hover:underline">About Us/FAQ</a>
        <a href="/login" className="hover:underline">Login</a>
        <a href="/signup" className="hover:underline">Signup</a>
      </nav>
      
      {/* Logo and Tagline */}
      <div className="flex items-center mt-4 mb-8">
        <div className="bg-purple-100 p-2 rounded mr-2">
          <span className="text-purple-800 text-2xl">L</span>
        </div>
        <div>
          <h1 className="text-4xl font-bold">LinkClick</h1>
          <p className="text-sm italic">simple & one step access for everyone</p>
        </div>
      </div>
      
      {/* Why LinkClick Section with Video */}
      <div className="w-full flex flex-col items-center my-8">
        <h2 className="text-2xl font-bold mb-4">Why LinkClick?</h2>
        <div className="flex justify-center">
          <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <polyline points="19 12 12 19 5 12"></polyline>
          </svg>
        </div>
        
        {/* Video Player with Placeholder */}
        <div className="mt-6 w-full max-w-3xl">
          {/* Replace with actual video element once you have the file */}
          <div className="w-full h-64 bg-gray-200 rounded shadow-lg flex items-center justify-center">
            <p className="text-gray-500">Video Player: linkclick_intro.mp4</p>
            <p className="text-red-500 text-sm absolute mt-16">
              (Check that video exists at /videos/linkclick_intro.mp4)
            </p>
          </div>
        </div>
      </div>
      
      {/* Dashboard Sections */}
      <div className="w-full max-w-3xl mt-16">
        {/* Tutorials Section */}
        <div className="flex items-center mb-12 bg-white rounded-lg shadow-md overflow-hidden cursor-pointer"
             onClick={() => handleNavigation('/tutorials')}>
          {/* Placeholder for missing image */}
          <div className="w-32 h-32 bg-gray-200 flex items-center justify-center">
            <span className="text-gray-400">Tutorials Image</span>
          </div>
          <div className="p-4">
            <h3 className="text-xl font-bold">Tutorials</h3>
            <p className="text-gray-600 text-sm">You've never made a website this fast before.</p>
            <button className="bg-gray-900 text-white px-3 py-1 rounded mt-2 text-sm">Learn More</button>
          </div>
        </div>
        
        {/* Services Section */}
        <div className="flex items-center mb-12 bg-white rounded-lg shadow-md overflow-hidden cursor-pointer"
             onClick={() => handleNavigation('/services')}>
          <div className="w-32 h-32 bg-gray-200 flex items-center justify-center">
            <span className="text-gray-400">Services Image</span>
          </div>
          <div className="p-4">
            <h3 className="text-xl font-bold">Services</h3>
            <p className="text-gray-600 text-sm">Explore our range of digital services.</p>
          </div>
        </div>
        
        {/* Notifications Section */}
        <div className="flex items-center mb-12 bg-white rounded-lg shadow-md overflow-hidden cursor-pointer"
             onClick={() => handleNavigation('/notifications')}>
          {/* Placeholder for missing image */}
          <div className="w-32 h-32 bg-gray-200 flex items-center justify-center">
            <span className="text-gray-400">Notifications Image</span>
          </div>
          <div className="p-4">
            <h3 className="text-xl font-bold">Notifications & Reminders</h3>
            <p className="text-gray-600 text-sm">Stay updated with important alerts.</p>
          </div>
        </div>
        
        {/* About Us Section */}
        <div className="mt-16 mb-10">
          <h2 className="text-2xl font-bold mb-4 text-center">About Us</h2>
          <p className="text-gray-700 text-center px-8 max-w-2xl mx-auto">
            LinkClick is a simple, senior-friendly digital support platform designed to simplify and centralize access to utility services. 
            It features push-to-call app navigation, QR scanning, billing, mobile bookings, and more.
          </p>
        </div>
        
        {/* FAQ Section */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold mb-4 text-center">FAQ</h2>
          <div className="bg-gray-100 p-6 rounded-lg max-w-2xl mx-auto">
            <div className="mb-3">
              <h3 className="font-bold">WHAT IS LINKCLICK?</h3>
              <p className="text-gray-600 text-sm mt-1">LinkClick is a simplified web platform for accessing essential services.</p>
            </div>
            <div className="mb-3">
              <h3 className="font-bold">WHO CAN USE LINKCLICK?</h3>
              <p className="text-gray-600 text-sm mt-1">Anyone looking for an easy way to access digital services.</p>
            </div>
            <div className="mb-3">
              <h3 className="font-bold">WHAT KIND OF SERVICES ARE COVERED ON LINKCLICK?</h3>
              <p className="text-gray-600 text-sm mt-1">Utilities, transportation, healthcare, and more.</p>
            </div>
            <div className="mb-3">
              <h3 className="font-bold">CAN I GET REMINDERS FOR PAYMENTS OR APPOINTMENTS?</h3>
              <p className="text-gray-600 text-sm mt-1">Yes, we offer customizable notification services.</p>
            </div>
            <div className="mb-3">
              <h3 className="font-bold">HOW CAN I STORE MY PAYMENT INFORMATION?</h3>
              <p className="text-gray-600 text-sm mt-1">Securely through our encrypted platform.</p>
            </div>
            <div className="mb-3">
              <h3 className="font-bold">DO I NEED TO SIGN IN EVERY TIME?</h3>
              <p className="text-gray-600 text-sm mt-1">No, you can enable "remember me" for quicker access.</p>
            </div>
            <div className="mb-3">
              <h3 className="font-bold">IS LINKCLICK FREE TO USE?</h3>
              <p className="text-gray-600 text-sm mt-1">Basic services are free, with premium features available.</p>
            </div>
            <div className="mb-3">
              <h3 className="font-bold">HOW DO I START USING LINKCLICK?</h3>
              <p className="text-gray-600 text-sm mt-1">Sign up for an account and follow our quick setup guide.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}