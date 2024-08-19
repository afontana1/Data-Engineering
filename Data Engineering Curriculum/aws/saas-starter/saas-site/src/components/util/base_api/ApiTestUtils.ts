import AuthApi from "../../auth/api/AuthApi";
import AuthResponse from "../../auth/api/AuthResponse";
import { v4 as uuidv4 } from "uuid";
import * as dotenv from "dotenv";
dotenv.config({ path: ".env.development" });

export const createAndSignInToVerifiedAccount = async (
  isMember: boolean = false
) => {
  const user: string = newRandomUser();
  const password: string = newRandomPassword();
  await signUpAndExpect(user, password, 200, true, isMember);
  return await signInAndExpect(user, password, 200);
};

export const signUpAndExpect = async (
  user: string,
  password: string,
  expectedCode: number,
  isVerified?: boolean,
  isMember?: boolean
) => {
  const response = await AuthApi.signUp(user, password, isVerified, isMember);
  return expectResponseOrPrint(response, expectedCode);
};

export const signInAndExpect = async (
  user: string,
  password: string,
  expectedCode: number
) => {
  const response = await AuthApi.signIn(user, password);
  return expectResponseOrPrint(response, expectedCode);
};

export const expectResponseOrPrint = (
  response: AuthResponse,
  expectedCode: number
) => {
  if (response.status !== expectedCode) {
    console.log("Response Message", response.message);
    console.log("Response Payload", response.payload);
  }
  expect(response.status).toBe(expectedCode);

  return response;
};

export const randomUUID = () => {
  return uuidv4().replaceAll("-", "").substr(0, 12);
};

export const newRandomUser = () => {
  return `test-user-1aA${randomUUID()}@bonestack.com`;
};

export const newRandomPassword = () => {
  return `password-1aA${randomUUID()}`;
};
