import { Router } from "@reach/router";
import React from "react";
import AuthRoute from "./AuthRoute";
import * as AuthViews from "../views/AuthViews";
import * as AuthURL from "../route/AuthURL";
import NavBar from "../../navbar/NavBar";

const AuthRouter: React.FunctionComponent<{ children?: React.ReactNode }> = (
  props
) => {
  return (
    <>
      <Router>
        <AuthRoute
          component={AuthViews.AuthRequestAccountVerification}
          path={AuthURL.VERIFY_ACCOUNT_REQUEST}
        />

        <AuthViews.AuthRegister path={AuthURL.REGISTER} />
        <AuthViews.AuthSignIn path={AuthURL.SIGN_IN} />
        <AuthViews.AuthForgotPassword path={AuthURL.FORGOT_PASSWORD} />
        <AuthViews.AuthResetPassword path={AuthURL.RESET_PASSWORD} />
        <AuthViews.AuthVerifyAccount path={AuthURL.VERIFY_ACCOUNT} />

        {props.children}
      </Router>
    </>
  );
};

export default AuthRouter;
