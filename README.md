# TaskRDI

Here's a set of example API requests for each endpoint in your Django project. These examples assume you're using `curl` for making the requests.

### 1. Upload a File
**Endpoint**: `POST /api/upload/`

**Example**:
```bash
curl -X POST http://localhost:8000/api/upload/ \
-H "Content-Type: application/json" \
-d '{
    "file": "<base64_encoded_file_data>",
    "file_type": "image"
}'
```
Replace `<base64_encoded_file_data>` with the actual base64-encoded file data.

### 2. List All Uploaded Files
**Endpoint**: `GET /api/upload/all/`

**Example**:
```bash
curl -X GET http://localhost:8000/api/upload/all/
```

### 3. Delete a File by ID
**Endpoint**: `DELETE /api/upload/delete/<id>/`

**Example**:
```bash
curl -X DELETE http://localhost:8000/api/upload/delete/1/
```

### 4. List All Uploaded Images
**Endpoint**: `GET /api/images/`

**Example**:
```bash
curl -X GET http://localhost:8000/api/images/
```

### 5. List All Uploaded PDFs
**Endpoint**: `GET /api/pdfs/`

**Example**:
```bash
curl -X GET http://localhost:8000/api/pdfs/
```

### 6. Get Image Metadata by ID
**Endpoint**: `GET /api/images/<id>/`

**Example**:
```bash
curl -X GET http://localhost:8000/api/images/1/
```

### 7. Get PDF Metadata by ID
**Endpoint**: `GET /api/pdfs/<id>/`

**Example**:
```bash
curl -X GET http://localhost:8000/api/pdfs/1/
```

### 8. Delete an Image by ID
**Endpoint**: `DELETE /api/images/<id>/delete/`

**Example**:
```bash
curl -X DELETE http://localhost:8000/api/images/1/delete/
```

### 9. Delete a PDF by ID
**Endpoint**: `DELETE /api/pdfs/<id>/delete/`

**Example**:
```bash
curl -X DELETE http://localhost:8000/api/pdfs/1/delete/
```

### 10. Rotate an Image
**Endpoint**: `POST /api/rotate/`

**Example**:
```bash
curl -X POST http://localhost:8000/api/rotate/ \
-H "Content-Type: application/json" \
-d '{
    "image_id": 1,
    "angle": 90
}'
```

### 11. Convert PDF to Single Image
**Endpoint**: `POST /api/convert-pdf-to-image/`

**Example**:
```bash
curl -X POST http://localhost:8000/api/convert-pdf-to-image/ \
-H "Content-Type: application/json" \
-d '{
    "pdf_id": 1
}'
```

### Notes:
- Ensure the server is running and accessible at `http://localhost:8000/`.
- Replace `localhost:8000` with your actual server URL if different.
- Replace `<id>` with the appropriate file or metadata ID in the `DELETE`, `GET`, and `POST` requests.
- The project has been deployed on **[PythonAnywhere](https://mahmoudismail.pythonanywhere.com/)** and is accessible at the following URL:  
  **https://mahmoudismail.pythonanywhere.com/**
- If needed, I can replace all instances of **`http://localhost:8000/`** with **`https://mahmoudismail.pythonanywhere.com/`** to ensure the project is accessible from the live deployment URL.