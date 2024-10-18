import os
import pandas as pd
import json
from dotenv import load_dotenv

load_dotenv()

def load_csv():
    data_filepath = os.getenv("DATA_FILEPATH")
    csv_file_path = os.path.join(data_filepath, 'tweets.csv')
    return pd.read_csv(csv_file_path), csv_file_path

def generate_llama_jsonl(df):
    system_prompt = "<|start_header_id|>system<|end_header_id|>\n\nCutting Knowledge Date: December 2023\n\nYou are a helpful assistant.\n<|eot_id|>"
    
    def convert_row_llama(row):
        user_prompt = f"<|start_header_id|>user<|end_header_id|>\n\nWrite an Opta-style tweet about the following: {row['Q']}\n<|eot_id|>"
        assistant_response = f"<|start_header_id|>assistant<|end_header_id|>\n\n{row['A']}"
        return {
            "prompt": f"{system_prompt}\n{user_prompt}\n{assistant_response}"
        }
    
    return df.apply(lambda row: json.dumps(convert_row_llama(row)), axis=1)

def save_jsonl(jsonl_data, output_file_name):
    output_dir = os.getenv("DATA_FILEPATH")
    output_file_path = os.path.join(output_dir, output_file_name)
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for entry in jsonl_data:
            f.write(f"{entry}\n")
    
    print(f"JSONL file created: {output_file_path}")

def create_llama_jsonl():
    df, csv_file_path = load_csv()
    
    base_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    output_file_name = f"{base_name}_llama.jsonl"
    
    jsonl_data = generate_llama_jsonl(df)
    
    save_jsonl(jsonl_data, output_file_name)

# Uitvoeren van het script voor Llama als dit direct wordt aangeroepen
if __name__ == "__main__":
    create_llama_jsonl()
