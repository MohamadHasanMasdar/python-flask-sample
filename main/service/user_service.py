from ..service.validator import userValidator, fileValidator
from main.utils import jsonMaker, fileUploader
from ..dal import user_repository
from werkzeug.exceptions import RequestEntityTooLarge
from main.service.dto.user_dto import UserDto
from main.service.dto.user_document_dto import UserDocumentDto
from main.service import user_document_service
from main.utils import database


def phone_number_register_check(phone_number):
    try:
        userValidator.validate_mobile_number(phone_number)
    except Exception as e:
        raise Exception(str(e))

    user = user_repository.find_user_by_phone_number(phone_number)
    if user is None:  # This phone number does not register before
        return jsonMaker.generate_json_for_200_status_code(False, None, None)
    else:  # This phone number registered before
        return jsonMaker.generate_json_for_200_status_code(True, None, None)


def national_code_register_check(national_code):
    try:
        userValidator.NationalCodeValidate().validate_user_national_code(str(national_code))
    except Exception as e:
        raise Exception(str(e))

    user = user_repository.find_user_by_national_code(national_code)
    if user is None:  # This national code does not register before
        return jsonMaker.generate_json_for_200_status_code(False, None, None)
    else:  # This national code registered before
        return jsonMaker.generate_json_for_200_status_code(True, None, None)


def register_user(user: UserDto, request):

    with database.connect_to_database() as connection:
        with connection.cursor() as cursor:
            try:
                userValidator.RegisterUserValidator().validate_register_user(user)
                fileValidator.validate_files(request, 'national card image')
                user_id = user_repository.register_user(user, cursor)
                file_name = fileUploader.upload_national_card_image_file(request)
                user_doc_dto = UserDocumentDto(user_id, file_name, None)
                user_document_service.register_user_document(user_doc_dto)
                user_info = {"user_id": user_id}
                user_model = jsonMaker.generate_json_list_with_dict_list(user_info)
                return jsonMaker.generate_json_for_200_status_code('', '', user_model)

            except Exception as e:
                raise Exception(str(e))
