import React from "react";

function ConceptCard({ title, children }) {
  return (
    <div className="concept-card">
      <h3>{title}</h3>
      <div className="concept-body">{children}</div>
    </div>
  );
}

export default ConceptCard;
