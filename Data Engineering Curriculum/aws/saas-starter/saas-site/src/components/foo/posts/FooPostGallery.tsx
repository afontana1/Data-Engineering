import * as React from "react";
import {
  SubComponentBaseProps,
  withApiWrapper,
} from "../../util/base_api_components/ApiComponents";
import ApiRefresher from "../../util/base_api_components/ApiRefresher";
import withBoxStyling from "../../util/functions/withBoxStyling";
import FooApi from "../api/FooApi";
import { FooPost } from "../api/FooResponse";
import FooPostCard from "./FooPostCard";

interface FooPostGalleryProps extends SubComponentBaseProps {
  postRefreshId?: string;
}

const FooPostGallery: React.FC<FooPostGalleryProps> = (props) => {
  const [rawPosts, setRawPosts] = React.useState<FooPost[]>([]);

  const onClickRefresh = () => {
    refreshPosts();
  };

  const refreshPosts = () => {
    console.log("Refreshing Post for UUID: " + props.postRefreshId);
    let isMounted: boolean = true;
    props.onApiRequest();
    FooApi.getPosts()
      .then((r) => {
        if (isMounted) {
          console.log(r.items);
          setRawPosts(r.items);
          props.onApiResponse(r);
        }
      })
      .catch((r) => {
        if (isMounted) {
          console.log(r.items);
          props.onApiFault(r);
        }
      });

    return () => {
      isMounted = false;
    };
  };

  // Load the posts on page load.
  React.useEffect(refreshPosts, [props.postRefreshId]);

  let postsElement;
  const thereArePosts = rawPosts.length > 0;
  const posts = [];
  if (thereArePosts) {
    for (let i = 0; i < rawPosts.length; i++) {
      const rawPost = rawPosts[i];
      const newPost = (
        <FooPostCard
          title="Untitled"
          content={rawPost.content}
          author={rawPost.account_id.substr(0, 8)}
          key={rawPost.key}
          isLoading={false}
        />
      );
      posts.push(newPost);
    }
  } else {
    for (let i = 0; i < 5; i++) {
      const newPost = <FooPostCard isLoading={true} key={"postLoading" + i} />;
      posts.push(newPost);
    }
  }
  postsElement = <div>{posts}</div>;

  return (
    <>
      <div className="flex justify-between mb-4">
        <h1 className="text-xl font-bold my-auto">Recent Posts</h1>
        <ApiRefresher
          onClickRefresh={onClickRefresh}
          isRefreshing={props.apiState.isBusy}
        />
      </div>
      <div>{postsElement}</div>
    </>
  );
};

export default withBoxStyling(withApiWrapper(FooPostGallery));
