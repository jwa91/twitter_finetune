"""
dataprep.py

Dit script converteert een CSV-bestand met query's en antwoorden naar een JSONL-formaat, geschikt voor het finetunen van verschillende large language models (LLMs), zoals LLaMA en Mistral. De CSV-bestanden worden gelezen vanuit een directory die wordt gespecificeerd in een .env-bestand, en de gegenereerde JSONL-bestanden worden in dezelfde directory opgeslagen.

Gebruik:

    create_jsonl <model>

Waarbij <model> kan zijn:
    - "llama": Converteert de CSV naar het JSONL-formaat voor finetuning van een LLaMA-model.
    - "mistral": Converteert de CSV naar het JSONL-formaat voor finetuning van een Mistral-model.
"""


import csv
import json
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

data_filepath = os.getenv('DATA_FILEPATH')
input_csv_path = os.path.join(data_filepath, 'tweets.csv')
output_jsonl_path_llama = os.path.join(data_filepath, 'tweets-llama.jsonl')
output_jsonl_path_mistral = os.path.join(data_filepath, 'tweets-mistral.jsonl')

# LLaMA
def create_llama_jsonl(input_csv, output_jsonl):
    with open(input_csv, mode='r', encoding='utf-8') as csvfile, open(output_jsonl, mode='w', encoding='utf-8') as jsonlfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            query = row['Query']
            answer = row['Answer']
            jsonl_data = {
                "text": f"<|start_header_id|>system<|end_header_id|> Cutting Knowledge Date: December 2023 Write an Opta-style tweet about the following:<|eot_id|> <|start_header_id|>user<|end_header_id|> {query}<|eot_id|> <|start_header_id|>assistant<|end_header_id|> {answer}<|eot_id|>"
            }
            jsonlfile.write(json.dumps(jsonl_data) + '\n')

# Mistral
def create_mistral_jsonl(input_csv, output_jsonl):
    with open(input_csv, mode='r', encoding='utf-8') as csvfile, open(output_jsonl, mode='w', encoding='utf-8') as jsonlfile:
        csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')

        for row in csv_reader:
            try:
                query = row['Query'].strip()
                answer = row['Answer'].strip()
            except KeyError as e:
                raise KeyError(f"Kolom niet gevonden: {e}")

            jsonl_data = {
                "text": f"[INST] Write an Opta-style tweet about the following: {query}[/INST]{answer}"
            }
            jsonlfile.write(json.dumps(jsonl_data) + '\n')

def main():
    parser = argparse.ArgumentParser(description="Convert CSV to JSONL for finetuning LLaMA or Mistral")
    parser.add_argument(
        "model",
        type=str,
        choices=["llama", "mistral"],
        help="Specify whether to create JSONL for 'llama' or 'mistral'"
    )
    args = parser.parse_args()

    if args.model == "llama":
        create_llama_jsonl(input_csv_path, output_jsonl_path_llama)
    elif args.model == "mistral":
        create_mistral_jsonl(input_csv_path, output_jsonl_path_mistral)

if __name__ == "__main__":
    main()
