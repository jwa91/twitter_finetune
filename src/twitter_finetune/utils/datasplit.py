"""
Split een JSONL-bestand in train, valid en test bestanden volgens de gegeven verhoudingen.
De bestanden worden opgeslagen in een map met dezelfde naam als het originele bestand.
"""
import os
import random
from dotenv import load_dotenv

load_dotenv()

def split_jsonl_file(file_path, output_dir, train_ratio=0.6, valid_ratio=0.2, test_ratio=0.2):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    random.shuffle(lines)

    total = len(lines)
    train_end = int(total * train_ratio)
    valid_end = train_end + int(total * valid_ratio)

    train_lines = lines[:train_end]
    valid_lines = lines[train_end:valid_end]
    test_lines = lines[valid_end:]

    base_name = os.path.basename(file_path).split('.')[0]
    output_path = os.path.join(output_dir, base_name)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with open(os.path.join(output_path, 'train.jsonl'), 'w') as f_train:
        f_train.writelines(train_lines)

    with open(os.path.join(output_path, 'valid.jsonl'), 'w') as f_valid:
        f_valid.writelines(valid_lines)

    with open(os.path.join(output_path, 'test.jsonl'), 'w') as f_test:
        f_test.writelines(test_lines)

def main():
    data_dir = os.getenv("DATA_FILEPATH")
    for filename in os.listdir(data_dir):
        if filename.endswith(".jsonl"):
            file_path = os.path.join(data_dir, filename)
            split_jsonl_file(file_path, data_dir)

if __name__ == "__main__":
    main()
