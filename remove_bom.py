import os

def remove_bom_from_csv(input_csv, output_csv):
    """
    Verwijder de BOM (Byte Order Mark) uit een CSV-bestand en sla het op als een nieuw bestand zonder BOM.
    
    Parameters:
    input_csv (str): Het pad naar het originele CSV-bestand met BOM.
    output_csv (str): Het pad waar het nieuwe CSV-bestand zonder BOM moet worden opgeslagen.
    """
    with open(input_csv, mode='r', encoding='utf-8-sig') as infile, open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
        outfile.write(infile.read())
    print(f"BOM verwijderd en nieuwe CSV opgeslagen als: {output_csv}")

if __name__ == "__main__":
    # Specificeer hier het pad naar het originele CSV-bestand en het doelbestand zonder BOM
    input_csv = '/Users/janwillemaltink/developer/twitter_finetune/data/tweets.csv'
    output_csv = '/Users/janwillemaltink/developer/twitter_finetune/data/tweets_no_bom.csv'
    
    # Voer de BOM-verwijdering uit
    if os.path.exists(input_csv):
        remove_bom_from_csv(input_csv, output_csv)
    else:
        print(f"Het opgegeven bestand bestaat niet: {input_csv}")
