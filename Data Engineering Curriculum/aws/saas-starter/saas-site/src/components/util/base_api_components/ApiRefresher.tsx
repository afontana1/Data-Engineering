import * as React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSyncAlt } from "@fortawesome/free-solid-svg-icons";

interface ApiRefresherProps {
  isRefreshing: boolean;
  onClickRefresh: React.MouseEventHandler<HTMLButtonElement>;
}

const ApiRefresher: React.FC<ApiRefresherProps> = (props) => {
  let displayableElement: {};

  if (props.isRefreshing) {
    displayableElement = (
      <div>
        <div className="w-7 h-7 flex">
          <div className="loader-dark" />
        </div>
      </div>
    );
  } else {
    displayableElement = (
      <button onClick={props.onClickRefresh}>
        <FontAwesomeIcon className="fa-lg text-gray-400" icon={faSyncAlt} />
      </button>
    );
  }

  return <div className="my-auto">{displayableElement}</div>;
};

export default ApiRefresher;
