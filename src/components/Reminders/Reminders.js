import React, { useState } from 'react';
import '../../App.css'; // Assuming you have a CSS file for styles

const ReminderAndNotification = () => {
  const [reminders, setReminders] = useState([]);
  const [newReminder, setNewReminder] = useState('');

  const notifications = [
    "Medicine",
    "Drink water",
    "Pension status update",
    "Bank visit",
    "Bill payments",
    "Eye check-up",
    "Booking confirmation"
  ];

  const handleAddReminder = () => {
    if (newReminder.trim()) {
      setReminders([...reminders, newReminder]);
      setNewReminder('');
    }
  };

  return (
    <div className="container">
      <h1 className="title">🧭 Reminders and Notifications</h1>

      <div className="section">
        <h2>🔔 Reminders</h2>
        <div style={{ display: 'flex', gap: '8px', marginBottom: '10px' }}>
          <input
            type="text"
            value={newReminder}
            onChange={(e) => setNewReminder(e.target.value)}
            placeholder="Add reminder..."
          />
          <button onClick={handleAddReminder}>+</button>
        </div>
        <ul>
          {reminders.map((reminder, index) => (
            <li key={index}>
              {reminder} 🔔
            </li>
          ))}
        </ul>
      </div>

      <div className="section">
        <h2>🔔 Notifications</h2>
        <ul>
          {notifications.map((notification, index) => (
            <li key={index}>
              <input type="checkbox" />
              {notification}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ReminderAndNotification;

