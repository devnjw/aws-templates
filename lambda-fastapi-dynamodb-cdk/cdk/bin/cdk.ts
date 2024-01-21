#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { ApiStack } from '../lib/api-stack';
import { DbStack } from '../lib/db-stack';

export interface StackProps extends cdk.StackProps {
    dbStack?: DbStack;
    apiStack?: ApiStack;
}

const app = new cdk.App();
const stackProps: StackProps = {};
stackProps.dbStack = new DbStack(app, 'DbStack', stackProps);
stackProps.apiStack = new ApiStack(app, 'ApiStack', stackProps);
