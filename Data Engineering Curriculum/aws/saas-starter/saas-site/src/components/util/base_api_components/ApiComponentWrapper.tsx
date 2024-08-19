import React, { FunctionComponent } from "react";
import ApiResponse from "../base/ApiResponse";
import { ApiState, ApiStateOverride, newApiState } from "./ApiState";

export interface SubComponentBaseProps {
  apiState: ApiState;
  setApiOverride(x: ApiStateOverride): void;
  onApiRequest(): void;
  onApiResponse(x: ApiResponse): void;
  onApiFault(x: any): void;
}

const ApiComponentWrapper = ({
  subComponent: FunctionComponent,
  path: string,
  ...rest
}) => {
  const [apiState, setApiState] = React.useState(newApiState());
  const setApiOverride = (override: ApiStateOverride) => {
    setApiState(newApiState(override));
  };

  const onApiRequest = () => {
    setApiOverride({ isBusy: true });
  };

  const onApiResponse = (response: ApiResponse) => {
    if (response.status == 200) {
      setApiOverride({ isBusy: false });
    } else {
      setApiOverride({
        hasError: true,
        errorMessage: response.message,
      });
    }
  };

  const onApiFault = (x: any) => {
    setApiOverride({
      hasError: true,
      errorMessage: `Something unexpected happened! [${x}]`,
    });
  };

  const subProps: SubComponentBaseProps = {
    apiState,
    setApiOverride,
    onApiRequest,
    onApiResponse,
    onApiFault,
  };

  return (
    <>
      <FunctionComponent<SubComponentBaseProps> {...rest} {...subProps} />
    </>
  );
};

export const withApiWrapper = (
  subComponent: FunctionComponent<SubComponentBaseProps>
) => ({ path: string, ...props }) => {
  return (
    <ApiComponentWrapper
      subComponent={subComponent}
      path={props.path}
      {...props}
    />
  );
};

export default ApiComponentWrapper;
