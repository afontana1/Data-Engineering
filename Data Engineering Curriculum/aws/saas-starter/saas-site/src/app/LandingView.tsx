import * as React from "react";
import FooView from "../components/foo/FooView";
import FooPostGallery from "../components/foo/posts/FooPostGallery";
import FooWritePostView from "../components/foo/posts/FooWritePostView";

interface LandingProps {
  path: string;
}

const LandingView: React.FC<LandingProps> = (props) => {
  const [postRefreshId, setPostRefreshId] = React.useState("");

  return (
    <>
      <FooWritePostView setPostRefreshId={setPostRefreshId} />
      <FooPostGallery postRefreshId={postRefreshId} />
      <FooView />
    </>
  );
};

export default LandingView;
