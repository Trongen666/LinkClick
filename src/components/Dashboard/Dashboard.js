import React from "react";
import { Helmet } from "react-helmet";

const Dashboard = () => {
  return (
    <div>
      <Helmet>
        <title>LinkClick Dashboard</title>
      </Helmet>
      <h2>Welcome to the Dashboard</h2>
      <p>Manage your services and settings here.</p>
    </div>
  );
};

export default Dashboard;
