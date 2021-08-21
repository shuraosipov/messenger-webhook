from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_s3 as s3,
                     aws_lambda as lambda_)


class MessengerWebhook(core.Construct):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)

        bucket = s3.Bucket(self, "WidgetStore")

        handler = lambda_.Function(self, "WidgetHandler",
                                   runtime=lambda_.Runtime.PYTHON_3_8,
                                   code=lambda_.Code.from_asset("lambda"),
                                   handler="lambda_function.lambda_handler",
                                   environment=dict(
                                       BUCKET=bucket.bucket_name,
                                       VERIFY_TOKEN=self.node.try_get_context("verify_token")
                                   )
                    )

        bucket.grant_read_write(handler)

        api = apigateway.RestApi(self, "widgets-api",
                                 rest_api_name="Widget Service",
                                 description="This service serves widgets.")

        get_widgets_integration = apigateway.LambdaIntegration(handler,
                                                               request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("GET", get_widgets_integration)   # GET /
        api.root.add_method("POST", get_widgets_integration)
        api.root.add_method("DELETE", get_widgets_integration)

        widget = api.root.add_resource("{id}")

        # Add new widget to bucket with: POST /{id}
        post_widget_integration = apigateway.LambdaIntegration(handler)

        # Get a specific widget from bucket with: GET /{id}
        get_widget_integration = apigateway.LambdaIntegration(handler)

        # Remove a specific widget from the bucket with: DELETE /{id}
        delete_widget_integration = apigateway.LambdaIntegration(handler)

        widget.add_method("POST", post_widget_integration)     # POST /{id}
        widget.add_method("GET", get_widget_integration)       # GET /{id}
        widget.add_method("DELETE", delete_widget_integration)  # DELETE /{id}
