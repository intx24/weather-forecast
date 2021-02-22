#!/usr/bin/env python3

from aws_cdk import core

from lib.stack.ecr.ecr_stack import EcrStack
from lib.util.stack_util import StackUtil

app = core.App()

stack_util = StackUtil()
EcrStack(app, stack_util.get_stack_name('REPOSITORY'))

app.synth()
