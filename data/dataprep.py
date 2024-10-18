import os
import pandas as pd
import json

def csv_to_jsonl(csv_file_path):
    df = pd.read_csv(csv_file_path)

    base_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    
    output_file_path = f"{base_name}.jsonl"
    
    def convert_to_jsonl_llama(row):
        system_prompt = "<|start_header_id|>system<|end_header_id|>\n\nCutting Knowledge Date: December 2023\n\nYou are a helpful assistant.\n<|eot_id|>"
        user_prompt = f"<|start_header_id|>user<|end_header_id|>\n\nSchrijf een Opta-style tweet over het volgende feitje: {row["Q"]}\n<|eot_id|>"
        assistant_response = f"<|start_header_id|>assistant<|end_header_id|>\n\n{row["A"]}"
        
        jsonl_entry = {
            "prompt": f"{system_prompt}\n{user_prompt}\n{assistant_response}"
        }
        return json.dumps(jsonl_entry)

    jsonl_data = df.apply(convert_to_jsonl_llama, axis=1)
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for entry in jsonl_data:
            f.write(f"{entry}\n")
    
    print(f"JSONL file created: {output_file_path}")
    
csv_to_jsonl('data/tweets.csv')
