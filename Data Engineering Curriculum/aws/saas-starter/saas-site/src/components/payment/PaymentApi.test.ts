import PaymentApi from "./PaymentApi";
import axios from "axios";
import ApiResponse from "../util/base_api/ApiResponse";
import {
  expectResponseOrPrint,
  newRandomPassword,
  newRandomUser,
  signInAndExpect,
  signUpAndExpect,
} from "../util/base_api/ApiTestUtils";

beforeEach(async () => {
  // HTTP Adapter required to solve CORS error.
  axios.defaults.adapter = require("axios/lib/adapters/http");

  // Set the timeout.
  jest.setTimeout(45000);
});

test("request checkout session", async () => {
  const user: string = newRandomUser();
  const password: string = newRandomPassword();
  await signUpAndExpect(user, password, 200);
  const signInResponse = await signInAndExpect(user, password, 200);
  const response = await requestPaymentCheckoutAndExpect(
    signInResponse.token,
    200
  );
  console.log(response.payload);
  expect(response.payload).toHaveProperty("session_id");
});

const requestPaymentCheckoutAndExpect = async (
  token: string,
  expectedCode: number
) => {
  const response = await PaymentApi.requestCheckout(token);
  return expectResponseOrPrint(response, expectedCode);
};
