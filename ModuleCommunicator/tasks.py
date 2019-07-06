from __future__ import print_function

from AnalysisSite.celerys import app
import json
import requests


@app.task
def communicator(url, image_path):
    json_data = dict()
    json_image = open(image_path, 'rb')
    json_files = {'image': json_image}

    result_response = requests.post(url=url, data=json_data, files=json_files)
    result_data = json.loads(result_response.content)
    result = result_data['result']

    model_execute_time = result_data['model_execute_time']
    db_save_time = result_data['db_save_time']
    json_image.close()

    return result, model_execute_time, db_save_time
