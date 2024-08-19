import axios, { AxiosRequestConfig, AxiosResponse, Method } from "axios";
import ApiRequest from "./ApiRequest";
import ApiResponse from "./ApiResponse";

class BaseApi {
  public static delayedSuccess(): Promise<ApiResponse> {
    const response: ApiResponse = {
      status: 200,
      message: "Fake operation succeeded!",
      payload: {},
    };
    return this.genericFakePromise((resolve, _reject) => resolve(response));
  }

  public static delayedError(): Promise<ApiResponse> {
    const response: ApiResponse = {
      status: 400,
      message: "Fake operation error!",
      payload: {},
    };
    return this.genericFakePromise((resolve, _reject) => resolve(response));
  }

  public static delayedFault(): Promise<ApiResponse> {
    return this.genericFakePromise((_resolve, reject) =>
      reject("Some unknown fault!")
    );
  }

  protected static genericFakePromise(
    executor: (
      resolve: (value: ApiResponse | PromiseLike<ApiResponse>) => void,
      reject: (reason?: any) => void
    ) => void
  ): Promise<ApiResponse> {
    const promise = new Promise<ApiResponse>((resolve, reject) => {
      setInterval(() => executor(resolve, reject), 1000);
    });
    return promise;
  }

  protected static getEndpoint(): string {
    throw new Error("getEndpoint() is not implemented!");
  }

  protected static getRequest(
    operation: string,
    payload: any,
    token?: string,
    extraFlags?: string[]
  ) {
    return this.genericRequest("GET", operation, payload, token, extraFlags);
  }

  protected static postRequest(
    operation: string,
    payload: any,
    token?: string,
    extraFlags?: string[]
  ) {
    return this.genericRequest("POST", operation, payload, token, extraFlags);
  }

  private static genericRequest(
    method: Method,
    operation: string,
    payload: any,
    token?: string,
    extraFlags?: string[]
  ) {
    const request: ApiRequest = {
      endpoint: this.getEndpoint(),
      method: method,
      operation: operation,
      payload: payload,
      token: token,
      extraFlags: extraFlags,
    };
    return this.sendRequest(request);
  }

  private static sendRequest(request: ApiRequest): Promise<ApiResponse> {
    const requestConfig = this.convertToAxiosRequestConfig(request);
    return new Promise<ApiResponse>((resolve, reject) => {
      axios
        .request(requestConfig)
        .then((r) => this.handleResponse(r, resolve))
        .catch((e) => this.handleError(e, resolve));
    });
  }

  protected static withSideEffect(
    promise: Promise<ApiResponse>,
    executor: (x: ApiResponse) => void
  ): Promise<ApiResponse> {
    return new Promise<ApiResponse>((resolve, reject) => {
      promise
        .then((r) => {
          executor(r);
          resolve(r);
        })
        .catch(reject);
    });
  }

  private static convertToAxiosRequestConfig(
    request: ApiRequest
  ): AxiosRequestConfig {
    // Start config.
    const requestConfig: AxiosRequestConfig = {
      url: request.endpoint,
      method: request.method,
    };

    // Bearer Token if any...
    if (request.token) {
      requestConfig.headers = {
        Authorization: `Bearer ${request.token}`,
        Accept: "application/json",
        "Content-Type": "application/json",
      };
    }

    // Concat the flags.

    const flags =
      request.extraFlags === undefined
        ? ["TMP"]
        : ["TMP", ...request.extraFlags];

    // If a payload exists, add it to the request.
    const payload = {
      operation: request.operation,
      flags: flags,
      ...request.payload,
    };

    // Add payload to appropriate request field.
    if (request.method === "GET") {
      requestConfig.params = payload;
    } else {
      requestConfig.data = payload;
    }

    return requestConfig;
  }

  private static handleResponse(response: AxiosResponse, resolve: any) {
    const apiResponse: ApiResponse = {
      status: response.status,
      message: response.data.message,
      payload: response.data.payload,
    };
    resolve(apiResponse);
  }

  private static handleError(error: any, resolve: any) {
    if (error.response) {
      resolve({
        status: error.response.status,
        message: error.response.data.message,
        payload: error.response.data,
      });
    } else {
      resolve({
        status: 400,
        message: `Unknown Error: ${error}`,
        payload: { error: error },
      });
    }
  }
}

export default BaseApi;
