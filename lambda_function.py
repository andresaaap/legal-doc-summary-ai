import json
import boto3
import os
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # Replace with your AWS region
)

def lambda_handler(event, context):
    # Get the bucket name and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Download the document from S3 to the /tmp directory
    download_path = f'/tmp/{object_key}'
    try:
        s3_client.download_file(bucket_name, object_key, download_path)
    except ClientError as e:
        print(f"Error downloading file from S3: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error downloading file from S3.')
        }

    # Read the document content
    try:
        with open(download_path, 'r') as file:
            document_content = file.read()
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return {
            'statusCode': 404,
            'body': json.dumps('File not found.')
        }

    print("Document Content:", document_content)

    # Create a multi-line prompt
    prompt = f"""
    Please summarize the following legal document. Focus on the main points, key clauses, and any important dates or figures mentioned. The summary should be concise and easy to understand.

    Legal Document:
    {document_content}

    Summary:
    """

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    summary = ""
    
    # Create a summary using AWS Bedrock
    try:
        request_body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31", 
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0,
            "top_p": 0.1,
        })
        print("Request Body:", request_body)
        
        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
            contentType='application/json',
            accept='application/json',
            body=request_body
        )
        
        response_body = response['body'].read()
        print("Response Body:", response_body)
        
        summary = json.loads(response_body)['content'][0]["text"]
        print("Summary:", summary)
        
    except Exception as e:
        print(f"Error invoking model: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error invoking model.')
        }
    
    # Upload the summary to the 'summaries' S3 bucket
    summary_key = f'summary_{object_key}.txt'
    try:
        s3_client.put_object(
            Bucket='summaries-docs-bucket-020125',
            Key=summary_key,
            Body=summary
        )
        print(f"Summary uploaded to S3 bucket 'summaries' with key '{summary_key}'")
    except ClientError as e:
        print(f"Error uploading summary to S3: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error uploading summary to S3.')
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps('Summary created and uploaded successfully!')
    }