import { NavMenuCommonProps } from "./NavBarInterfaces";
import React from "react";

const NavBarPopupMenu: React.FC<NavMenuCommonProps> = (props) => {
  const onClick = (e: any) => {
    console.log("CLICKED BUTTON!");
    props.setIsShowing(!props.isShowing);
  };

  return (
    <div className="relative">
      <button
        type="button"
        className="w-8 h-8 bg-blue-700 rounded-full"
        onClick={onClick}
      ></button>
    </div>
  );
};

export default NavBarPopupMenu;
