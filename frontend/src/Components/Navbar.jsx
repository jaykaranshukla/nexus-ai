import React from "react";

export const Navbar = () => {
  return (
    <nav className="navbar mx-auto w-3/4">
      <div className="flex bg-blue-500 border rounded-xl">
        <div className="img px-5 py-5">
          <span className="material-symbols-outlined">smart_toy</span>
        </div>
        <div className="flex flex-col">
            <div className="text-white text-2xl font-bold py-1">Nexus AI</div>
            <div className="text-white text-sm py-1">Online</div>
        </div>
      </div>
    </nav>
  );
};
