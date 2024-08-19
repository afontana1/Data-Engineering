import { loadStripe } from "@stripe/stripe-js";
import { navigate } from "gatsby";
import BaseApi from "../util/base_api/BaseApi";
import ApiResponse from "../util/base_api/ApiResponse";

class PaymentApi extends BaseApi {
  protected static getEndpoint(): string {
    return process.env["GATSBY_AUTH_API_ENDPOINT"];
  }

  protected static getStripeKey(): string {
    return process.env["GATSBY_STRIPE_PUBLIC_KEY"];
  }

  public static async redirectToCheckout(sessionId: string) {
    const stripe = await loadStripe(this.getStripeKey());
    const { error } = await stripe.redirectToCheckout({ sessionId });
    alert(error.message);
  }

  public static requestCheckout(token: string): Promise<ApiResponse> {
    const returnEndpoint: string = this.getReturnEndpoint();
    return this.postRequest(
      "create_payment_session",
      { return_endpoint: returnEndpoint },
      token
    );
  }

  public static requestPaymentPortal(token: string): Promise<ApiResponse> {
    const returnEndpoint: string = this.getReturnEndpoint();
    return this.postRequest(
      "create_payment_portal",
      { return_endpoint: returnEndpoint },
      token
    );
  }

  public static async requestCheckoutAndRedirect(token: string): Promise<void> {
    try {
      const response = await this.requestCheckout(token);
      await this.redirectToCheckout(response.payload["session_id"]);
    } catch (e) {
      console.log(e);
      throw e;
    }
  }

  public static getReturnEndpoint(): string {
    return window.location.origin + "/app/";
  }

  public static async requestPaymentPortalAndRedirect(
    token: string
  ): Promise<void> {
    const response = await this.requestPaymentPortal(token);
    const externalUrl = response.payload["session_url"];
    navigate(externalUrl);
  }
}

export default PaymentApi;
