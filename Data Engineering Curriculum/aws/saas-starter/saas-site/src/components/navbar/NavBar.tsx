import { Link, navigate } from "gatsby";
import React, { useContext, useRef } from "react";
import AuthContext, { AuthApiContext } from "../auth/api/AuthContext";
import * as AuthURL from "../auth/route/AuthURL";
import useRenderKey from "../util/functions/useRenderKey";
import NavBarDropdown from "./NavBarDropdown";
import { NavMenuCommonProps } from "./NavBarInterfaces";
import NavBarPopupMenu from "./NavBarPopupMenu";
import NavMobileMenu from "./NavMobileMenu";

interface NavBarProps {
  location?: any;
}

function getWindowDimensions() {
  const { innerWidth: width, innerHeight: height } =
    typeof window !== "undefined"
      ? window
      : { innerWidth: 100, innerHeight: 100 };
  return {
    windowWidth: width,
    windowHeight: height,
  };
}

function useWindowDimensions() {
  const [windowDimensions, setWindowDimensions] = React.useState(
    getWindowDimensions()
  );

  React.useEffect(() => {
    function handleResize() {
      setWindowDimensions(getWindowDimensions());
    }

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return windowDimensions;
}

const NavBar: React.FC<NavBarProps> = (props) => {
  const renderKey = useRenderKey();
  const auth = useContext(AuthContext);
  const siteTitle = <div className="my-auto">SaaS</div>;
  const isSignedIn = auth.state.hasToken; //AuthApi.isSignedIn();
  const wrapperRef = useRef(null);
  const [isShowing, setIsShowing] = React.useState(false);

  let interactiveNavElement = null;
  let mobileNavElement = null;

  const navCommonProps = getNavBarCommonAttributes(
    wrapperRef,
    isShowing,
    setIsShowing,
    auth
  );

  const navProfileElement = <NavBarProfileElement {...navCommonProps} />;
  const navMobileElement = <NavMobileMenu {...navCommonProps} />;
  const navSignInElement = <NavBarSignInElement />;

  if (isSignedIn) {
    interactiveNavElement = navProfileElement;
    mobileNavElement = navMobileElement;
  } else {
    interactiveNavElement = navSignInElement;
  }

  let shouldExcludeNavBar = false;

  if (props.location) {
    AuthURL.EXCLUDE_NAV_BAR.forEach((excludePath) => {
      const matchResult = props.location.pathname.match(excludePath);
      if (matchResult) {
        shouldExcludeNavBar = true;
      }
    });
  }

  console.log("Should exclude: " + shouldExcludeNavBar);

  if (shouldExcludeNavBar) {
    return <div key={renderKey.key}></div>;
  } else {
    return (
      <div key={renderKey.key}>
        <div className="mb-2 md:mb-4">
          <div className="rounded-md  bg-white p-4 pt-4 pb-4 md:p-4 flex w-full">
            <div className="flex justify-between m-auto w-full max-w-4xl">
              {siteTitle}
              <div className="relative" ref={wrapperRef}>
                {interactiveNavElement}
              </div>
            </div>
          </div>
          {mobileNavElement}
        </div>
      </div>
    );
  }
};

const getNavBarCommonAttributes = (
  wrapperRef,
  isShowing,
  setIsShowing,
  auth: AuthApiContext
) => {
  const profileName = auth.stateUtil.payload.userEmail;
  const { windowWidth, windowHeight } = useWindowDimensions();
  const isMobileSize = windowWidth <= 640;
  const navCommonProps: NavMenuCommonProps = {
    isShowing,
    setIsShowing,
    wrapperRef,
    isMobile: isMobileSize,
    profileName: profileName,
    items: [
      { label: "Dashboard", action: () => navigate("/app/") },
      { label: "Profile", action: () => navigate("/app/profile") },
      {
        label: "Sign Out",
        action: () => {
          auth.signOut();
          navigate("/app/");
        },
      },
    ],
  };
  return navCommonProps;
};

const NavBarProfileElement = (props: NavMenuCommonProps) => {
  return (
    <>
      <NavBarPopupMenu {...props} />
      <NavBarDropdown {...props} />
    </>
  );
};

const NavBarSignInElement = (props) => {
  return (
    <div className=" px-2 py-1 text-sm font-bold rounded-md border border-blue-500">
      <Link to={AuthURL.SIGN_IN} className="text-blue-600 hover:underline">
        Sign In
      </Link>
    </div>
  );
};

export default NavBar;
