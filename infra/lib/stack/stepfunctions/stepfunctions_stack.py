from aws_cdk import core
from aws_cdk.aws_ecr import Repository
from aws_cdk.aws_events import Schedule, Rule, RuleTargetInput
from aws_cdk.aws_events_targets import SfnStateMachine
from aws_cdk.aws_stepfunctions import Fail, Succeed, StateMachine, Errors
from aws_cdk.aws_stepfunctions_tasks import LambdaInvoke

from lib.stack.stepfunctions.resources.function.get_forecast_resource import get_get_forecast_resource
from lib.stack.stepfunctions.resources.function.send_message_resource import get_send_message_resource
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

        fail_task = Fail(self, 'FailTask', comment='failed.')
        succeed_task = Succeed(self, 'SucceedTask', comment='succeeded.')

        get_forecast_function = get_get_forecast_resource(self, repo)
        send_message_function = get_send_message_resource(self, repo)

        get_forecast_task = LambdaInvoke(self,
                                         'GetForecastTask',
                                         lambda_function=get_forecast_function,
                                         input_path='$',
                                         result_path='$.get_forecast_task',
                                         output_path='$',
                                         payload_response_only=True)
        get_forecast_task.add_catch(fail_task,
                                    errors=[Errors.ALL],
                                    result_path='$.error_info')

        send_message_task = LambdaInvoke(self,
                                         'SendMessageTask',
                                         lambda_function=send_message_function,
                                         input_path='$.get_forecast_task.body',
                                         result_path='$.send_message_function',
                                         output_path='$',
                                         payload_response_only=True)
        send_message_task.add_catch(fail_task,
                                    errors=[Errors.ALL],
                                    result_path='$.error_info')

        state_machine = StateMachine(self,
                                     id='StateMachine',
                                     state_machine_name=stack_util.get_upper_name('STATE-MACHINE'),
                                     definition=get_forecast_task
                                     .next(send_message_task)
                                     .next(succeed_task))

        rule = Rule(self, 'StateMachineRule',
                    description='invoking state machine',
                    rule_name=stack_util.get_upper_name('INVOKE-STATE-MACHINE'),
                    schedule=Schedule.cron(
                        hour='19',
                        minute='0',
                    ))

        target = SfnStateMachine(state_machine,
                                 input=RuleTargetInput.from_object({'city': '130010'}))
        rule.add_target(target)
