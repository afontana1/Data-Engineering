import React from "react";
import { ApiState } from "../../util/base_api_components/ApiState";

const createErrorElement = (message: string) => {
  return (
    <div className="text-red-600 bg-red-100 p-3 border-red-600 mb-6 rounded-md text-sm">
      Error: {message}
    </div>
  );
};

const AuthCommonComponent: React.FC<{
  apiState: ApiState;
  header: string;
}> = (props) => {
  const errorElement = props.apiState.hasError
    ? createErrorElement(props.apiState.errorMessage)
    : null;

  return (
    <div className="bg-white md:px-8 md:py-12 px-4 py-8 border border-gray-300 rounded-md max-w-lg  m-2 md:m-auto mt-4 md:mt-8">
      <h1 className="text-2xl font-light mb-6 text-gray-700">{props.header}</h1>
      {errorElement}
      {props.children}
    </div>
  );
};

export default AuthCommonComponent;
