import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda'
import * as iam from '@aws-cdk/aws-iam'
import * as uuid from 'uuid'
import * as crypto from 'crypto'
import * as fs from 'fs'
import * as sns from '@aws-cdk/aws-sns'
const { hashElement } = require('folder-hash');
import { SnsEventSource } from '@aws-cdk/aws-lambda-event-sources';
import * as subs from '@aws-cdk/aws-sns-subscriptions';

export class GreengrassLambdasStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    const gg_lambda_role = new iam.Role(this, "LambdaRole", {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('AWSGreengrassFullAccess'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
      ]    
    });

    const cloud_lambda_role = new iam.Role(this, "CloudLambdaRole", {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSNSFullAccess'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('AWSIoTDataAccess'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
      ]    
    });


    const newOrdersTopic = new sns.Topic(this, "NewDemandTopic", {
      topicName: "retail-demand-neworders"
    })




    const cloud_code = new lambda.AssetCode('cloud_lambdas');
    const gg_code = new lambda.AssetCode('gg_lambdas');

    // Create a unique value that represents all the files in the code directory.
    // This is used to generate a unique "version" object for each of the lambdas, 
    // so that when we do a deployment, it sends out the newest version.  It means
    // that whenever we update any code, all of the lambdas will be revisioned, but
    // I don't care.
    // TODO this won't handle updates in subdirectories
    var hash = crypto.createHash('sha1')
    for (let file of fs.readdirSync(gg_code.path)) {
      if (file.endsWith(".py") || file.endsWith(".txt")) {
        hash.update(fs.readFileSync(`${gg_code.path}/${file}`))
      }
    }
    var version = hash.digest('hex')


    var demandTranslator = new lambda.Function(this, "FarmDemandTranslator", {
      code: cloud_code,
      functionName: "FarmDemandTranslator",
      description: "Takes SNS messages published to represent demand, and sends them over MQTT to farm.  Note that this runs in the cloud, not on the Farm GreenGrass server",
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'demand_translator.function_handler',
      memorySize: 256,
      role: cloud_lambda_role
    });

    newOrdersTopic.addSubscription(new subs.LambdaSubscription(demandTranslator));



    const demand_receiver = new lambda.Function(this, "DemandReceiver", {
      code: gg_code,
      functionName: "FarmDemandReceiver",
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'demand_receiver.function_handler',
      memorySize: 256,
      role: gg_lambda_role,
    })

    new lambda.Alias(this, "DemandReceiverProdAlias", {
      aliasName: "prod",
      version: new lambda.Version(this, `DemandReceiverVersion${version}`, {
        lambda: demand_receiver,
        // codeSha256: hash_result
      })
    })


    const light_level_receiver = new lambda.Function(this, "LoraLightLevelReceiver", {
      code: gg_code,
      functionName: "FarmLoraLightLevelReceiver",
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'light_receiver.function_handler',
      memorySize: 256,
      role: gg_lambda_role,
    })

    new lambda.Alias(this, "LoraLightLevelReceiverProdAlias", {
      aliasName: "prod",
      version: new lambda.Version(this, `LoraLightLevelReceiverVersion${version}`, {
        lambda: light_level_receiver,
        // codeSha256: hash_result
      })
    })



    const light_updater = new lambda.Function(this, "LightUpdater", {
      code: gg_code,
      functionName: "FarmLightUpdater",
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'light_updater.function_handler',
      memorySize: 256,
      role: gg_lambda_role,
    })

    new lambda.Alias(this, "LightUpdaterProdAlias", {
      aliasName: "prod",
      version: new lambda.Version(this, `LightUpdaterVersion${version}`, {
        lambda: light_updater,
        // codeSha256: hash_result
      })
    })


    const metric_receiver = new lambda.Function(this, "MetricReceiver", {
      code: gg_code,
      description: "Receives Metrics from devices, and sends them to the cloud - or does it?",
      functionName: "FarmMetricReceiver",
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'metric_receiver.function_handler',
      memorySize: 256,
      role: gg_lambda_role,
    })

    new lambda.Alias(this, "MetricReceiverrProdAlias", {
      aliasName: "prod",
      version: new lambda.Version(this, `MetricReceiverVersion${version}`, {
        lambda: metric_receiver,
        // codeSha256: hash_result
      })
    })


    const farm_procesisng = new lambda.Function(this, "FarmProcessing", {
      code: gg_code,
      description: "Processes demand, producing beans",
      functionName: "FarmProcesisng",
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'farm_processing.function_handler',
      memorySize: 256,
      role: gg_lambda_role,
    })

    new lambda.Alias(this, "FarmProcessingrProdAlias", {
      aliasName: "prod",
      version: new lambda.Version(this, `FarmProcessingVersion${version}`, {
        lambda: farm_procesisng,
        // codeSha256: hash_result
      })
    })



    const webserver = new lambda.Function(this, "Webserver", {
      code: gg_code,
      description: "runs a webserver",
      functionName: "FarmWebserver",
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'webserver.function_handler',
      memorySize: 256,
      role: gg_lambda_role,
    })

    new lambda.Alias(this, "WebserverProdAlias", {
      aliasName: "prod",
      version: new lambda.Version(this, `WebserverrVersion${version}`, {
        lambda: webserver,
        // codeSha256: hash_result
      })
    })


  
  
  }
}
