import * as React from "react";
import AuthCommonComponent from "./AuthCommonComponent";
import {
  ApiButton,
  withApiWrapper,
  SubComponentBaseProps,
  ApiTextLink,
} from "../../util/base_api_components/ApiComponents";
import * as AuthURL from "../route/AuthURL";
import { navigate } from "gatsby";
import { useLocation } from "@reach/router";
import AuthApi from "../api/AuthApi";

enum VerificationStatus {
  LOADING,
  FAILED,
  SUCCESS,
}

const AuthVerifyAccount: React.FC<SubComponentBaseProps> = (props) => {
  const query = new URLSearchParams(useLocation().search);
  const [status, setStatus] = React.useState(VerificationStatus.LOADING);
  const key = query.get("key");

  React.useEffect(() => {
    let isMounted: boolean = true;

    if (key === null) {
      setStatus(VerificationStatus.FAILED);
    } else {
      AuthApi.verifyAccount(key)
        .then((r) => {
          if (isMounted) {
            props.onApiResponse(r);
            if (r.status == 200) {
              setStatus(VerificationStatus.SUCCESS);
            } else {
              setStatus(VerificationStatus.FAILED);
            }
          }
        })
        .catch((r) => {
          if (isMounted) {
            props.onApiFault(r);
            setStatus(VerificationStatus.FAILED);
          }
        });
    }
    return () => {
      isMounted = false;
    };
  }, []);

  const actionButton = (
    <ApiButton label="Back" onClick={() => navigate(AuthURL.HOME)} />
  );

  const pageLabel: string = "Account Verification";
  let contentDiv: any = null;

  const loadingContent = (
    <div className="md:text-base text-sm text-gray-800 mb-6">
      <div className="bg-gray-100 p-4 rounded-md">
        <div className="w-full">
          <div className="w-full mt-4 flex">
            <div className="flex mx-auto">
              <div className="w-12 h-12 flex">
                <div className="loader-dark" />
              </div>
            </div>
          </div>
          <div className="text-center mt-4 text-gray-500">
            Please wait a moment.
          </div>
        </div>
      </div>
    </div>
  );

  const successContent = (
    <div className="md:text-base text-sm text-gray-800 mb-6">
      <div className="bg-green-100 p-4 rounded-md">
        <div className="font-semibold mb-1 text-green-700 text-lg">
          Success!
        </div>
        <div className="text-green-600 text-sm md:text-base">
          Your account is now verified. Please sign in to start using your
          account.
        </div>
      </div>

      {actionButton}
    </div>
  );

  const failedContent = (
    <div className="md:text-base text-sm text-gray-800 mb-6">
      <div className="bg-gray-100 p-4 rounded-md">
        <div className="font-semibold mb-1 text-gray-800 text-lg">
          Verification failed
        </div>
        <div className="text-gray-700 text-sm md:text-base mb-2">
          The verification key either doesn't exist or has expired. Please
          request a new verification key and try again.
        </div>
        <ApiTextLink
          linkPath={AuthURL.VERIFY_ACCOUNT_REQUEST}
          linkText="re-verify"
          preLinkText="Sign in to"
        />
      </div>
    </div>
  );

  switch (status) {
    case VerificationStatus.LOADING:
      contentDiv = loadingContent;
      break;

    case VerificationStatus.SUCCESS:
      contentDiv = successContent;
      break;

    case VerificationStatus.FAILED:
      contentDiv = failedContent;
      break;
  }

  return (
    <AuthCommonComponent header={pageLabel} apiState={props.apiState}>
      {contentDiv}
    </AuthCommonComponent>
  );
};

export default withApiWrapper(AuthVerifyAccount);
