import bundles.messages as messages
from main.utils import jsonMaker, database
import phonenumbers
from main.service.dto.user_dto import UserDto
from .dateValidator import DateValidate
from bundles import table_names
from main.dal import user_repository
from .emailValidator import EmailValidate


class MobileNumberValidate:
    def validate_mobile_number(self, phone_number):
        try:
            self.validate_mobile_number_is_none_or_empty(phone_number)
            self.validate_mobile_number_in_correct_format(phone_number)
        except Exception as e:
            raise Exception(str(e))

    def validate_mobile_number_is_none_or_empty(self, phone_number):
        if phone_number is None or not phone_number:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.check_phone_number_user_validate_phone_number_is_none_or_empty)
            raise Exception(response)

    def validate_mobile_number_in_correct_format(self, phone_number):
        """
        This method validate if phone number is in correct format.
        We use phonenumbers library to verify phone numbers. it hosted in the following url:
        https://pypi.org/project/phonenumbers
        :param phone_number:
        :return: the method does not return anything. if phone number is not validate, an Exception will be raised
        """

        if len(phone_number) != 11:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.check_phone_number_user_validate_phone_number_format_is_not_true)
            raise Exception(response)
        try:
            parsed_number = phonenumbers.parse(phone_number, "IR")
        except phonenumbers.NumberParseException:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.check_phone_number_user_validate_phone_number_format_is_not_true)
            raise Exception(response)

        is_valid_number = phonenumbers.is_valid_number(parsed_number)
        if not is_valid_number:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.check_phone_number_user_validate_phone_number_format_is_not_true)
            raise Exception(response)


class NationalCodeValidate:
    def validate_user_national_code(self, national_code):
        try:
            self.validate_national_code_is_none_or_empty(national_code)
            self.validate_national_code_is_in_correct_format(national_code)
        except Exception as e:
            raise Exception(str(e))

    def validate_national_code_is_none_or_empty(self, national_code):
        if national_code is None or not national_code:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.check_nat_code_national_code_validate_is_none_or_empty)
            raise Exception(response)

    def validate_national_code_is_in_correct_format(self, national_code):
        if len(national_code) != 10:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.check_nat_code_national_code_validate_format_is_not_correct)
            raise Exception(response)
        if not str(national_code).isnumeric():
            response = jsonMaker.generate_json_for_400_status_code(
                messages.check_nat_code_national_code_validate_format_is_not_correct)
            raise Exception(response)


class RegisterUserValidator:

    def validate_register_user(self, user: UserDto):
        if user is None:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.object_is_none)
            raise Exception(response)

        NationalCodeValidate().validate_user_national_code(user.national_code)
        MobileNumberValidate().validate_mobile_number(user.phone_number)
        if self.validate_user_register_before(user):
            response = jsonMaker.generate_json_for_400_status_code(
                messages.user_register_validate_user_register_before)
            raise Exception(response)

        self.validate_user_first_name(user.fname)
        self.validate_user_last_name(user.lname)

        try:
            DateValidate().validate_date_format_is_correct(user.birth_date)
        except ValueError:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.user_register_validate_user_birth_date_is_not_in_correct_format)
            raise Exception(response)

        try:
            EmailValidate().validate_email(user.email_address)
        except Exception as e:
            raise Exception(str(e))

    def validate_user_register_before(self, user: UserDto):
        '''
        This function check if user national code or phone number registered before
        :param user: userDto include user national code and phone number
        :return: True if user register before. else return False
        '''
        founded_user = user_repository.find_user_by_national_code(user.national_code)
        if founded_user is not None:
            return True
        else:
            founded_user = user_repository.find_user_by_phone_number(user.phone_number)
            if founded_user is not None:
                return True

        return False

    def validate_user_first_name(self, fname):

        # check for name is not none or empty
        if fname is None or not fname:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.user_register_validate_user_fname_is_none_or_empty)
            raise Exception(response)

        # check maximum length of fname column in database and compare to input name
        fname_max_length = database.get_column_length_of_table("'fname'", table_names.user_table_string)
        if len(fname) > fname_max_length:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.user_register_validate_user_fname_length_is_too_long)
            raise Exception(response)

        # check for first name is in correct format
        # name characters should be alphabet or space
        if not all(x.isalpha() or x.isspace() for x in fname):
            response = jsonMaker.generate_json_for_400_status_code(
                messages.user_register_validate_user_fname_is_not_in_correct_format)
            raise Exception(response)

    def validate_user_last_name(self, lname):

        # check for name is not none or empty
        if lname is None or not lname:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.user_register_validate_user_lname_is_none_or_empty)
            raise Exception(response)

        # check maximum length of lname column in database and compare to input name
        lname_max_length = database.get_column_length_of_table("'lname'", table_names.user_table_string)
        if len(lname) > lname_max_length:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.user_register_validate_user_lname_length_is_too_long)
            raise Exception(response)

        # check for last name is in correct format
        # name characters should be alphabet or space
        if not all(x.isalpha() or x.isspace() for x in lname):
            response = jsonMaker.generate_json_for_400_status_code(
                messages.user_register_validate_user_lname_is_not_in_correct_format)
            raise Exception(response)
