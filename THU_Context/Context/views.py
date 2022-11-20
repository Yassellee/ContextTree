from django.http import JsonResponse
import sys, os, json, threading
from .models import Task, Key
sys.path.append('..')
from Boruta_AllInOne.Boruta import generate_feature_names
from openai_toolkit.openai_toolkit import openai_toolkit
from utils.calculate_rec_score import calculate_rec_score


current_valid_key = "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"


def insert_info(request):
    def gen_response(code, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'POST':
        try:
            insert_info = request.FILES['file']
            username = request.POST['user']
        except Exception as e:
            return gen_response(400, "Unable to extract files: {}".format(e))
        def handle_uploaded_file(f):
            previous_folder_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            with open(previous_folder_path+'/Boruta_AllInOne/data/{}/logItems.txt'.format(username), 'ab+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        def delete_useless_lines():
            previous_folder_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            with open(previous_folder_path+'/Boruta_AllInOne/data/{}/logItems.txt'.format(username), 'r') as f:
                lines = f.readlines()
            with open(previous_folder_path+'/Boruta_AllInOne/data/{}/logItems.txt'.format(username), 'w') as f:
                for line in lines:
                    line_data = line.split('##')
                    if line_data[1] == "package" or line_data[1] == "task":
                        f.write(line)

        def thread_function():
            generate_feature_names(task_names, username)

        # check if folder exists
        previous_folder_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        if not os.path.exists(previous_folder_path+'/Boruta_AllInOne/data/{}'.format(username)):
            os.makedirs(previous_folder_path+'/Boruta_AllInOne/data/{}'.format(username))
        handle_uploaded_file(insert_info)

        delete_useless_lines()

        task_names = Task.objects.values_list('task_name', flat=True).distinct()

        task_names = list(set(task_names))

        if not os.path.exists(previous_folder_path+'/Boruta_AllInOne/data/{}/feature.json'.format(username)):
            with open(previous_folder_path+'/Boruta_AllInOne/data/{}/feature.json'.format(username), 'w') as f:
                # create an empty dict, key will be task name, value will be a list of feature names
                feature_dict = {}
                for task_name in task_names:
                    feature_dict[task_name] = []
                json.dump(feature_dict, f, indent=4, ensure_ascii=False)

        thread_to_generate_feature_names = threading.Thread(target=thread_function)
        thread_to_generate_feature_names.start()

        with open(previous_folder_path+'/Boruta_AllInOne/data/{}/feature.json'.format(username), 'r') as f:
            feature_names = json.load(f)

        return gen_response(200, feature_names)

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

def get_task(request):
    def gen_response(code, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'GET':
        try:
            task_names = Task.objects.values_list('task_name', flat=True).distinct()
            task_names = list(set(task_names))
            return gen_response(200, task_names)
        except Exception as e:
            return gen_response(400, "Error when getting task names from database: {}".format(e))

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


def get_completion(request):
    def gen_response(code, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'POST':
        try:
            prompt = request.POST['prompt']
            try:
                key = request.POST['key']
            except:
                key = current_valid_key
            try:
                engine = request.POST['engine']
            except:
                engine = "ada"
            try:
                temperature = request.POST['temperature']
            except:
                temperature = 0.5
        except Exception as e:
            return gen_response(400, "Unable to digest post information: {}".format(e))
        try:
            openai_toolkit_instance = openai_toolkit(api_key = key, engine = engine, temperature = temperature)
            completion = openai_toolkit_instance.get_completion(prompt)
            return gen_response(200, completion)
        except Exception as e:
            return gen_response(400, "Error when getting completion from openai: {}".format(e))

    else:
        return gen_response(400, "Bad Request")


def delete_logitems(request):
    def gen_response(code, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'POST':
        username = request.POST['user']
        try:
            previous_folder_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            with open(previous_folder_path+'/Boruta_AllInOne/logItems_{}.txt'.format(username), 'w') as f:
                f.truncate()
            return gen_response(200, "Delete logItems successfully!")
        except Exception as e:
            return gen_response(400, "Error when deleting logItems: {}".format(e))

    else:
        return gen_response(400, "Bad Request")

def calculate_score(request):
    def gen_response(code, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'POST':
        try:
            rule_based_dict = request.POST['rule_based_dict']
            feature_based_dict = request.POST['feature_based_dict']
            current_context_dict = request.POST['current_context_dict']
        except Exception as e:
            return gen_response(400, "Unable to digest post information: {}".format(e))
        try:
            rule_based_dict = json.loads(rule_based_dict)
            feature_based_dict = json.loads(feature_based_dict)
            current_context_dict = json.loads(current_context_dict)
            score = calculate_rec_score(rule_based_dict, feature_based_dict, current_context_dict)
            return gen_response(200, score)
        except Exception as e:
            return gen_response(400, "Error when calculating score: {}".format(e))


def add_key(request):
    def gen_response(code, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'POST':
        try:
            key = request.POST['key']
        except Exception as e:
            return gen_response(400, "Unable to digest post information: {}".format(e))
        try:
            # if key not in database, add key
            query_list = Key.objects.values_list('key_name', flat=True).distinct()
            key_list = list(set(query_list))
            if key not in key_list:
                new_key = Key(key_name=key)
                new_key.save()
            return gen_response(200, "Added key successfully! {}".format(key))
        except Exception as e:
            return gen_response(400, "Error when inserting key into database: {}".format(e))

    else:
        return gen_response(400, "Bad Request")


def get_key(request):
    def gen_response(code, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'GET':
        try:
            key = Key.objects.values_list('key_name', flat=True)
            ret_list = []
            for k in key:
                ret_list.append(k)
            return gen_response(200, ret_list)
        except Exception as e:
            return gen_response(400, "Error when getting key from database: {}".format(e))

    else:
        return gen_response(400, "Bad Request")


def test_key(request):
    def gen_response(code, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'GET':
        try:
            global current_valid_key
            openai_toolkit_instance = openai_toolkit(api_key = current_valid_key, engine = 'ada')
            try:
                completion = openai_toolkit_instance.get_completion("This is a test")
            except Exception as error_invalid_key:
                # delete the invalid key
                key = Key.objects.filter(key_name=current_valid_key)
                if key:
                    key.delete()
                # get a new key
                key = Key.objects.values_list('key_name', flat=True)
                if key:
                    current_valid_key = key[0]
                else:
                    return gen_response(400, "No valid key!")
                return gen_response(400, "Key is invalid! Changed to a new key {}".format(current_valid_key))
            return gen_response(200, "Key is valid! Current key is {}".format(current_valid_key))
                    
        except Exception as e:
            return gen_response(400, "Error when testing key: {}".format(e))

    else:
        return gen_response(400, "Bad Request")


def clean_key(request):
    def gen_response(code, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'GET':
        try:
            key = Key.objects.all()
            key.delete()
            return gen_response(200, "Cleaned all keys successfully!")
        except Exception as e:
            return gen_response(400, "Error when cleaning key from database: {}".format(e))

    else:
        return gen_response(400, "Bad Request")


def query_feature(request):
    def gen_response(code, data):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'POST':
        try:
            task = request.POST['task_name']
            username = request.POST['user']
        except Exception as e:
            return gen_response(400, "Unable to digest post information: {}".format(e))
        try:
            previous_folder_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            feature_list = []
            with open(previous_folder_path+'/Boruta_AllInOne/data/{}/feature.json'.format(username), 'r') as f:
                feature_dict = json.load(f)
                feature_list = feature_dict.get(task)
            if feature_list:
                return gen_response(200, feature_list)
            else:
                return gen_response(200, [])
        except Exception as e:
            return gen_response(400, "Error when querying feature from database: {}".format(e))

    else:
        return gen_response(400, "Bad Request")