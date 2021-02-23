from aws_cdk import core
from aws_cdk.aws_ecr import IRepository
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode
from aws_cdk.aws_logs import RetentionDays


def get_get_forecast_resource(scope: core.Construct, ecr: IRepository) -> DockerImageFunction:
    return DockerImageFunction(
        scope=scope,
        id='GetForecastFunction',
        function_name='get-forecast',
        code=DockerImageCode.from_ecr(
            repository=ecr,
            tag='get-forecast'
        ),
        log_retention=RetentionDays.ONE_DAY,
    )
