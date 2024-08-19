import React from "react";
import AuthApi from "../api/AuthApi";
import AuthContext, { AuthApiContext } from "../api/AuthContext";
import { AuthStateUtility } from "../state/AuthState";

interface AuthProviderProps {
  children?: React.ReactNode;
}

const AuthProvider: React.FunctionComponent<AuthProviderProps> = (props) => {
  const [authState, setAuthState] = React.useState(
    new AuthStateUtility().state
  );

  const authApiContext: AuthApiContext = new AuthApiContext(
    authState,
    setAuthState
  );

  console.log("Reloaded with new Auth State");
  console.log(authState);

  React.useEffect(() => {
    if (!authState.hasToken && authState.firstLoad) {
      console.log("Loading state from browser.");
      const loadedAuthState = authApiContext.stateUtil.load();

      console.log("Checking if token is still valid.");
      const isTokenValid = AuthApi.verifyTokenAsBoolean(authState.token);
      if (isTokenValid) {
        console.log("Token is valid. Keeping.");
        setAuthState({ ...loadedAuthState, firstLoad: false });
      } else {
        console.log("Token is invalid. Voiding.");
        setAuthState(new AuthStateUtility(authState).withoutToken().state);
      }
    }
  }, []);

  return (
    <AuthContext.Provider value={authApiContext}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
