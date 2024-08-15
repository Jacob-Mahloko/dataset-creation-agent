import os
import csv
import anthropic

from prompts import *

# set anthropic api key
if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = input("Please enter your anthropic API key: ")\

# create the anthropic client
client = anthropic.Anthropic()
sonnet = "claude-3-5-sonnet-20240620"

def read_csv(file_path):
    dataset = []
    with open(file_path, "r", newline="") as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            dataset.append(row)

    return dataset

def save_to_csv(data, output_file, headers=None):
    mode = 'w' if headers else 'a'
    with open(output_file, mode, newline="") as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for row in csv.reader(data.splitlines()): # split data string into rows
            writer.writerow(row)

# create an analyser agent

def analyser_agent(sample_data):
    message = client.messages.create(
        model = sonnet,
        max_tokens= 400,
        temperature=0.1, # set low temperature for mored focuses, deterministic output
        system=ANALYZER_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)
            }
        ]

    )
    return message.content[0].text

def generator_agent(analysis_result,sample_data,num_rows=30):
    message = client.messages.create(
        model = sonnet,
        max_tokens= 1500,
        temperature=1, # set high temperature for mored creative, non-deterministic output
        system=GENERATOR_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": GENERATOR_USER_PROMPT.format(num_rows=num_rows,analysis_result=analysis_result,sample_data=sample_data)
            }
        ]

    )
    return message.content[0].text


# main execution flow

# get input from the user

file_path = input("\nEnter the name of your csv file: ")
file_path = os.path.join('/app/data',file_path)
desired_rows = int((input("\nNumber of row you want in new dataset: ")))

sample_data = read_csv(file_path)
sample_data_str = "\n".join([",".join(row) for row in sample_data])

print("\nlaunching team of Agents")

analysis_result = analyser_agent(sample_data_str)

print("\#### Analyzer Agent output: ####\n")
print(analysis_result)
print("\n--------------------------------------------------------------------\n\nGenerating new data...")

# set up properties for output file
output_file =  "/app/data/new_dataset.csv"
headers =sample_data[0]

# create the output file with headers
save_to_csv("",output_file,headers)

batch_size = 30
generated_rows = 0 # keep count of number of rows generated

while generated_rows < desired_rows:
    # number of rows to generate in this batch
    rows_to_generate = min(batch_size,desired_rows - generated_rows)

    # generate batch
    generated_data = generator_agent(analysis_result, sample_data_str, rows_to_generate)

    save_to_csv(generated_data, output_file)

    generated_rows +=rows_to_generate

    print(f"Generated {generated_rows} rows out of {desired_rows}")


print(f"\nGenerated data has been saved to {output_file}")