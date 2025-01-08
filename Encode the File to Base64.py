import base64

with open("/home/mahmoud/Downloads/Backend Task (Document Processing)1-1-2025.pdf", "rb") as file:
    encoded_string = base64.b64encode(file.read()).decode('utf-8')
    print(encoded_string)
