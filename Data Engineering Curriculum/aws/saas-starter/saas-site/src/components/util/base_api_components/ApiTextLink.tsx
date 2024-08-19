import { Link } from "gatsby";
import React from "react";

export interface ApiTextLinkProps {
  preLinkText?: string;
  justifyStyle?: string; // "[justify-center, justify-start...] https://tailwindcss.com/docs/justify-content"
  linkPath: string;
  linkText: string;
  isDisabled?: boolean;
}

export const ApiTextLink: React.FC<ApiTextLinkProps> = (props) => {
  const preTextElement = props.preLinkText ? (
    <div>{props.preLinkText}</div>
  ) : null;

  const justifyStyle: string = props.justifyStyle
    ? props.justifyStyle
    : "justify-center";

  const linkElement = props.isDisabled ? (
    <div className="text-blue-300">{props.linkText}</div>
  ) : (
    <Link to={props.linkPath} className="text-blue-600 hover:underline">
      {props.linkText}
    </Link>
  );

  return (
    <div className={`text-gray-600 text-sm flex space-x-1 ${justifyStyle}`}>
      {preTextElement}
      {linkElement}
    </div>
  );
};
