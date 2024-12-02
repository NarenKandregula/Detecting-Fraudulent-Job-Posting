import boto3
def get_row_from_dynamodb(table_name, key):
    """Retrieve a row by key."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    response = table.get_item(Key={'job_id': key})
    if 'Item' in response:
        print(f"Retrieved item: {response['Item']}")
        return response['Item']
    else:
        print(f"No item found with ID: {key}")
        return None

# Example retrieval
key_to_retrieve = '12345'  # Replace with a valid ID
table_name = "JobPostings"
get_row_from_dynamodb(table_name, key_to_retrieve)
