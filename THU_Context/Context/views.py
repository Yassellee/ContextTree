from django.http import JsonResponse
import sys, os
from .models import Task
sys.path.append('..')
from Boruta_AllInOne.Boruta import generate_feature_names


def insert_info(request):
    def gen_response(code, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'POST':
        try:
            insert_info = request.FILES['update_file']
        except Exception as e:
            return gen_response(400, "Unable to extract files: {}".format(e))
        def handle_uploaded_file(f):
            previous_folder_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            with open(previous_folder_path+'\\Boruta_AllInOne\\logItems.txt', 'ab+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        handle_uploaded_file(insert_info)

        task_names = Task.objects.values_list('task_name', flat=True).distinct()

        print(task_names)
        
        return_info = generate_feature_names(task_names)

        return gen_response(200, return_info)

    else:
        return gen_response(400, "Bad Request")


def add_task(request):
    def gen_response(code, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'POST':
        try:
            task_names = request.POST['task_name']
            task_names = task_names.split('==')
        except Exception as e:
            return gen_response(400, "Unable to digest post information: {}".format(e))
        try:
            original_task_names = Task.objects.values_list('task_name', flat=True).distinct()
            for task_name in task_names:
                if task_name not in original_task_names:
                    task = Task(task_name=task_name)
                    task.save()
            return gen_response(200, "Add task successfully!")
        except Exception as e:
            return gen_response(400, "Error when inserting name into database: {}".format(e))

    else:
        return gen_response(400, "Bad Request")


def clean_database(request):
    def gen_response(code, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'POST':
        try:
            task_names = request.POST['task_name']
            task_names = task_names.split('==')
        except Exception as e:
            return gen_response(400, "Unable to digest post information: {}".format(e))
        try:
            for task_name in task_names:
                task = Task.objects.filter(task_name=task_name)
                if task:
                    task.delete()
            return gen_response(200, "Delete task successfully!")
        except Exception as e:
            return gen_response(400, "Error when deleting name from database: {}".format(e))

    else:
        return gen_response(400, "Bad Request")
