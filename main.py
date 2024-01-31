import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


endpoint = "https://documentintelligenceinterninstance.cognitiveservices.azure.com/"
key = "" 

formUrl = "https://testing-ecal-publisher-assets.s3.amazonaws.com/intern_ai/2023-VAFA-Premier-Mens-Fixture.pdf"

try:
  
    document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

    poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-layout", formUrl)
    result = poller.result()

  
    structured_data = {"pages": []}

    for page in result.pages:
        page_data = {"pageNumber": page.page_number, "text": [], "tables": []}

     
        for line in page.lines:
            page_data["text"].append(line.content)

        structured_data["pages"].append(page_data)

    
    for table in result.tables:
      
        pass

    
    json_data = json.dumps(structured_data, indent=4)
    print(json_data)

    print("----------COMPLETED----------")

except Exception as e:
    print(f"An error occurred: {e}")
