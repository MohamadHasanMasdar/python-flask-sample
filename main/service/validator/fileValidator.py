from main.utils import jsonMaker
import bundles.messages as messages

def validate_files(request, file_tag):
    # check if the post request has the file part
    if file_tag not in request.files:
        response = jsonMaker.generate_json_for_400_status_code(
            messages.user_register_validate_national_card_image_file_not_found
        )
        raise Exception(response)

    file_name = request.files[file_tag].filename
    # if user does not select file, browser also
    # submit an empty part without filename
    if file_name and file_name == '':
        response = jsonMaker.generate_json_for_400_status_code(
            messages.user_register_validate_national_card_image_file_not_found
        )
        raise Exception(response)

    if not __file_with_allowed_format(file_name, {'bmp', 'png', 'jpg', 'jpeg'}):
        response = jsonMaker.generate_json_for_400_status_code(
            messages.user_register_validate_national_card_image_file_format_is_not_supported
        )
        raise Exception(response)


def __file_with_allowed_format(file_name, allowed_formats):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in allowed_formats
