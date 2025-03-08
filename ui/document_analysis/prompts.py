simple_json_extract = """
Extract structured data from the following document and return it in valid JSON format. The JSON should only include these specific fields:
- name: Name of the facility/building
- square_feet: Total square footage of the facility
- number_of_employees: Number of employees working in the facility
- power_consumption: Power consumption details
- water_source: Source of water supply
- waste_disposal: Waste management and disposal methods

TEXT:
{text}

Return **only** the extracted information as a well-formatted JSON object with the above fields. If a field's information is not found in the text, use null as the value. Do not include any additional text or markdown code blocks in the response.

Example format:
{
    "name": "Facility name",
    "square_feet": 50000,
    "number_of_employees": 100,
    "power_consumption": "500 kW per month",
    "water_source": "Municipal water supply",
    "waste_disposal": "On-site recycling and municipal waste collection"
}
""" 