import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import GreengrassLambdas = require('../lib/greengrass_lambdas-stack');

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new GreengrassLambdas.GreengrassLambdasStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
