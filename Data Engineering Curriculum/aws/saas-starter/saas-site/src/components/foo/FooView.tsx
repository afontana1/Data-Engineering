import * as React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCheckCircle,
  faTimesCircle,
  faQuestionCircle,
} from "@fortawesome/free-solid-svg-icons";
import {
  SubComponentBaseProps,
  withApiWrapper,
} from "../util/base_api_components/ApiComponents";
import FooApi from "./api/FooApi";
import withBoxStyling from "../util/functions/withBoxStyling";
import ApiRefresher from "../util/base_api_components/ApiRefresher";
import { useContext } from "react";
import AuthContext from "../auth/api/AuthContext";

interface ServiceResponseProps {
  fooIsSignedIn: boolean;
  fooIsIsVerified: boolean;
  fooIsPremium: boolean;
  isLoading: boolean;
}

const ServiceResponseView = (props: ServiceResponseProps) => {
  if (props.isLoading) {
    const loadingColor = "text-gray-500";
    const questionCircle = <FontAwesomeIcon icon={faQuestionCircle} />;

    return (
      <div>
        <div className={loadingColor}>{questionCircle} Signed In</div>
        <div className={loadingColor}>{questionCircle} Verified</div>
        <div className={loadingColor}>{questionCircle} Premium Plan</div>
      </div>
    );
  } else {
    const checkCircleIcon = <FontAwesomeIcon icon={faCheckCircle} />;
    const checkTimesIcon = <FontAwesomeIcon icon={faTimesCircle} />;

    const isSignedInStatus = props.fooIsSignedIn
      ? checkCircleIcon
      : checkTimesIcon;
    const isVerifiedStatus = props.fooIsIsVerified
      ? checkCircleIcon
      : checkTimesIcon;
    const isPremiumMember = props.fooIsPremium
      ? checkCircleIcon
      : checkTimesIcon;
    const isSignedInColor = props.fooIsSignedIn
      ? "text-green-500"
      : "text-red-500";
    const isVerifiedColor = props.fooIsIsVerified
      ? "text-green-500"
      : "text-red-500";
    const isPremiumMColor = props.fooIsPremium
      ? "text-green-500"
      : "text-red-500";

    return (
      <div>
        <div className={isSignedInColor}>{isSignedInStatus} Signed In</div>
        <div className={isVerifiedColor}>{isVerifiedStatus} Verified</div>
        <div className={isPremiumMColor}>{isPremiumMember} Premium Plan</div>
      </div>
    );
  }
};

const FooView: React.FC<SubComponentBaseProps> = (props) => {
  const [fooIsSignedIn, setFooIsSignedIn] = React.useState(false);
  const [fooIsIsVerified, setFooIsVerified] = React.useState(false);
  const [fooIsPremium, setFooIsPremium] = React.useState(false);
  const auth = useContext(AuthContext);

  const refreshServiceStatus = () => {
    let isMounted: boolean = true;
    props.onApiRequest();
    FooApi.foo(auth.state.token)
      .then((r) => {
        if (isMounted) {
          props.onApiResponse(r);
          setFooIsSignedIn(r.isSignedIn);
          setFooIsVerified(r.isAccountVerified);
          setFooIsPremium(r.isPremium);
        }
      })
      .catch((r) => {
        if (isMounted) {
          props.onApiFault(r);
          setFooIsSignedIn(false);
          setFooIsVerified(false);
          setFooIsPremium(false);
        }
      });

    return () => {
      isMounted = false;
    };
  };

  const onClickRefresh = () => {
    refreshServiceStatus();
  };

  // Hit the Foo API and get the response.
  React.useEffect(refreshServiceStatus, [auth.state.token]);

  return (
    <div>
      <div className="flex justify-between mb-4">
        <h1 className="text-xl font-bold my-auto">Foo Service Status</h1>
        <ApiRefresher
          onClickRefresh={onClickRefresh}
          isRefreshing={props.apiState.isBusy}
        />
      </div>
      <div className="bg-gray-50 rounded-md p-4 mt-2">
        <ServiceResponseView
          fooIsSignedIn={fooIsSignedIn}
          fooIsIsVerified={fooIsIsVerified}
          fooIsPremium={fooIsPremium}
          isLoading={props.apiState.isBusy}
        />
      </div>
    </div>
  );
};

export default withBoxStyling(withApiWrapper(FooView));
