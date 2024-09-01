import csv
from django.core.exceptions import ValidationError

REQUIRED_FIELDS = ['S. No.', 'Product Name', 'Input Image Urls']
def validate_csv(decoded_file):
    '''
    Validates the csv file to ensure it has correct format and content

    :param file: The uploaded CSV file
    :raises ValidationError: if the file does not meet the validation criteria
    '''
    try:
        reader = csv.DictReader(decoded_file)
        header = reader.fieldnames

        if not all(column in header for column in REQUIRED_FIELDS):
            raise ValidationError(f"CSV must contain the following fields: {', '.join(REQUIRED_FIELDS)}")
        
        #validating row data
        for row in reader:
            serial_number = row.get(REQUIRED_FIELDS[0])
            product_name = row.get(REQUIRED_FIELDS[1])
            input_image_urls = row.get(REQUIRED_FIELDS[2])

            # Validate Serial Number
            if not serial_number.isdigit():
                raise ValidationError(f"Invalid Serial Number: {serial_number}")

            # Validate Product Name
            if not product_name or len(product_name.strip()) == 0:
                raise ValidationError("Product Name cannot be empty")

            # Validate Input Image URLs
            if not input_image_urls or len(input_image_urls.strip()) == 0:
                raise ValidationError("Input Image URLs cannot be empty")

            # Split and validate each URL
            urls = input_image_urls.split(',')
            for url in urls:
                url = url.strip()
                if not url.startswith("http://") and not url.startswith("https://"):
                    raise ValidationError(f"Invalid URL format: {url}")
                
    except csv.Error as e:
        raise ValidationError(f"Error reading CSV file: {str(e)}")
    except UnicodeDecodeError:
        raise ValidationError("CSV file must be in UTF-8 format")
    
    return True