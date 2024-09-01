from celery import shared_task
from .models import Image
import requests
from io import BytesIO
import time


@shared_task
def process_image(image_id):
    try:
        image_obj = Image.objects.get(id=image_id)
        # Dummy processing
        response = requests.get(image_obj.input_url)
        # image = PILImage.open(BytesIO(response.content))

        # output = BytesIO()  # dummy output image, in production we can store it on cloud
        # image.save(output,format='JPEG',quality=50)
        output_url = f"https://dummy-output-url.com/compressed-{image_id}.jpg"

        time.sleep(2)   # to imitate delay in real application
        image_obj.output_url = output_url
        image_obj.status = 'Completed'
        image_obj.save()
    
    except Exception as e:
        image_obj.status = 'Failed'
        image_obj.save()
        raise Exception("Error while processing image {image_id}: {e}")


@shared_task
def test_task(x,y):
    return x+y
