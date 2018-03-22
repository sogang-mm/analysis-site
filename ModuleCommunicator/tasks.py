from __future__ import print_function

from AnalysisSite.celerys import app
import json
import requests


@app.task
def post_image_and_get_result(url, image_path):
    json_data = dict()
    json_image = open(image_path, 'rb')
    json_files = {'image': json_image}

    result_response = requests.post(url=url, data=json_data, files=json_files)
    result_data = json.loads(result_response.content)
    result = result_data['result']

    json_image.close()

    return str(result)
