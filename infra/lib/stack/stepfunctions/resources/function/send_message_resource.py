from aws_cdk import core
from aws_cdk.aws_ecr import IRepository
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode
from aws_cdk.aws_logs import RetentionDays

from lib.config.secrets import secrets


def get_send_message_resource(scope: core.Construct, ecr: IRepository) -> DockerImageFunction:
    return DockerImageFunction(
        scope=scope,
        id='SendMessageFunction',
        function_name='send-message',
        code=DockerImageCode.from_ecr(
            repository=ecr,
            tag='send-message',
        ),
        log_retention=RetentionDays.ONE_DAY,
        environment={
            'BOT_USER_TOKEN': secrets['botUserToken']
        }
    )
