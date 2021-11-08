import * as cdk from "@aws-cdk/core";
import { WebStack } from "../src/web-stack";

export class InfraStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here

    const webApp = new WebStack(this, "TTM4160WebStack", {});
  }
}
