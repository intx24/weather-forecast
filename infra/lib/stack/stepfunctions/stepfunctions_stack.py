from aws_cdk import core
from aws_cdk.aws_ecr import Repository

from lib.stack.stepfunctions.resources.function.get_weather_forecast_resource import get_get_weather_forecast_resource
from lib.util.stack_util import StackUtil


class StepFunctionsStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stack_util = StackUtil()
        repo = Repository.from_repository_attributes(
            scope=self,
            id='FunctionRepository',
            repository_name=stack_util.get_name('repo'),
            repository_arn=f'arn:aws:ecr:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:repository/{stack_util.get_name("repo")}'
        )
        get_weather_forecast_function = get_get_weather_forecast_resource(self, repo)
