import boto3
from utils.colors import Colors

# Create a CloudFormation client
cf = boto3.client('cloudformation')

def delete_stack(stack_name):
    try:
        print(Colors.blue(f"Attempting to delete CloudFormation stack: {stack_name}..."))
        
        response = cf.delete_stack(
            StackName=stack_name
        )
        
        print(Colors.green(f"Stack {stack_name} deletion initiated successfully!"))
        return response

    except Exception as e:
        print(Colors.red(f"Error occurred while deleting stack {stack_name}: {e}"))
        return None

# Specify CloudFormation stack name here
stack_name = 'frontend-pipeline'

# Call the function to delete the stack
delete_stack(stack_name)
