import boto3
import csv
from botocore.exceptions import ClientError

def create_dynamodb_table(table_name):
    """Create a DynamoDB table."""
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'job_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'job_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Creating table {table_name}...")
        table.wait_until_exists()
        print(f"Table {table_name} created successfully.")
        return table
    except ClientError as e:
        print(f"Error creating table: {e}")
        return None

def upload_csv_to_dynamodb(csv_file_path, table_name):
    """Upload CSV data to DynamoDB."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Open the CSV file with UTF-8 encoding
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert job_id to string if it's not
            row['job_id'] = str(row['job_id'])
            try:
                table.put_item(Item=row)
                print(f"Inserted row: {row}")
            except ClientError as e:
                print(f"Error inserting row: {e}")
    
    print("CSV data upload complete.")

    
    print("CSV data upload complete.")

# Replace with your details
csv_file_path = 'fake_job_postings.csv'  # Path to your CSV file
table_name = 'JobPostings'

# Create table and upload data
dynamodb_table = create_dynamodb_table(table_name)
if dynamodb_table:
    upload_csv_to_dynamodb(csv_file_path, table_name)
