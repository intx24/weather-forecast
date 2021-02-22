#!/usr/bin/env python3

from aws_cdk import core

from lib.stack.ecr.ecr_stack import EcrStack
from lib.stack.stepfunctions.stepfunctions_stack import StepFunctionsStack
from lib.util.stack_util import StackUtil

app = core.App()

stack_util = StackUtil()
ecr_stack = EcrStack(app, stack_util.get_stack_name('REPOSITORY'))
StepFunctionsStack(app, stack_util.get_stack_name('STEPFUNCTIONS')) \
    .add_dependency(ecr_stack)

app.synth()
