import aws_cdk as core
import aws_cdk.assertions as assertions

from stack.prototype_stack import TelebotPrototypeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in stack/prototype_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TelebotPrototypeStack(app, "stack")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
