import * as cdk from "@aws-cdk/core";
import * as lambda from "@aws-cdk/aws-lambda";
import * as apigateway from "@aws-cdk/aws-apigateway";
import { NodejsFunction } from "@aws-cdk/aws-lambda-nodejs";
import * as path from "path";
import { WebStack } from "../src/web-stack";

export class InfraStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here

    const webApp = new WebStack(this, "TTM4160WebStack", {});

    const handler = new lambda.Function(this, "WidgetHandler", {
      runtime: lambda.Runtime.NODEJS_14_X, // So we can use async in widget.js
      code: lambda.Code.fromAsset(path.join(__dirname, "../lambda/build")),
      handler: "index.main",
      environment: {},
    });

    const api = new apigateway.RestApi(this, "widgets-api", {
      restApiName: "TTM4160 service",
      description: "This service serves widgets.",
    });

    const getWidgetsIntegration = new apigateway.LambdaIntegration(handler, {
      requestTemplates: { "application/json": '{ "statusCode": "200" }' },
    });
    const postWidgetIntegration = new apigateway.LambdaIntegration(handler);

    api.root.addMethod("GET", getWidgetsIntegration); // GET /
    api.root.addMethod("POST", postWidgetIntegration); // POST /
  }
}
