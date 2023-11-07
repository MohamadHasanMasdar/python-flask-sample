from flask import Blueprint, jsonify, request
from main.service.dto.user_dto import UserDto
from main.service.validator import fileValidator
from main.utils import jsonMaker
from werkzeug.exceptions import RequestEntityTooLarge
import bundles.messages as messages
import main.utils.fileUploader as fileUploader
import main.utils.enums.userStatus as userStatus
from ..service import user_service

user = Blueprint("user", __name__)


@user.route('/phoneNumberRegisterCheck/<phone_number>')
def phone_number_register_check(phone_number):
    """
    file: ymlfiles/phoneNumber.yml
    """

    try:
        return user_service.phone_number_register_check(phone_number)

    except Exception as e:
        response = eval(str(e))
        return jsonify(response)


@user.route("/nationalCodeRegisterCheck/<national_code>")
def national_code_register_check(national_code):
    """
    file: ymlfiles/nationalCode.yml
    """

    try:
        return user_service.national_code_register_check(phone_number)

    except Exception as e:
        response = eval(str(e))
        return jsonify(response)


@user.route("/registerUser", methods=['POST'])
def register_user():
    try:
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        national_code = request.form.get('national code')
        phone_number = request.form.get('phone number')
        birth_date = request.form.get('birth date')
        email_address = request.form.get('email')
        user_dto = UserDto(fname, lname, national_code, phone_number, birth_date, email_address)

        return user_service.register_user(user_dto, request)
    except RequestEntityTooLarge:
        response = jsonMaker.generate_json_for_400_status_code(
            messages.user_register_validate_national_card_image_file_size_is_larger_than_standard_size
        )
        return jsonify(response)
    except Exception as e:
        response = eval(str(e))
        return jsonify(response)
