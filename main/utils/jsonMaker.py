from flask import jsonify


def generate_json_for_400_status_code(message):
    # generate json object for validation error responses
    response = {"status": "nok", "statusCode": "400", "message": message}
    return response


def generate_json_for_200_status_code(result, message, model):
    # generate json object for successful responses
    response = {"status": "ok", "statusCode": "200", "result": result, "message": message, "model": model}
    return response


def generate_json_for_500_status_code(message):
    # generate json object for unexpected internal errors
    response = {"status": "nok", "statusCode": "500", "message": message}
    return response


def generate_json_list_with_dict_list(dict_list: dict):
    json_list = []
    for key, value in dict_list.items():
        json_object = {str(key): str(value)}
        json_list.append(json_object)
        return json_list
