#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { GreengrassLambdasStack } from '../lib/greengrass_lambdas-stack';

const app = new cdk.App();
new GreengrassLambdasStack(app, 'GreengrassLambdasStack');
