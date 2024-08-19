import { NavMenuCommonProps } from "./NavBarInterfaces";

import React from "react";

const NavMobileMenu: React.FC<NavMenuCommonProps> = (props) => {
  if (!props.isMobile || !props.isShowing) {
    return null;
  }

  const items = [];
  for (let i = 0; i < props.items.length; i++) {
    const item = props.items[i];
    const element = (
      <div
        key={`navMenuItem${i}`}
        className="first:border-t-0 border-t border-gray-200"
      >
        <button
          onClick={() => {
            props.wrapperRef.current.scrollTo(0, 0);
            item.action();
            props.setIsShowing(false);
          }}
          className="block py-3 text-gray-700 hover:bg-gray-100 w-full text-left"
        >
          {item.label}
        </button>
      </div>
    );
    items.push(element);
  }

  const profileElement = (
    <div className="block py-3 text-gray-700 w-full text-left">
      {props.profileName}
    </div>
  );

  return (
    <div className="bg-gray-50 px-4 py-2 border-t border-gray-100 font-bold">
      {profileElement}
      {items}
    </div>
  );
};

export default NavMobileMenu;
