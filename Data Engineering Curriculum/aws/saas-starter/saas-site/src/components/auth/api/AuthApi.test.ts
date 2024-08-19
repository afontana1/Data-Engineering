import AuthApi from "./AuthApi";
import axios from "axios";
import {
  createAndSignInToVerifiedAccount,
  expectResponseOrPrint,
  newRandomPassword,
  newRandomUser,
  signInAndExpect,
  signUpAndExpect,
} from "../../util/base_api/ApiTestUtils";
import { getPayloadFromToken } from "../state/AuthTokenPayload";

beforeEach(async () => {
  // HTTP Adapter required to solve CORS error.
  axios.defaults.adapter = require("axios/lib/adapters/http");
  console.log("Preparing for new test.");
  console.log("Clearing AuthApi state.");

  // Set the timeout.
  jest.setTimeout(45000);
});

test("auth positive login", async () => {
  // User can register, login, and validate their session.
  const user: string = newRandomUser();
  const password: string = newRandomPassword();
  await signUpAndExpect(user, password, 200);
  const signInResponse = await signInAndExpect(user, password, 200);

  // Token verification should succeed.
  const verificationResponse = await AuthApi.verifyToken(signInResponse.token);
  expect(verificationResponse.status).toBe(200);
});

test("auth login account not verified", async () => {
  const user: string = newRandomUser();
  const password: string = newRandomPassword();
  await signUpAndExpect(user, password, 200);
  const signInResponse = await signInAndExpect(user, password, 200);

  // Token should exist, and have the 'confirmed' status as false.
  const isAccountVerified = await AuthApi.getAccountVerificationStatusAsBoolean(
    signInResponse.token
  );
  expect(isAccountVerified).toBe(false);
});

test("verification with bad token fails", async () => {
  const response = await AuthApi.verifyToken("badToken");
  expect(response.status).toBe(401);
});

test("can verify account", async () => {
  // // Validation should fail without a session.
  const user: string = newRandomUser();
  const password: string = newRandomPassword();
  const signUpResponse = await signUpAndExpect(user, password, 200);
  console.log(signUpResponse);

  // The account key should now exist in our session.
  const tokenPayload = getPayloadFromToken(signUpResponse.token);
  const accountId = tokenPayload.accountId;

  // // Should be able to request validation email.
  const response = await requestAccountVerificationAndExpect(accountId, 200);
  expect(response.payload).toHaveProperty("verification_token");
  const verificationToken = response.payload["verification_token"];

  // Can verify account with the key.
  const verificationResult = await verifyAccountAndExpect(
    verificationToken,
    200
  );
  console.log(verificationResult);
});

test("can reset account", async () => {
  // I should be able to reset my password.
  const email: string = newRandomUser();
  const oldPassword: string = newRandomPassword();
  const newPassword: string = newRandomPassword();
  await signUpAndExpect(email, oldPassword, 200);

  // Request password reset.
  const resetRequestResponse = await requestAccountResetAndExpect(email, 200);

  // Reset the password
  console.log(resetRequestResponse.payload);
  expect(resetRequestResponse.payload).toHaveProperty("reset_token");
  const resetToken = resetRequestResponse.payload["reset_token"];
  await resetAccountAndExpect(resetToken, newPassword, 200);

  // Cannot sign in with old password.
  await signInAndExpect(email, oldPassword, 401);

  // Can sign in with new password.
  await signInAndExpect(email, newPassword, 200);
});

test("premium not signed in", async () => {
  const response = await AuthApi.verifyPremiumStatus("badToken");
  expect(response.status).toBe(401);
});

test("premium not a member", async () => {
  const signInResponse = await createAndSignInToVerifiedAccount();
  const response = await AuthApi.verifyPremiumStatus(signInResponse.token);
  expect(response.status).toBe(402);
});

test("premium is a member", async () => {
  const signInResponse = await createAndSignInToVerifiedAccount(true);
  const response = await AuthApi.verifyPremiumStatus(signInResponse.token);
  expect(response.status).toBe(200);
});

test("get premium is a member", async () => {
  const signInResponse = await createAndSignInToVerifiedAccount(true);
  const response = await AuthApi.getPremiumStatus(signInResponse.token);
  expect(response.isMember).toBe(true);
});

test("get premium not a member", async () => {
  const response = await AuthApi.getPremiumStatus("badToken");
  expect(response.isMember).toBe(false);
});

const requestAccountVerificationAndExpect = async (
  accountKey: string,
  expectedCode: number
) => {
  const response = await AuthApi.requestAccountVerification(accountKey);
  return expectResponseOrPrint(response, expectedCode);
};

const requestAccountResetAndExpect = async (
  accountKey: string,
  expectedCode: number
) => {
  const response = await AuthApi.requestAccountReset(accountKey);
  return expectResponseOrPrint(response, expectedCode);
};

const resetAccountAndExpect = async (
  token: string,
  new_password: string,
  expectedCode: number
) => {
  const response = await AuthApi.resetAccount(token, new_password);
  return expectResponseOrPrint(response, expectedCode);
};

const verifyAccountAndExpect = async (
  verification_token: string,
  expectedCode: number
) => {
  const response = await AuthApi.verifyAccount(verification_token);
  return expectResponseOrPrint(response, expectedCode);
};
