Instructions to run the code:

1) clone the repo and change working directory to image_processor folder
   
    `git clone <url> && cd image_processor'

3) create virtual python environment
    `python3 -m venv myvenv`

4) activate the environment
    `./myvenv/scripts/activate   #windows`
    `source myvenv/bin/activate  #macOS/linux`

5) Install dependencies
    pip install -r requirements.txt

6) change directory to image_processor
    cd image_processor

7) run the django server
    python manage.py runserver

8) run the celery 
    celery -A image_processor worker -l info

TESTING

try api collection aftre starting the server
Postman API collection: https://gold-comet-628112.postman.co/workspace/dfghdjfkgm~a318d5c9-1560-4a4a-98ac-67ee0fc4b586/collection/13311764-67875dea-a58a-4c33-a871-0680432046b8?action=share&creator=13311764


API DOCUMENTATION

--------------------------- UPLOAD API ----------------------------
RegisterView API
Endpoint: `/upload/`

Method: `POST`

Description: Upload a CSV file containing product information and image URLs. The system validates the CSV, stores the data, and asynchronously processes the images.

Request
Header :{
    - Content-Type: multipart/form-data
}
Body :
    - 'file' : The CSV file to be uploaded. It should contain columns Serial Number, Product Name, and Input Image Urls.


Response:
- Success (200 OK): Returns a unique request_id that can be used to track the status of the image processing.
{
  "request_id": "123e4567-e89b-12d3-a456-426614174000"
}

- Error:
    - file not provided
    - CSV validation failed
    - Internal server error

--------------------------- GET STATUS API ----------------------------
Get Status API
Endpoint: `/status/<request_id>/`

Method: `GET`

Description: Check the status of the image processing request using the request_id returned by the upload API.

Request
    Headers:
    - Content-Type: application/json
    
    Parameters:
    - request_id: UUID of the processing request.


Response:
- Success (200 OK):
    {
    "request_id": "1ded0e1c-83a5-4a4f-bcd8-2871bc0b9299",
    "status": "Completed",
    "images_processed": 14,
    "images_total": 14
    }

    or 
    {
    "request_id": "1ded0e1c-83a5-4a4f-bcd8-2871bc0b9299",
    "status": "Pending",
    "images_processed": 1,
    "images_total": 14
    }

- Error:
    - Wrong Request ID
