import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Menu, Home, Users, Calendar, TrendingUp, Medal } from 'lucide-react';
import Sidebar from '../components/Sidebar';

export default function DashboardLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navItems = [
    { name: 'Home', icon: Home, path: './pages/Home' },
    { name: 'Athletes', icon: Users, path: '/athletes' },
    { name: 'Events', icon: Calendar, path: '/events' },
    { name: 'Predictions', icon: TrendingUp, path: '/predictions' },
    { name: 'Medal Count', icon: Medal, path: '/medal-count' },
  ];

  return (
    <div className="flex h-screen w-screen bg-gray-100">
      {/* Sidebar */}
      <Sidebar />
      {/* Main Content */}
      <div className="flex flex-col overflow-hidden w-full">
        {/* Top bar */}
        <header className="bg-gradient-to-r from-blue-800 via-purple-500 to-black w-">
          <div className="flex items-center justify-between p-4 rounded-md">
            <button onClick={() => setSidebarOpen(true)} className="md:hidden">
              <Menu size={24} />
            </button>
            <h1 className="px-5 text-xl font-semibold olympic-logo">Olympics 2024 Dashboard</h1>
          </div>
        </header>
        {/* Page Content */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gradient-to-r via-purple-500 from-blue-800 to-black p-6 w-full">
          <Outlet />
        </main>
      </div>
    </div>
  );
};