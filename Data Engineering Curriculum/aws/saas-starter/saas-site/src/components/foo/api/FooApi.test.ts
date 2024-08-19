import FooApi from "./FooApi";
import axios from "axios";
import {
  newRandomPassword,
  newRandomUser,
  randomUUID,
  signInAndExpect,
  signUpAndExpect,
} from "../../util/base_api/ApiTestUtils";

beforeEach(async () => {
  // HTTP Adapter required to solve CORS error.
  axios.defaults.adapter = require("axios/lib/adapters/http");

  // Set the timeout.
  jest.setTimeout(45000);
});

test("foo not signed in", async () => {
  // Token validation should succeed.
  const response = await FooApi.foo("badToken");
  expect(response.status).toBe(200);
  expect(response.isSignedIn).toBe(false);
  expect(response.isPremium).toBe(false);
  expect(response.isAccountVerified).toBe(false);
});

test("foo signed in but not verified", async () => {
  // Token validation should succeed.
  const signInResponse = await createAndSignUser();
  const response = await FooApi.foo(signInResponse.token);

  expect(response.status).toBe(200);
  expect(response.isSignedIn).toBe(true);
  expect(response.isPremium).toBe(false);
  expect(response.isAccountVerified).toBe(false);
});

test("foo can write and get post", async () => {
  const randomContent = `My random content ${randomUUID()}`;

  const signInResponse = await createAndSignUser();
  const response = await FooApi.putPost(
    "My Post Title",
    randomContent,
    signInResponse.token
  );
  expect(response.status).toBe(200);
  expect(response.itemKey).not.toBeUndefined();
  const postKey = response.itemKey;

  // Try to get the post from batch.
  const getPostsResponse = await FooApi.getPosts();
  expect(getPostsResponse.status).toBe(200);
  expect(getPostsResponse.items).not.toBeUndefined();

  // Check that most recent item is the one we put.
  const mostRecentItem = getPostsResponse.items[0];
  expect(mostRecentItem.content).toEqual(randomContent);
  expect(mostRecentItem.key).not.toBeUndefined();
  expect(mostRecentItem.account_id).not.toBeUndefined();

  // Try to get the specific post directly.
  const getPostResponse = await FooApi.getPost(postKey);
  expect(getPostResponse.status).toBe(200);
  expect(getPostResponse.items).not.toBeUndefined();
});

// ===================================================================================================
//
// ===================================================================================================

const createAndSignUser = async () => {
  const user: string = newRandomUser();
  const password: string = newRandomPassword();
  await signUpAndExpect(user, password, 200);
  return await signInAndExpect(user, password, 200);
};
