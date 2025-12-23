import React from "react";

function Header() {
  return (
    <header className="header">
      <h1>Networking Primitives: From epoll to Event Loops</h1>
      <p className="subtitle">
        A guided tour of how modern network servers watch many sockets at once,
        using <strong>epoll</strong>, <strong>kqueue</strong>, and a
        cooperative <strong>event loop</strong>.
      </p>
    </header>
  );
}

export default Header;
