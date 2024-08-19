import * as React from "react";
import AuthApi from "../api/AuthApi";
import * as AuthURL from "../route/AuthURL";
import {
  ApiButton,
  ApiStringField,
  ApiTextLink,
  SubComponentBaseProps,
  withApiWrapper,
} from "../../util/base_api_components/ApiComponents";
import AuthCommonComponent from "./AuthCommonComponent";
import ApiResponse from "../../util/base_api/ApiResponse";

const AuthForgotPassword: React.FC<SubComponentBaseProps> = (props) => {
  const emailField = ApiStringField.fromHook("Email", React.useState(""));
  const [recoveryEmailSent, setRecoveryEmailSent] = React.useState(false);

  const onSuccess = (response: ApiResponse) => {
    console.log(response);
    props.onApiResponse(response);
    if (response.status === 200) {
      setRecoveryEmailSent(true);
    }
  };

  const onClick = () => {
    props.onApiRequest();
    console.log("Request account reset...");
    AuthApi.requestAccountReset(emailField.value)
      .then(onSuccess)
      .catch(props.onApiFault);
  };

  const isDisabled: boolean = props.apiState.isBusy || recoveryEmailSent;
  const instructions: string =
    "Enter your email and we'll send you instructions to recover your account.";
  let interactionElement = null;

  if (recoveryEmailSent) {
    interactionElement = (
      <div className="bg-green-50 border-green-300 border text-green-600 p-4 py-6 rounded-md">
        <div className="font-bold">Success!</div>{" "}
        <div className="text-sm">
          Please check your email for further instructions.
        </div>
      </div>
    );
  } else {
    interactionElement = (
      <ApiButton
        label="Send Recovery Link"
        onClick={onClick}
        isDisabled={isDisabled}
        isLoading={isDisabled}
      />
    );
  }

  return (
    <AuthCommonComponent
      header="Recover your account."
      apiState={props.apiState}
    >
      <div className="text-sm text-gray-500 mb-6">{instructions}</div>
      {emailField.asComponent(isDisabled)}
      {interactionElement}

      <div className="mt-4">
        <ApiTextLink linkPath={AuthURL.SIGN_IN} linkText="Back to Sign In" />
      </div>
    </AuthCommonComponent>
  );
};

export default withApiWrapper(AuthForgotPassword);
