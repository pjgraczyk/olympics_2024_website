import React from "react";
import Sidebar from "./components/Sidebar";
import MainContent from "./components/MainContent";

const App = () => {
  return (
  <div className="flex h-screen w-screen">
    <Sidebar />
    <MainContent />
  </div>
  );
};

export default App;
