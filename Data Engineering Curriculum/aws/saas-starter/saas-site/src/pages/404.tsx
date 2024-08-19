import { Link } from "gatsby";
import * as React from "react";
import useRenderKey from "../components/util/functions/useRenderKey";
import Layout from "../layout/Layout";

interface PageNotFoundProps {
  default?: boolean;
}

const PageNotFound: React.FC<PageNotFoundProps> = (props) => {
  const [isMounted, setIsMounted] = React.useState(false);
  // const renderKey = useRenderKey();

  React.useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return null;
  } else {
    return (
      <div>
        <Layout>
          <div className="bg-white rounded-md p-6 w-full">
            <h1 className="text-2xl font-bold mb-4">Page Not Found</h1>
            <p className="text-gray-700">
              Sorry, I couldn't find the page you're looking for. Are you sure
              this is the right address?
            </p>
            <div className="flex mt-8">
              <Link
                to={"/"}
                className="text-white font-bold bg-blue-600 rounded-md py-2 px-6 mx-auto"
              >
                Home
              </Link>
            </div>
          </div>
        </Layout>
      </div>
    );
  }
};

export default PageNotFound;
