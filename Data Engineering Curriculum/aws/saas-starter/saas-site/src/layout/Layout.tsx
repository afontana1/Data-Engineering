import React from "react";
import { Helmet } from "react-helmet";
import useRenderKey from "../components/util/functions/useRenderKey";

interface LayoutProps {
  children?: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = (props) => {
  const renderKey = useRenderKey();

  const serviceTitle: string = process.env["GATSBY_SERVICE_NAME"];

  return (
    <div>
      <Helmet>
        <title>{serviceTitle}</title>
        <meta name="description" content="Boilerplate SaaS application." />
      </Helmet>
      <div className="p-2 md:p-4" key={renderKey.key}>
        <div className="max-w-4xl m-auto">{props.children}</div>
      </div>
    </div>
  );
};

export default Layout;
