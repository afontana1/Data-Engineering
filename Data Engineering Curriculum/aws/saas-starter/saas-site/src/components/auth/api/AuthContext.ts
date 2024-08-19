import React from "react";
import AuthApi from "./AuthApi";
import AuthResponse from "./AuthResponse";
import { AuthState, AuthStateUtility } from "../state/AuthState";
import withSideEffect from "../../util/functions/withSideEffect";

export class AuthApiContext {
  public readonly stateUtil: AuthStateUtility;
  private readonly setState: (x: AuthState) => void;
  public readonly state: AuthState;

  constructor(state?: AuthState, setState?: (x: AuthState) => void) {
    this.stateUtil = new AuthStateUtility(state);
    this.setState = setState;
    this.state = state;
  }

  public getState(): AuthState {
    return this.stateUtil.state;
  }

  public signIn(email: string, password: string): Promise<AuthResponse> {
    return withSideEffect(AuthApi.signIn(email, password), (x) => {
      const newState = this.stateUtil.withToken(x.token).save();
      this.setState(newState);
    });
  }

  public signUp(email: string, password: string): Promise<AuthResponse> {
    return withSideEffect(AuthApi.signUp(email, password), (x) => {
      const newState = this.stateUtil.withToken(x.token).save();
      this.setState(newState);
    });
  }

  public signOut(): void {
    this.stateUtil.clear();
    this.setState(this.stateUtil.newDefaultState());
  }
}

const AuthContext = React.createContext<AuthApiContext>(
  new AuthApiContext(new AuthStateUtility().newDefaultState())
);
export default AuthContext;
