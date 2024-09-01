from django.views import View
from django.http import JsonResponse
from .models import Request, Image
import csv
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from processing.tasks import process_image
from processing.utils import validate_csv
from django.core.exceptions import ValidationError


@method_decorator(csrf_exempt, name='dispatch')
class UploadCSV(View):
    def post(self, request, *args, **kwargs):
        
        try:
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            validate_csv(decoded_file)
            reader = csv.DictReader(decoded_file)
            
            # Create a new request
            new_request = Request.objects.create()
        
            for row in reader:
                product_name = row['Product Name']
                input_urls = row['Input Image Urls'].split(',')

                for url in input_urls:
                    img = Image.objects.create(request=new_request, input_url=url, product_name=product_name)
                    process_image.apply_async(args=[img.id], countdown=60)

            
            return JsonResponse({'request_id': new_request.request_id})
            # return JsonResponse({'success':"done"})
        
        except Exception as e:
            return JsonResponse({'error':str(e)}, status=400)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'GET method not allowed'}, status=405)


class CheckStatus(View):
    def get(self, request, request_id, *args, **kwargs):
        try:
            req = Request.objects.get(request_id=request_id)
            images = req.images.all()
            processed_images = req.images.filter(status__in=['Completed'])

            # Check if all images are processed
            all_processed = True
            if images.count() > processed_images.count():
                all_processed = False

            if not all_processed:
                response = {
                'request_id': str(req.request_id),
                'status': req.status,
                'images_processed': processed_images.count(),
                'images_total':images.count(),

                }
                return JsonResponse(response)
   
            req.status = 'Completed'
            req.save()

            response = {
                'request_id': str(req.request_id),
                'status': req.status,
                'images_processed': processed_images.count(),
                'images_total':images.count(),
            }

            return JsonResponse(response)
            
        except Request.DoesNotExist:
            return JsonResponse({'error': 'Request not found'}, status=404)
    
        except Exception as e:
            return JsonResponse({'error':str(e)}, status=500)
