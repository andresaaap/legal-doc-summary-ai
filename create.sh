#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <stack-name> <template-file> <parameters-file> <region>"
    exit 1
fi

STACK_NAME=$1
TEMPLATE_FILE=$2
PARAMETERS_FILE=$3
REGION=$4

# Validate the template file
echo "Validating the CloudFormation template..."
aws cloudformation validate-template --template-body file://$TEMPLATE_FILE --region $REGION

if [ $? -ne 0 ]; then
    echo "Template validation failed."
    exit 1
fi

# Create the CloudFormation stack
echo "Creating the CloudFormation stack..."
aws cloudformation create-stack --stack-name $STACK_NAME --template-body file://$TEMPLATE_FILE --parameters file://$PARAMETERS_FILE --capabilities CAPABILITY_NAMED_IAM --region $REGION

if [ $? -ne 0 ]; then
    echo "Failed to create the stack."
    exit 1
fi

echo "Stack creation initiated. You can check the status in the AWS Management Console."