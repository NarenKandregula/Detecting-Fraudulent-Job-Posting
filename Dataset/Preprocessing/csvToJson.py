import pandas as pd

# Load the CSV file
df = pd.read_csv('my_data.csv')

# Convert the DataFrame to JSON
json_data = df.to_json(orient='records')

# Print JSON output
# print(json_data)

# Optionally, save the JSON to a file
with open('public/features.json', 'w') as json_file:
    json_file.write(json_data)
