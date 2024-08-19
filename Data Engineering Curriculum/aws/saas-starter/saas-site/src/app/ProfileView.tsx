import { navigate } from "gatsby";
import * as React from "react";
import AuthApi from "../components/auth/api/AuthApi";
import AuthContext from "../components/auth/api/AuthContext";
import * as AuthURL from "../components/auth/route/AuthURL";
import PaymentApi from "../components/payment/PaymentApi";
import withBoxStyling from "../components/util/functions/withBoxStyling";

interface ProfileViewProps {
  path: string;
}

const ProfileView: React.FC<ProfileViewProps> = (props) => {
  const [isLoadingPremium, setLoadingPremium] = React.useState(true);
  const [isPremiumMember, setPremiumMember] = React.useState(false);
  const [isAutoRenew, setAutoRenew] = React.useState(false);
  const [expiryTime, setExpiryTime] = React.useState(0);
  const auth = React.useContext(AuthContext);

  const [
    isLoadingVerificationStatus,
    setLoadingVerificationStatus,
  ] = React.useState(true);
  const [isVerified, setVerified] = React.useState(false);

  React.useEffect(() => {
    let isMounted = true;

    AuthApi.getPremiumStatus(auth.state.token).then((premiumStatus) => {
      if (isMounted) {
        setPremiumMember(premiumStatus.isMember);
        setAutoRenew(premiumStatus.autoRenew);
        setExpiryTime(premiumStatus.expiryTime);
        console.log("Set Autorenew to: " + premiumStatus.autoRenew);
        console.log("Set expiryTime Time to: " + premiumStatus.expiryTime);
        setLoadingPremium(false);
      }
    });

    AuthApi.getAccountVerificationStatusAsBoolean(auth.state.token).then(
      (isVerified) => {
        if (isMounted) {
          setVerified(isVerified);
          setLoadingVerificationStatus(false);
        }
      }
    );

    return () => {
      isMounted = false;
    };
  }, []);

  const onClickToSubscribe = () => {
    setLoadingPremium(true);
    PaymentApi.requestCheckoutAndRedirect(auth.state.token).catch((r) => {
      setLoadingPremium(false);
      console.log(r);
    });
  };

  const onClickToPaymentPortal = () => {
    setLoadingPremium(true);
    PaymentApi.requestPaymentPortalAndRedirect(auth.state.token);
  };

  let premiumStatusElement;
  let premiumInteractiveElement;

  if (isLoadingPremium) {
    premiumStatusElement = <div className="text-gray-400">Loading</div>;
    premiumInteractiveElement = <div className="loader-dark"></div>;
  } else {
    if (isPremiumMember) {
      const expiryDate = new Date(expiryTime * 1000);
      const expiryElement = (
        <div className="text-xs text-gray-500 mb-1">
          Until {expiryDate.toLocaleDateString()}
        </div>
      );

      const autoRenewColors: string = isAutoRenew
        ? "bg-green-100 text-green-600"
        : "bg-gray-200 text-gray-600";

      const autoRenewElement = (
        <div
          className={
            "mt-2 text-center text-xs font-bold p-1 rounded-md px-2 " +
            autoRenewColors
          }
        >
          AUTO RENEW {isAutoRenew ? "ON" : "OFF"}
        </div>
      );

      premiumStatusElement = (
        <div>
          <div className="text-green-600">Active </div>
          {expiryElement}
        </div>
      );
      premiumInteractiveElement = (
        <div>
          <button
            className="bg-blue-600 text-white rounded-md p-2 w-32"
            onClick={onClickToPaymentPortal}
          >
            Manage
          </button>
          {autoRenewElement}
        </div>
      );
    } else {
      premiumStatusElement = <div>Inactive</div>;
      premiumInteractiveElement = (
        <button
          className="bg-blue-600 text-white rounded-md p-2 w-32"
          onClick={onClickToSubscribe}
        >
          Subscribe
        </button>
      );
    }
  }

  const onClickToVerify = () => {
    setLoadingVerificationStatus(true);
    navigate(AuthURL.VERIFY_ACCOUNT_REQUEST);
  };

  let verificationStatusElement;
  let verificationInteractiveElement;

  if (isLoadingVerificationStatus) {
    verificationStatusElement = <div className="text-gray-400">Loading</div>;
    verificationInteractiveElement = <div className="loader-dark"></div>;
  } else {
    if (isVerified) {
      verificationStatusElement = (
        <div className="text-green-600">Verified</div>
      );
      verificationInteractiveElement = null;
    } else {
      verificationStatusElement = (
        <div className="text-red-700">Not Verified</div>
      );
      verificationInteractiveElement = (
        <button
          className="bg-blue-600 text-white rounded-md p-2 w-32"
          onClick={onClickToVerify}
        >
          Verify
        </button>
      );
    }
  }

  const premiumElement = (
    <div className="bg-gray-50 p-4 rounded-md flex justify-between mb-2">
      <div className="my-auto">
        <div className="text-gray-600 text-sm">Premium Status</div>
        <div className="text-lg font-light">{premiumStatusElement}</div>
      </div>

      <div className="my-auto">{premiumInteractiveElement}</div>
    </div>
  );

  const verifyElement = (
    <div className="bg-gray-50 p-4 rounded-md flex justify-between">
      <div className="my-auto">
        <div className="text-gray-600 text-sm">Verification Status</div>
        <div className="text-lg font-light">{verificationStatusElement}</div>
      </div>

      <div className="my-auto">{verificationInteractiveElement}</div>
    </div>
  );

  return (
    <>
      <h1 className="text-xl font-bold mb-4">Your Profile</h1>
      {premiumElement}
      {verifyElement}
    </>
  );
};

export default withBoxStyling(ProfileView);
