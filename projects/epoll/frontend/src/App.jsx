import React, { useState } from "react";
import Header from "./components/layout/Header";
import Nav from "./components/layout/Nav";
import Footer from "./components/layout/Footer";
import EpollPage from "./pages/EpollPage";
import KqueuePage from "./pages/KqueuePage";
import EventLoopPage from "./pages/EventLoopPage";

function App() {
  const [page, setPage] = useState("epoll");

  return (
    <div className="app">
      <Header />
      <Nav current={page} onChange={setPage} />
      <main className="content">
        {page === "epoll" && <EpollPage />}
        {page === "kqueue" && <KqueuePage />}
        {page === "eventloop" && <EventLoopPage />}
      </main>
      <Footer />
    </div>
  );
}

export default App;
