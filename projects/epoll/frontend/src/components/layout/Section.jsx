import React from "react";

function Section({ title, eyebrow, children }) {
  return (
    <section className="section">
      {eyebrow && <div className="section-eyebrow">{eyebrow}</div>}
      <h2 className="section-title">{title}</h2>
      <div className="section-body">{children}</div>
    </section>
  );
}

export default Section;
