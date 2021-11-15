import * as cdk from "@aws-cdk/core";
import * as logs from "@aws-cdk/aws-logs";
import * as ec2 from "@aws-cdk/aws-ec2";
import * as ecs from "@aws-cdk/aws-ecs";
import * as elb from "@aws-cdk/aws-elasticloadbalancingv2";
import { DockerImageAsset } from "@aws-cdk/aws-ecr-assets";

export class EcsStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props: cdk.StackProps) {
    super(scope, id, props);

    const port = 80;

    const bffVpc = new ec2.Vpc(this, "TTM4160Vpc2", {});

    const cluster = new ecs.Cluster(this, "TTM4160Cluster", {
      vpc: bffVpc,
      clusterName: "TTM4160Cluster",
    });

    const taskDefinition = new ecs.FargateTaskDefinition(
      this,
      "BffTaskDeifinition",
      {}
    );

    taskDefinition.addContainer("BffContainer", {
      image: ecs.ContainerImage.fromDockerImageAsset(
        new DockerImageAsset(this, "4160ImageAsset", {
          directory: "../live",
        })
      ),
      environment: {},
      logging: ecs.LogDrivers.awsLogs({
        logGroup: new logs.LogGroup(this, "BffLogs", {
          retention: logs.RetentionDays.TWO_MONTHS,
        }),
        streamPrefix: "ecs",
        datetimeFormat: "%Y-%m-%dT%H:%M:%S",
      }),
      portMappings: [
        {
          containerPort: port,
          hostPort: port,
        },
      ],
    });

    const loadbalancer = new elb.ApplicationLoadBalancer(
      this,
      "BffLoadBalancer",
      {
        vpc: bffVpc,
        internetFacing: true,
      }
    );

    const service = new ecs.FargateService(this, "BffService", {
      cluster: cluster,
      taskDefinition: taskDefinition,
    });

    const targetGroup = new elb.ApplicationTargetGroup(this, "BffTargetGroup", {
      vpc: bffVpc,
      targets: [service],
      port: port,
    });

    targetGroup.configureHealthCheck({
      interval: cdk.Duration.minutes(1),
      path: "/health/",
      healthyThresholdCount: 2,
    });

    loadbalancer.addListener("ttm4160Listener", {
      protocol: elb.ApplicationProtocol.HTTP,
      port: 80,
      defaultTargetGroups: [targetGroup],
    });
  }
}
