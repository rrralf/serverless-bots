import subprocess
import os
import shutil

from aws_cdk import CfnOutput
from aws_cdk import Stack
from aws_cdk import aws_lambda
from aws_cdk import aws_apigatewayv2 as apigwv2
from aws_cdk import aws_apigatewayv2_integrations as integrations

from constructs import Construct


class TelebotPrototypeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        name_prefix = "proto-bot"
        temp_files_prefix = '../.aws-temp'

        ######
        # prepare lambda layers
        # 1. bot-logic layer
        bot_logic_layer = self.make_bot_logic_layer(name_prefix, temp_files_prefix)
        requirements_layer = self.make_requirements_layer(name_prefix, temp_files_prefix)


        ######
        # prepare lambda handler
        lambda_name = f'{name_prefix}-webhook-lambda'
        source_file = '../src/lambda_entry_point.py'
        destination_dir = f'{temp_files_prefix}/{lambda_name}'

        # Create the temporary directory if it doesn't exist
        os.makedirs(destination_dir, exist_ok=True)

        # Copy the specific file to the temporary directory
        shutil.copy(source_file, destination_dir)

        ########################
        # create webhook lambda
        webhook_lambda = aws_lambda.Function(
            self, lambda_name,
            function_name=lambda_name,
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler='lambda_entry_point.lambda_handler',
            code=aws_lambda.Code.from_asset(f'{temp_files_prefix}/{lambda_name}'),
            layers=[ bot_logic_layer, requirements_layer ],
            environment={
                "BOT_TOKEN": "<put-your-telegram-bot-token-here>"
            }
        )

        #######
        # Define the HTTP API
        http_api = apigwv2.HttpApi(
            self, f"{name_prefix}-http-api",
            api_name=f"{name_prefix}-http-api",
            description=f'HTTP API {name_prefix}'
        )

        # Create Lambda integration
        lambda_integration = integrations.HttpLambdaIntegration(f"{name_prefix}-webhook-lambda-integration",
            handler=webhook_lambda
        )

        # Add a route to the HTTP API
        http_api.add_routes(
            path='/webhook',
            methods=[
                apigwv2.HttpMethod.GET,
                apigwv2.HttpMethod.POST
            ],
            integration=lambda_integration
        )

        # Output the URL of the HTTP API
        CfnOutput(
            self, 'HTTP API URL',
            value=http_api.url,
            description='The URL of the HTTP API'
        )

        # done

    def make_bot_logic_layer(self, name_prefix, temp_files_prefix):
        # Paths
        layer_source_dir = '../src/bot_logic'
        layer_destination_dir = f'{temp_files_prefix}/bot-logic-layer'

        # Create the temporary directories if they don't exist
        os.makedirs(layer_destination_dir, exist_ok=True)

        # Copy the layer directory to the temporary directory
        shutil.copytree(layer_source_dir, f"{layer_destination_dir}/python/bot_logic", dirs_exist_ok=True)

        # Define the Lambda layer
        bot_logic_layer = aws_lambda.LayerVersion(
            self, f'{name_prefix}-bot-logic-layer',
            layer_version_name=f'{name_prefix}-bot-logic-layer',
            code=aws_lambda.Code.from_asset(layer_destination_dir),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_12],
            description='Bot logic layer for telegram lambda'
        )

        return bot_logic_layer

    def make_requirements_layer(self, name_prefix, temp_files_prefix):
        # Paths
        layer_destination_dir = f'{temp_files_prefix}/requirements-layer'

        # Create the temporary directories if they don't exist
        os.makedirs(layer_destination_dir, exist_ok=True)

        # Paths
        layer_dir = f'{layer_destination_dir}/python/lib/python3.12/site-packages'

        # Ensure the directory exists
        os.makedirs(layer_dir, exist_ok=True)

        # Install the dependencies into the layer directory
        subprocess.check_call([
            'pip', 'install', '-r', '../src/requirements-lambda.txt', '-t', layer_dir
        ])

        # Define the Lambda layer
        requirements_layer = aws_lambda.LayerVersion(
            self, f'{name_prefix}-requirements-layer',
            layer_version_name=f'{name_prefix}-requirements-layer',
            code=aws_lambda.Code.from_asset(layer_destination_dir),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_12],
            description='misc requirements telegram lambda'
        )

        return requirements_layer
