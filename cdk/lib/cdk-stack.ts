import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as path from 'path';
import { Construct } from 'constructs';
import { Platform } from 'aws-cdk-lib/aws-ecr-assets';

export class LambdaStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const api = new lambda.DockerImageFunction(this, 'SimpleFastApi', {
      code: lambda.DockerImageCode.fromImageAsset(
        path.join(__dirname, '../../app'),
        {
          platform: Platform.LINUX_AMD64,
        }
      ),
    });

    new apigateway.LambdaRestApi(this, 'SimpleFastApiEndpoint', {
      handler: api,
    });
  }
}
