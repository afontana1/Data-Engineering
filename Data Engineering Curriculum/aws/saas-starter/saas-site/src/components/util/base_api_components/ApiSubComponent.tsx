import React from "react";
import { SubComponentBaseProps, withApiWrapper } from "./ApiComponentWrapper";

const ApiSubComponent: React.FC<SubComponentBaseProps> = (props) => {
  const onClick = () => {
    props.setApiOverride({ isBusy: true });
  };

  console.log(props.apiState);

  return (
    <div>
      I'm an Api Subcomponent! My key is: {1}
      <button onClick={onClick}>Click me</button>
      Is busy: {props.apiState.isBusy.toString()}
    </div>
  );
};

export const WrappedApiSubComponent = withApiWrapper(ApiSubComponent);
