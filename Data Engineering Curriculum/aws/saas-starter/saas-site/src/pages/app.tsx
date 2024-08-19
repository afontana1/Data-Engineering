import React from "react";
import LandingView from "../app/LandingView";
import AuthRoute from "../components/auth/route/AuthRoute";
import ProfileView from "../app/ProfileView";
import PageNotFound from "./404";
import AuthRouter from "../components/auth/route/AuthRouter";
import AuthProvider from "../components/auth/route/AuthProvider";
import Layout from "../layout/Layout";

const App = () => {
  return (
    <AuthProvider>
      <Layout>
        <AuthRouter>
          <AuthRoute component={LandingView} path="/app" bypassAuth />
          <AuthRoute component={ProfileView} path="/app/profile" />
          <PageNotFound default />
        </AuthRouter>
      </Layout>
    </AuthProvider>
  );
};
export default App;
