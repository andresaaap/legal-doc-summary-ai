#!/bin/bash

# filepath: /Users/alvaroandrespinzoncortes/Documents/udacity/legal-doc-summary-ai/delete.sh

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <stack-name>"
    exit 1
fi

STACK_NAME=$1

# Delete the CloudFormation stack
echo "Deleting the CloudFormation stack..."
aws cloudformation delete-stack --stack-name $STACK_NAME

if [ $? -ne 0 ]; then
    echo "Failed to delete the stack."
    exit 1
fi

echo "Stack deletion initiated. You can check the status in the AWS Management Console."