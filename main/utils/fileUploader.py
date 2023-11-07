from werkzeug.utils import secure_filename
import os
from main.utils import jsonMaker
from bundles import messages


def upload_national_card_image_file(request):
    '''
    This method get a request object that include image file of user national card.
    Then check file name by one of werkzeug utils named secure_filename. this function check file name and modify that
    if necessary. in this case, file name will be user national code
    :param request: it's an object of flask request class. it contains user national code and file of the user national
    card image
    :return: file name
    '''
    try:
        national_card_image = request.files['national card image']
        user_national_code = request.form.get('national code')

        home_dir = os.path.expanduser("~")
        upload_folder = os.path.join(home_dir, "upload")
        file_name = secure_filename(user_national_code)
        national_card_image.save(os.path.join(upload_folder, file_name))
        return file_name
    except Exception:
        response = jsonMaker.generate_json_for_500_status_code(
            messages.some_thing_went_wrong_please_call_support
        )
    raise Exception(response)
