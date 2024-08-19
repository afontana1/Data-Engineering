import * as React from "react";
import AuthApi from "../api/AuthApi";
import AuthCommonComponent from "./AuthCommonComponent";
import * as AuthURL from "../route/AuthURL";
import {
  ApiButton,
  ApiTextLink,
  SubComponentBaseProps,
  withApiWrapper,
} from "../../util/base_api_components/ApiComponents";
import ApiResponse from "../../util/base_api/ApiResponse";
import { useContext } from "react";
import AuthContext from "../api/AuthContext";

const AuthRequestAccountVerification: React.FC<SubComponentBaseProps> = (
  props
) => {
  const [verificationEmailSent, setVerificationEmailSent] = React.useState(
    false
  );
  const auth = useContext(AuthContext);

  const onSuccess = (response: ApiResponse) => {
    props.onApiResponse(response);
    if (response.status == 200) {
      setVerificationEmailSent(true);
    }
  };

  const onClick = () => {
    props.onApiRequest();
    AuthApi.requestAccountVerification(auth.stateUtil.payload.accountId)
      .then(onSuccess)
      .catch(props.onApiFault);
  };

  const resendInstructions: string = "Didn't receive it?";

  const isDisabled: boolean = props.apiState.isBusy || verificationEmailSent;
  let interactiveElement = null;

  if (!verificationEmailSent) {
    const actionButton = (
      <ApiButton
        label="Re-send Verification Email"
        onClick={onClick}
        isDisabled={isDisabled}
        isLoading={isDisabled}
      />
    );
    interactiveElement = (
      <div>
        <div className="mt-4 text-gray-400 -mb-2">{resendInstructions}</div>
        {actionButton}
      </div>
    );
  } else {
    const successPrompt = (
      <div className="bg-blue-50 border-blue-600 border text-blue-600 p-4 py-6 rounded-md mb-6">
        <div className="text-sm">
          Verification email has been sent! Please check your inbox.
        </div>
      </div>
    );
    interactiveElement = <div>{successPrompt}</div>;
  }

  return (
    <AuthCommonComponent
      header="Verify your account."
      apiState={props.apiState}
    >
      <div className="md:text-base text-sm text-gray-800 mb-6">
        <div className="font-semibold mb-2">
          You must verify your account before you can use it.
        </div>
        <div className="text-gray-600">
          An email has been sent to X with instructions on how to do this.
        </div>
      </div>
      {interactiveElement}
      <div className="mt-4">
        <ApiTextLink linkPath={AuthURL.HOME} linkText="Back" />
      </div>
    </AuthCommonComponent>
  );
};

export default withApiWrapper(AuthRequestAccountVerification);
