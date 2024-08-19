import * as jwt from "jsonwebtoken";

const TOKEN_USER_EMAIL_PROPERTY: string = "email";
const TOKEN_ACCOUNT_ID_PROPERTY: string = "account_id";

export interface AuthTokenPayload {
  userEmail?: string;
  accountId?: string;
}

export const getPayloadFromToken = (token: string) => {
  const rawPayload = jwt.decode(token);
  if (rawPayload === null) {
    throw new Error("Unable to decode user token.");
  } else {
    const payload: AuthTokenPayload = {
      userEmail: valueFromPayload(
        rawPayload,
        TOKEN_USER_EMAIL_PROPERTY,
        undefined
      ),
      accountId: valueFromPayload(
        rawPayload,
        TOKEN_ACCOUNT_ID_PROPERTY,
        undefined
      ),
    };
    return payload;
  }
};

const valueFromPayload = (payload: any, key: string, defaultValue: any) => {
  return payload.hasOwnProperty(key) ? payload[key] : defaultValue;
};
