from aws_cdk import core
from aws_cdk.aws_ecr import Repository, LifecycleRule, TagStatus

from lib.util.stack_util import StackUtil


class EcrStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stack_util = StackUtil()

        Repository(self,
                   'Repository',
                   repository_name=stack_util.get_name('repo'),
                   lifecycle_rules=[LifecycleRule(
                       description='leave only one untagged',
                       rule_priority=1,
                       tag_status=TagStatus.UNTAGGED,
                       max_image_count=1
                   )])
