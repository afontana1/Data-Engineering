import BaseApi from "../../util/base_api/BaseApi";
import { FooResponse, withFooResponse } from "./FooResponse";

class FooApi extends BaseApi {
  protected static getEndpoint(): string {
    return process.env["GATSBY_FOO_API_ENDPOINT"];
  }

  public static foo(token: string): Promise<FooResponse> {
    return this.callWithToken("foo", {}, token);
  }

  public static putPost(
    title: string,
    content: string,
    token?: string
  ): Promise<FooResponse> {
    return this.callWithToken(
      "foo_write_post",
      {
        title,
        content,
      },
      token
    );
  }

  public static getPosts(token?: string): Promise<FooResponse> {
    return this.callWithToken("foo_get_posts", {}, token);
  }

  public static getPost(key: string, token?: string): Promise<FooResponse> {
    return this.callWithToken("foo_get_post", { key }, token);
  }

  private static callWithToken(
    apiName: string,
    params: any,
    token?: string
  ): Promise<FooResponse> {
    console.log("Calling " + apiName + " with token " + token);
    const responsePromise = this.getRequest(apiName, params, token);
    return withFooResponse(responsePromise);
  }
}

export default FooApi;
