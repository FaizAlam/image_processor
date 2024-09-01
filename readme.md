# Instructions to Run the Code

### 1. Clone the repo and Change Directory to `image_processor`
```bash
git clone https://github.com/FaizAlam/image_processor.git && cd image_processor
```

### 2. Create a Virtual Python Environment
```bash
python3 -m venv myvenv
```

### 3. Activate the Environment
- **Windows**:
  ```bash
  .\myvenv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source myvenv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Django Server
```bash
python3 manage.py runserver
```

### 7. Run the Celery Worker
```bash
celery -A image_processor worker -l info
```

# Testing

- After starting the server, you can test the API using the Postman collection:
  - [Postman API Collection](https://gold-comet-628112.postman.co/workspace/dfghdjfkgm~a318d5c9-1560-4a4a-98ac-67ee0fc4b586/collection/13311764-67875dea-a58a-4c33-a871-0680432046b8?action=share&creator=13311764)

# API Documentation

### **UPLOAD API**

**Endpoint**: `/upload/`

**Method**: `POST`

**Description**: Upload a CSV file containing product information and image URLs. The system validates the CSV, stores the data, and asynchronously processes the images.

**Request**:
- **Headers**:
  - `Content-Type: multipart/form-data`
- **Body**:
  - `file`: The CSV file to be uploaded. It should contain columns `Serial Number`, `Product Name`, and `Input Image Urls`.

**Response**:
- **Success** (`200 OK`): Returns a unique `request_id` that can be used to track the status of the image processing.
  ```json
  {
    "request_id": "123e4567-e89b-12d3-a456-426614174000"
  }
  ```
- **Error**:
  - File not provided
  - CSV validation failed
  - Internal server error

### **GET STATUS API**

**Endpoint**: `/status/<request_id>/`

**Method**: `GET`

**Description**: Check the status of the image processing request using the `request_id` returned by the upload API.

**Request**:
- **Headers**:
  - `Content-Type: application/json`
- **Parameters**:
  - `request_id`: UUID of the processing request.

**Response**:
- **Success** (`200 OK`):
  ```json
  {
    "request_id": "1ded0e1c-83a5-4a4f-bcd8-2871bc0b9299",
    "status": "Completed",
    "images_processed": 14,
    "images_total": 14
  }
  ```
  or
  ```json
  {
    "request_id": "1ded0e1c-83a5-4a4f-bcd8-2871bc0b9299",
    "status": "Pending",
    "images_processed": 1,
    "images_total": 14
  }
  ```

- **Error**:
  - Wrong `request_id`

