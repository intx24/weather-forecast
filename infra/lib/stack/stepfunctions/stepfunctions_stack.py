from aws_cdk import core
from aws_cdk.aws_ecr import Repository

from lib.stack.stepfunctions.resources.function.get_forecast_resource import get_get_forecast_resource
from lib.stack.stepfunctions.resources.function.list_channels_resource import get_list_channels_resource
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
        get_weather_forecast_function = get_get_forecast_resource(self, repo)
        list_channels_function = get_list_channels_resource(self, repo)

        # def get_parallel(self, scope: core.Construct, get_forecast: DockerImageFunction,
        #                  list_channels: DockerImageFunction, fail: Fail) -> Parallel:
        #     get_forecast_task = LambdaInvoke(scope,
        #                                      'GetForecastTask',
        #                                      lambda_function=get_forecast,
        #                                      input_path='$',
        #                                      result_path='$.get_forecast_task',
        #                                      output_path='$',
        #                                      payload_response_only=True)
        #
        #     list_channels_task = LambdaInvoke(scope,
        #                                       'ListChannelsTask',
        #                                       lambda_function=list_channels,
        #                                       input_path='$',
        #                                       result_path='$.list_channels_task',
        #                                       output_path='$',
        #                                       payload_response_only=True)
        #
        #     parallel = Parallel(self, 'ParallelState')
        #     parallel.branch(get_forecast_task)
        #     parallel.branch(list_channels_task)
        #
        #     parallel.add_catch(fail,
        #                        errors=[Errors.ALL],
        #                        result_path='$error_info')

        # return parallel
