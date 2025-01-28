import requests

url = "http://localhost:3000/api/upload"

file_path = "assets/image/1738003088366.jpg"

with open(file_path, "rb") as image_file:
    form_data = {
        "farmer_id" : "782-129-491-212",
        "latitude" : "12.34",
        "longitude" : "56.78"
    }
    file_data = {
        "image": ("1738003088366.jpg", image_file, "image/jpeg") 
    }
    response = requests.post(url, data=form_data, files=file_data)

print(response.status_code)
print(response.json())
