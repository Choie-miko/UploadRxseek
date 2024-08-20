import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import os

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        # Check if the file is in either key 'file' or 'File'
        uploaded_file = request.FILES.get('file') or request.FILES.get('File')

        if uploaded_file:
            # Check if the file is a CSV
            if not uploaded_file.name.endswith('.csv'):
                return JsonResponse({'error': 'Only CSV files are accepted.'}, status=400)

            # Save the file temporarily
            file_path = default_storage.save('temp.csv', uploaded_file)

            # Load the CSV into a DataFrame
            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                os.remove(file_path)
                return JsonResponse({'error': f'Error reading CSV file: {str(e)}'}, status=400)

            # Check for exact column names
            required_columns = {'firstname', 'lastname'}
            if set(df.columns) != required_columns:
                os.remove(file_path)
                return JsonResponse({'error': 'CSV must contain only the columns: firstname, lastname.'}, status=400)

            # File is valid
            os.remove(file_path)
            return JsonResponse({'message': 'File uploaded successfully.'}, status=200)

        return JsonResponse({'error': 'No file provided.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
