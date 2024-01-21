import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as path from 'path';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';
import { Platform } from 'aws-cdk-lib/aws-ecr-assets';
import { StackProps } from '../bin/cdk';

export class ApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const api = new lambda.DockerImageFunction(this, 'SimpleFastApi', {
      code: lambda.DockerImageCode.fromImageAsset(
        path.join(__dirname, '../../api'),
        {
          platform: Platform.LINUX_AMD64,
        }
      ),
    });

    api.role?.attachInlinePolicy(new iam.Policy(this, 'DynamoDBPolicy', {
      statements: [
        new iam.PolicyStatement({
          sid: 'DynamoDBPolicy',
          effect: iam.Effect.ALLOW,
          actions: ['dynamodb:*'],
          resources: ['*'],
        }),
      ],
    }));

    new apigateway.LambdaRestApi(this, 'SimpleFastApiEndpoint', {
      handler: api,
    });
  }
}
