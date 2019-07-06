from __future__ import print_function

from AnalysisSite.celerys import app
from AnalysisSite.config import PROFILE
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

    json_image.close()

    if PROFILE :
        return result, result_data['model_inference_time'], result_data['result_save_time']
    else :
        return result
