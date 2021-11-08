import * as cdk from "@aws-cdk/core";
import * as s3 from "@aws-cdk/aws-s3";
import * as iam from "@aws-cdk/aws-iam";
import * as cloudFront from "@aws-cdk/aws-cloudfront";
import * as origins from "@aws-cdk/aws-cloudfront-origins";
import * as cm from "@aws-cdk/aws-certificatemanager";

interface WebStackProps extends cdk.StackProps {
  domainName?: string;
}

export class WebStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props: WebStackProps) {
    super(scope, id, props);

    const webappBucket = new s3.Bucket(this, "TTM4160WebBucket", {
      encryption: s3.BucketEncryption.S3_MANAGED,
    });

    const ciUser = new iam.User(this, "CiUser");

    webappBucket.grantReadWrite(ciUser);

    const originAccessIdentity = new cloudFront.OriginAccessIdentity(
      this,
      "WebOriginAccess"
    );
    webappBucket.addToResourcePolicy(
      new iam.PolicyStatement({
        resources: [webappBucket.arnForObjects("*")],
        actions: ["s3:GetObject"],
        principals: [originAccessIdentity.grantPrincipal],
      })
    );
    webappBucket.addToResourcePolicy(
      new iam.PolicyStatement({
        resources: [webappBucket.bucketArn],
        actions: ["s3:ListBucket"],
        principals: [originAccessIdentity.grantPrincipal],
      })
    );
    const origin = new origins.S3Origin(webappBucket, {
      originPath: "/web",
      originAccessIdentity,
    });
    const cdn = new cloudFront.Distribution(this, "WebDistribution", {
      defaultBehavior: {
        origin: origin,
        cachePolicy: new cloudFront.CachePolicy(this, "WebAppCachePolicy", {
          defaultTtl: cdk.Duration.minutes(5),
          maxTtl: cdk.Duration.minutes(20),
        }),
        viewerProtocolPolicy: cloudFront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
      },
      errorResponses: [
        {
          httpStatus: 404,
          responseHttpStatus: 200,
          responsePagePath: "/index.html",
        },
      ],
      defaultRootObject: "index.html",
      //   certificate: cm.Certificate.fromCertificateArn(
      //     this,
      //     "Certificate",
      //     "arn:aws:acm:us-east-1:859141738257:certificate/95a16c6a-6eac-4809-94d9-f52d0d019d72"
      //   ),
      //   domainNames: [props.domainName!!], // wait until domain is forwarded
    });

    // new r53.ARecord(this, `DnRecord${props.domainName}`, {
    //   zone: r53.HostedZone.fromHostedZoneId(
    //     this,
    //     "DomainNameZone",
    //     "Z01406901IXMYPGRJ4RT6"
    //   ),
    //   recordName: `${props.domainName}.`,
    //   target: r53.RecordTarget.fromAlias(new r53t.CloudFrontTarget(cdn)),
    // });
  }
}
