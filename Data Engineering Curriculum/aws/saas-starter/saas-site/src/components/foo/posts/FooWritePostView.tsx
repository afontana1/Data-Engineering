import { navigate } from "gatsby";
import * as React from "react";
import * as AuthURL from "../../auth/route/AuthURL";
import { v4 as uuidv4 } from "uuid";
import AuthContext from "../../auth/api/AuthContext";
import { useContext } from "react";
import {
  SubComponentBaseProps,
  withApiWrapper,
} from "../../util/base_api_components/ApiComponents";
import { FooResponse } from "../api/FooResponse";
import FooApi from "../api/FooApi";
import withBoxStyling from "../../util/functions/withBoxStyling";

interface FooWritePostViewProps extends SubComponentBaseProps {
  setPostRefreshId?(x: string): void;
}

const PostEnabledView: React.FC<FooWritePostViewProps> = (props) => {
  const [postContent, setPostContent] = React.useState("");
  const [postSucceeded, setPostSucceeded] = React.useState(false);
  const auth = useContext(AuthContext);

  const onPostSuccess = (result: FooResponse) => {
    props.onApiResponse(result);
    if (result.status == 200) {
      console.log("Foo post succeeded!");
      setPostSucceeded(true);
      const randomId = uuidv4().replaceAll("-", "").substr(0, 12);
      props.setPostRefreshId(randomId);
    }
  };

  console.log("Foo post writer reloaded with token: " + auth.state.token);

  const onClickPost = () => {
    console.log("Foo Post with Content ", postContent);
    props.onApiRequest();
    FooApi.putPost("Untitled", postContent, auth.state.token)
      .then(onPostSuccess)
      .catch(props.onApiFault);
  };
  const isBusy = props.apiState.isBusy;
  const buttonLabel = isBusy ? (
    <div className="w-6 h-6 flex m-auto">
      <div className="loader" />
    </div>
  ) : (
    "Post"
  );

  let postContentElement;
  if (postSucceeded) {
    postContentElement = (
      <div className="text-center flex w-full bg-green-100 p-4 rounded-md">
        <div className="m-auto">
          <div className="text-green-800 mb-4">
            Post succeeded! Do you want to write another?
          </div>

          <button
            className="rounded-md bg-blue-600 text-white px-4 py-2 font-bold w-32"
            onClick={() => {
              setPostSucceeded(false);
              setPostContent("");
            }}
          >
            New Post
          </button>
        </div>
      </div>
    );
  } else {
    postContentElement = (
      <div>
        <textarea
          id="message"
          name="message"
          rows={2}
          className="shadow-sm focus:ring-blue-500 focus:border-blue-500 mt-1 block 
    w-full sm:text-sm border border-gray-300 rounded-md disabled:opacity-50
    p-2"
          placeholder="Write your message here..."
          defaultValue={postContent}
          onChange={(e) => {
            setPostContent(e.currentTarget.value);
          }}
          disabled={isBusy}
        ></textarea>
        <div className="mt-4 flex w-full">
          <div className="ml-auto my-auto">
            <button
              className="rounded-md bg-blue-600 text-white px-4 py-2 font-bold w-32 disabled:opacity-50"
              disabled={isBusy}
              onClick={onClickPost}
            >
              {buttonLabel}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return <div>{postContentElement}</div>;
};

const PostDisabledView: React.FC<FooWritePostViewProps> = (props) => {
  const goToSignIn = () => navigate(AuthURL.SIGN_IN);

  return (
    <div className="text-center flex w-full bg-gray-50 p-4 rounded-md">
      <div className="m-auto">
        <div className="text-gray-600 mb-4">You must be signed in to post.</div>

        <button
          className="rounded-md bg-blue-600 text-white px-4 py-2 font-bold w-32"
          onClick={goToSignIn}
        >
          Sign In
        </button>
      </div>
    </div>
  );
};
const FooWritePostView: React.FC<FooWritePostViewProps> = (props) => {
  const auth = useContext(AuthContext);
  const isSignedIn: boolean = auth.state.hasToken; //AuthApi.isSignedIn();
  const postView = isSignedIn ? (
    <PostEnabledView {...props} key="postEnabledView" />
  ) : (
    <PostDisabledView {...props} key="postDisabledView" />
  );

  return (
    <>
      <h1 className="text-xl font-bold mb-4">Write a post</h1>
      {postView}
    </>
  );
};

export default withBoxStyling(withApiWrapper(FooWritePostView));
