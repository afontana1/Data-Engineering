import ApiResponse from "../../util/base_api/ApiResponse";

export interface FooResponse extends ApiResponse {
  isPremium?: boolean;
  isAccountVerified?: boolean;
  isSignedIn?: boolean;
  itemKey?: string;
  items?: FooPost[];
}

export interface FooPost {
  content: string;
  account_id: string;
  key: string;
}

export const withFooResponse = (
  promise: Promise<ApiResponse>
): Promise<FooResponse> => {
  return new Promise<FooResponse>((resolve, reject) => {
    promise
      .then((apiResponse) => {
        const authResponse: FooResponse = {
          ...apiResponse,
          isPremium: apiResponse.payload["is_premium"],
          isAccountVerified: apiResponse.payload["is_account_verified"],
          isSignedIn: apiResponse.payload["is_signed_in"],
          itemKey: apiResponse.payload["item_key"],
        };

        const itemsArray = apiResponse.payload["items"];
        if (itemsArray !== undefined) {
          authResponse.items = [];
          for (let i = 0; i < itemsArray.length; i++) {
            const rawItem = itemsArray[i];
            console.log(rawItem);
            authResponse.items.push(rawItem);
          }
        }

        resolve(authResponse);
      })
      .catch(reject);
  });
};
