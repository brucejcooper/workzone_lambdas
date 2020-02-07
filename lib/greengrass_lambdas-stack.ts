import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda'
import * as iam from '@aws-cdk/aws-iam'

export class GreengrassLambdasStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    const role = new iam.Role(this, "LambdaRole", {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('AWSGreengrassFullAccess'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
      ]    
    });

    const code = new lambda.AssetCode('lambdas');


    const demand_receiver = new lambda.Function(this, "DemandReceiver", {
      code: code,
      functionName: "FarmDemandReceiver",
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'demand_receiver.function_handler',
      memorySize: 512,
      role: role,
    })

    new lambda.Alias(this, "DemandReceiverProdAlias", {
      aliasName: "prod",
      version: new lambda.Version(this, "DemandReceiverVersion", {
        lambda: demand_receiver
      })
    })


    const metric_receiver = new lambda.Function(this, "MetricReceiver", {
      code: code,
      description: "Receives messages from devices, and forwards them to the cloud",
      functionName: "FarmMetricReceiver",
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'metric_receiver.function_handler',
      memorySize: 512,
      role: role,
    })

    new lambda.Alias(this, "MetricReceiverrProdAlias", {
      aliasName: "prod",
      version: new lambda.Version(this, "MetricReceiverVersion", {
        lambda: metric_receiver
      })
    })




    const webserver = new lambda.Function(this, "Webserver", {
      code: code,
      description: "Receives messages from devices, and forwards them to the cloud",
      functionName: "FarmWebserver",
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'webserver.function_handler',
      memorySize: 512,
      role: role,
    })

    new lambda.Alias(this, "WebserverProdAlias", {
      aliasName: "prod",
      version: new lambda.Version(this, "WebserverrVersion6", {
        lambda: webserver
      })
    })
  }
}
