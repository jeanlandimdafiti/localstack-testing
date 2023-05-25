import logging
from time import sleep
from typing import Dict
from unittest import TestCase
from uuid import uuid4

import boto3
from botocore.client import BaseClient


class TestStateMachine(TestCase):
    """
    This integration test will execute the step function and verify if the execution is succesful.
    """

    state_machine_arn: str

    client: BaseClient

    @classmethod
    def verify_stack_name(cls) -> str:
        stack_name = "campaign-segmentation-workflow"

        # Verify stack exists
        client = boto3.client("cloudformation")
        try:
            client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name}. \n" f'Please make sure stack with the name "{stack_name}" exists.'
            ) from e

        return stack_name

    @classmethod
    def setUpClass(cls) -> None:
        """
        Here we use cloudformation API to find out:
        - campaign-segmentation-workflow_machine's ARN
        """
        stack_name = TestStateMachine.verify_stack_name()

        client = boto3.client("cloudformation")
        response = client.list_stack_resources(StackName=stack_name)
        resources = response["StackResourceSummaries"]
        state_machine_resources = [
            resource for resource in resources if resource["LogicalResourceId"] == "campaign-segmentation-workflow_machine"
        ]

        if not state_machine_resources:
            raise Exception("Cannot find campaign-segmentation-workflow_machine")

        cls.state_machine_arn = state_machine_resources[0]["PhysicalResourceId"]

    def setUp(self) -> None:
        self.client = boto3.client("stepfunctions")

    def _start_execute(self) -> str:
        """
        Start the state machine execution request and record the execution ARN
        """
        response = self.client.start_execution(
            stateMachineArn=self.state_machine_arn, name=f"integ-test-{uuid4()}", input="{}"
        )
        return response["executionArn"]

    def _wait_execution(self, execution_arn: str):
        while True:
            response = self.client.describe_execution(executionArn=execution_arn)
            status = response["status"]
            if status == "SUCCEEDED":
                logging.info(f"Execution {execution_arn} completely successfully.")
                assert True
                break
            elif status == "RUNNING":
                logging.info(f"Execution {execution_arn} is still running, waiting")
                sleep(3)
            else:
                self.fail(f"Execution {execution_arn} failed with status {status}")
                assert False

    def test_state_machine(self):
        execution_arn = self._start_execute()
        self._wait_execution(execution_arn)
