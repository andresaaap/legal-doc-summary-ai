# Legal Document Summary AI

This project uses AWS services to summarize legal documents. The solution leverages AWS S3 for storage, AWS Lambda for processing, and AWS Bedrock for generating summaries using the Claude LLM.

## Architecture

1. **AWS S3**: Stores the uploaded legal documents and the generated summaries.
2. **AWS Lambda**: Processes the documents and generates summaries.
3. **AWS Bedrock**: Provides the Claude LLM to create the summaries.

### Architecture Diagram

You can find the architecture diagram of the solution in the `images` folder with the name `architecture_diagram.png`.

### Project Review Screenshots

You can find the screenshots of the project review in the `images` folder.

## Prerequisites

- AWS account with necessary permissions.
- Python 3.13 or higher.

## Setup

1. Clone the repository:

```bash
git clone
```

2. Run the cloudformation script to create the stack:

Create a .zip file of the lambda function code.

Create a bucket and upload the .zip file to the bucket.

Change the Permissions: Use the chmod command to add execute permissions to the script.

chmod +x ./create.sh

```bash
./create.sh <stack-name> <template-file> <parameters-file> <region>
```

3. Upload a legal document to the S3 bucket created by the CloudFormation stack.

4. The Lambda function will process the document and generate a summary using the Claude LLM.

5. The summary will be stored in the S3 bucket.

6. Delete the stack after testing:

chmod +x ./delete.sh

```bash
./delete.sh <stack-name>
```

## Questions

### How would you further optimize your solution if your storage costs become prohibitively expensive?
To optimize the solution and reduce storage costs, I can use the following strategies:

1. Data Lifecycle Management
Implement S3 lifecycle policies to automatically transition objects to less expensive storage classes or delete them after a certain period. Move older documents and summaries to S3 Standard-IA (Infrequent Access) or S3 Glacier for long-term storage at a lower cost. Set expiration policies to automatically delete documents and summaries that are no longer needed after a certain period.

2. Compression
Compress the documents before uploading them to S3. This reduces the storage size and costs.

Compression Libraries: Use libraries like gzip or bzip2 to compress files before uploading

3. Deduplication
Implement deduplication to avoid storing multiple copies of the same document.

Hashing: Use hashing to detect duplicate files before uploading

4. Optimize Data Storage
Store only essential data and remove unnecessary metadata or redundant information.

Selective Storage: Store only the necessary parts of the document or summary.

5. Cost Monitoring and Alerts
Set up cost monitoring and alerts to keep track of your storage costs and take action when costs exceed a certain threshold.

AWS Budgets: Use AWS Budgets to set custom cost and usage budgets and receive alerts.

6. Use Reserved Instances for Lambda
If your Lambda function usage is predictable, consider using Reserved Instances to reduce costs.

7. Optimize Lambda Execution
Ensure that your Lambda function is optimized to reduce execution time and memory usage, which can indirectly reduce costs

### How would you further optimize your solution if your model inference costs become prohibitively expensive?

1. Batch Processing
Batch multiple documents together and process them in a single inference request. This can reduce the number of API calls and make better use of the model's capacity.

2. Optimize Prompt Engineering
Ensure that your prompts are concise and efficient. Avoid unnecessary text in the prompt to reduce the token count, which can lower inference costs.

3. Use a Smaller Model
If possible, use a smaller and less expensive model that still meets your accuracy requirements. AWS Bedrock may offer different models with varying costs.

4. Cache Results
Cache the results of frequently requested summaries. If the same document is summarized multiple times, you can store the summary and reuse it instead of making repeated inference requests.

5. Preprocess Documents
Preprocess documents to remove unnecessary content before sending them for summarization. This can reduce the size of the input and the cost of inference.

6. Monitor and Optimize Usage
Set up monitoring to track usage and costs. Analyze the data to identify patterns and optimize usage. For example, you might find that certain times of day are more cost-effective for processing.

7. Use Spot Instances for Lambda
If your workload is flexible, consider using AWS Lambda with spot instances to reduce costs.

