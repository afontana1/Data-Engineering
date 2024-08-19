import * as React from "react";
import AuthCommonComponent from "./AuthCommonComponent";
import {
  ApiButton,
  ApiStringField,
  ApiTextLink,
  withApiWrapper,
  SubComponentBaseProps,
} from "../../util/base_api_components/ApiComponents";
import { navigate } from "gatsby";
import * as AuthURL from "../route/AuthURL";
import { useContext } from "react";
import AuthContext from "../api/AuthContext";
import AuthResponse from "../api/AuthResponse";
import AuthApi from "../api/AuthApi";

const AuthSignIn: React.FC<SubComponentBaseProps> = (props) => {
  const auth = useContext(AuthContext);
  const emailField = ApiStringField.emailFromHook(
    React.useState(AuthApi.getDefaultUser())
  );

  const passwordField = ApiStringField.passwordFromHook(
    React.useState(AuthApi.getDefaultPassword())
  );

  const onSignInSuccess = (result: AuthResponse) => {
    props.onApiResponse(result);
    if (result.status == 200) {
      console.log("Sign In succeeded");
      navigate("/app/");
    }
  };

  const onSignIn = () => {
    console.log("Sign in with ", emailField.value, passwordField.value);
    props.onApiRequest();
    auth
      .signIn(emailField.value, passwordField.value)
      .then(onSignInSuccess)
      .catch(props.onApiFault);
  };

  const isDisabled: boolean = props.apiState.isBusy;

  const linkToRegister = (
    <div className="mt-4">
      <ApiTextLink
        isDisabled={isDisabled}
        preLinkText="Need an account?"
        linkText="Register"
        linkPath={AuthURL.REGISTER}
      />
    </div>
  );

  const linkToRecoverPassword = (
    <div className="-mt-4 mb-8">
      <ApiTextLink
        isDisabled={isDisabled}
        justifyStyle="justify-end"
        linkText="Forgot password?"
        linkPath={AuthURL.FORGOT_PASSWORD}
      />
    </div>
  );

  const linkToHome = (
    <div className="mt-4">
      <ApiTextLink
        isDisabled={isDisabled}
        linkText="Back"
        linkPath={AuthURL.HOME}
      />
    </div>
  );

  return (
    <div>
      <AuthCommonComponent header="Sign in." apiState={props.apiState}>
        {emailField.asComponent(isDisabled)}
        {passwordField.asComponent(isDisabled)}
        {linkToRecoverPassword}
        <ApiButton
          label="Sign In"
          onClick={onSignIn}
          isDisabled={isDisabled}
          isLoading={isDisabled}
        />
        {linkToRegister}
      </AuthCommonComponent>
      {linkToHome}
    </div>
  );
};

export default withApiWrapper(AuthSignIn);
