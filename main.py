import json
import re
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

endpoint = "https://documentintelligenceinterninstance.cognitiveservices.azure.com/"
key = " "  

formUrl = "https://testing-ecal-publisher-assets.s3.amazonaws.com/intern_ai/AFL_2024_fixture+The+Age.pdf"

def extract_fixtures(text_list):
    fixtures = []
    current_date = None
    current_round = None

    date_pattern = re.compile(r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), \w+ \d{1,2}\b')
    time_pattern = re.compile(r'\b\d{1,2}:\d{2}\w{2}\b')
    round_pattern = re.compile(r'\bRound \d+\b')
    match_pattern = re.compile(r'(.*) vs\. (.*)')  

    for text in text_list:
        if round_pattern.match(text):
            current_round = text
        elif date_pattern.match(text):
            current_date = text
        elif time_pattern.search(text):
            time = time_pattern.search(text).group()
            match = match_pattern.search(text)
            if match:
                team1, team2 = match.groups()
                fixture = {
                    "round": current_round,
                    "date": current_date,
                    "time": time,
                    "team1": team1.strip(),
                    "team2": team2.strip()
                }
                fixtures.append(fixture)

    return fixtures

try:
    document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

    poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-layout", formUrl)
    result = poller.result()

    structured_data = {"pages": []}

    for page in result.pages:
        page_data = {"pageNumber": page.page_number, "text": [], "tables": [], "fixtures": []}

        for line in page.lines:
            page_data["text"].append(line.content)

        page_data["fixtures"] = extract_fixtures(page_data["fixtures"])
        structured_data["pages"].append(page_data)

    json_data = json.dumps(structured_data, indent=4)
    print(json_data)

    with open('extracted_data.json', 'w') as json_file:
        json_file.write(json_data)
        print("----------COMPLETED----------")

except Exception as e:
    print(f"An error occurred: {e}")
