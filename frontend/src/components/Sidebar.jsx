import React from "react";
import { useState } from "react";
import { Link } from "react-router-dom";
import { X, Home, Users, Calendar, TrendingUp, Medal } from "lucide-react";
import OlympicsLogo from "../assets/logos/olympics.svg";

function Sidebar() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navItems = [
    { name: "Home", icon: Home, path: "/" },
    { name: "Athletes", icon: Users, path: "/athletes" },
    { name: "Events", icon: Calendar, path: "/events" },
    { name: "Predictions", icon: TrendingUp, path: "/predictions" },
    { name: "Medal Count", icon: Medal, path: "/medal-count" },
  ];

  return (
    <div
      className={`bg-blue-800 border-l-blue-900 text-white w-64 space-y-6 py-7 px-2 absolute inset-y-0 left-0 transform ${
        sidebarOpen ? "translate-x-0" : "-translate-x-full"
      } md:relative md:translate-x-0 transition duration-200 ease-in-out`}
    >
      <img src={OlympicsLogo} alt="Olympic Logo" className="w-auto h-auto px-5 pr-20" />
      <div className="flex items-center justify-between px-4">
        <h2 className="text-2xl font-bold mb-5 p-2 olympic-logo ">
          Olympic Games 2024
        </h2>
        <button onClick={() => setSidebarOpen(false)} className="md:hidden">
          <X size={24} />
        </button>
      </div>
      <nav>
        {navItems.map((item) => (
          <Link
            key={item.name}
            to={item.path}
            className="py-2.5 px-4 rounded transition duration-200 hover:bg-blue-700 flex items-center"
          >
            <item.icon size={20} className="mr-2" />
            {item.name}
          </Link>
        ))}
      </nav>
    </div>
  );
}

export default Sidebar;
