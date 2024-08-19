#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "@aws-cdk/core";
import { SaasInfrastructureStack } from "../lib/saas-infrastructure-stack";
import ServiceProps from "../lib/utils/service-props";
import * as config from "../service.config.json";

// Configure all infrastructure things here.
const serviceProps: ServiceProps = {
  serviceName: config.name,
  serviceRootDomain: config.domain,
  servicePrefix: config.prefix,
  serviceFrontendUrl: config.frontendUrl,
  region: config.awsRegion,
  stripeKey: config.stripeKey,
  stripePriceId: config.stripePriceId,
};

const app = new cdk.App();
new SaasInfrastructureStack(app, `${config.name}`, serviceProps, {
  env: { account: config.awsAccount, region: config.awsRegion },
});
