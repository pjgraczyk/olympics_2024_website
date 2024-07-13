import React from "react";

function Sidebar() {
  return (
    <div className="sidebar w-64 bg-gray-800 text-white p-4 transition-all duration-300 ease-in-out">
      <h1 className="text-2xl font-bold mb-8 p-10 olympic-logo">Olympic Games 2024</h1>
      <nav>
        <ul className="space-y-2 p-2 text-xl">
          <li>
            <a href="#" className="block py-2 px-4 text-indigo-200 hover:bg-indigo-700 hover:text-white rounded"> Dashboard </a>
          </li>
        </ul>
      </nav>
    </div>
  );
}

export default Sidebar;
