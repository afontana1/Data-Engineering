import React from "react";

function Nav({ current, onChange }) {
  const tabs = [
    { id: "epoll", label: "1. epoll + RB-tree" },
    { id: "kqueue", label: "2. kqueue" },
    { id: "eventloop", label: "3. Event loop" },
  ];

  return (
    <nav className="nav">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          className={
            "nav-tab" + (current === tab.id ? " nav-tab--active" : "")
          }
          onClick={() => onChange(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </nav>
  );
}

export default Nav;
