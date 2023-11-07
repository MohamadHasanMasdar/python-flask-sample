from email_validator import validate_email, EmailNotValidError
from main.utils import jsonMaker, database
from bundles import messages, table_names


class EmailValidate:
    def validate_email(self, email_address):
        try:
            self.validate_email_address_not_empty(email_address)
            self.validate_email_address_length_is_less_than_database_column_max_length(email_address)
            self.validate_email_address_format_is_correct(email_address)
        except Exception as e:
            raise Exception(str(e))

    def validate_email_address_not_empty(self, email_address):
        if email_address is None or not email_address:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.user_register_validate_user_email_address_is_empty)
            raise Exception(response)

    def validate_email_address_format_is_correct(self, email_address):
        '''
               This function validate email address is in correct format. it uses email_validator library to do that.
               for more information visit: https://pypi.org/project/email-validator/
               :param email_address:
               :return:does not return anything. if email address is not correct, an EmailNotValidError will be raise.
               '''

        try:
            # Check that the email address is valid.
            validation = validate_email(email_address)

            # Take the normalized form of the email address
            # for all logic beyond this point (especially
            # before going to a database query where equality
            # may not take into account Unicode normalization).
            email = validation.email
        except EmailNotValidError:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.user_register_validate_user_email_address_is_not_in_correct_format)
            raise Exception(response)

    def validate_email_address_length_is_less_than_database_column_max_length(self, email_address):
        email_database_column_length = database.get_column_length_of_table("'email_address'", table_names.user_table_string)
        if len(email_address) > email_database_column_length:
            response = jsonMaker.generate_json_for_400_status_code(
                messages.user_register_validate_user_email_address_length_is_too_long)
            raise Exception(response)
