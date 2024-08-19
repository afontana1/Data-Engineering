import React from "react";
import { NavMenuCommonProps } from "./NavBarInterfaces";

const NavBarDropdown: React.FC<NavMenuCommonProps> = (props) => {
  React.useEffect(() => {
    function handleClickOutside(event: any) {
      if (
        props.wrapperRef.current &&
        !props.wrapperRef.current.contains(event.target) &&
        !props.isMobile
      ) {
        console.log("handle bg click");
        props.setIsShowing(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [props.wrapperRef, props.isMobile]);

  if (!props.isShowing || props.isMobile) {
    return null;
  }

  const items = [];
  for (let i = 0; i < props.items.length; i++) {
    const item = props.items[i];
    const element = (
      <div key={`navMenuItem${i}`}>
        <button
          onClick={() => {
            props.setIsShowing(false);
            item.action();
          }}
          className="block px-4 py-2 text-gray-700 hover:bg-gray-100 w-full text-left"
        >
          {item.label}
        </button>
      </div>
    );
    items.push(element);
  }

  const profileElement = (
    <div className="block px-4 py-2 text-gray-700 w-full text-left font-bold border-b mb-2 pb-3">
      {props.profileName}
    </div>
  );

  return (
    <div className="z-30 origin-top-right absolute right-0 top-16 w-72 p-2 rounded-md bg-white border border-black border-opacity-10 focus:outline-none">
      {profileElement}
      {items}
    </div>
  );
};

export default NavBarDropdown;
