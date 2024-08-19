import StateUtility from "../../util/state/StateUtility";
import { AuthTokenPayload, getPayloadFromToken } from "./AuthTokenPayload";

export interface AuthState {
  hasToken: boolean;
  firstLoad: boolean;
  token?: string;
}

export class AuthStateUtility extends StateUtility<AuthState> {
  public readonly payload: AuthTokenPayload;

  constructor(state?: AuthState) {
    super(state);

    if (state && state.token) {
      this.payload = getPayloadFromToken(state.token);
    } else {
      this.payload = {};
    }
  }

  public newDefaultState(): AuthState {
    return {
      hasToken: false,
      firstLoad: true,
    };
  }

  public deserialize(x: any): AuthState {
    const newState: AuthState = {
      ...this.newDefaultState(),
      token: x.token,
      hasToken: x.token ? true : false,
    };
    return newState;
  }

  public serialize(): string {
    return JSON.stringify({ token: this.state.token });
  }

  public withToken(token: string): AuthStateUtility {
    const newRawState: AuthState = {
      ...this.state,
      hasToken: token ? true : false,
      token: token,
    };
    return new AuthStateUtility(newRawState);
  }

  public withoutToken(): AuthStateUtility {
    return this.withToken(undefined);
  }
}
