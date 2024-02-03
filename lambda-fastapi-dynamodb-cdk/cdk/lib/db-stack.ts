import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { Construct } from 'constructs';


// FIXME: Lambda에서 사용하는 테이블은 이 테이블이 아니다.
//        Lambda BuildArgs로 테이블 이름을 넘겨주는 방식으로 변경 필요.
export class DbStack extends cdk.Stack {
  public readonly table: dynamodb.Table;
  
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB
    this.table = new dynamodb.Table(this, 'Table', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    });
  }
}
