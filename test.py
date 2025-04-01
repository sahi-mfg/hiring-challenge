import requests

url = "https://api.brightdata.com/datasets/v3/trigger"
headers = {
    "Authorization": "Bearer 24b31a688980a430608bd47daed8f3f5e4b28766b75deb65898b326f5daee952",
}
params = {
    "dataset_id": "gd_lyy3tktm25m4avu764",
    "include_errors": "true",
}
files = {"data": ("data.csv", open("path/to/your/file.csv", "rb"), "text/csv")}

response = requests.post(url, headers=headers, params=params, files=files)
print(response.json())
