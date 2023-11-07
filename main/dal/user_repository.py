from main.utils import database
from bundles import table_names
import main.dal.categoryType_repository as categoryType_repository
import main.dal.category_repository as categories_repository
from main.service.dto.user_dto import UserDto
from main.utils import jsonMaker
from main.utils.enums.userStatus import UserStatus
from bundles import messages


def find_user_by_phone_number(phone_number):
    with database.connect_to_database() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM" + table_names.user_table + "where `phone_number` =" + phone_number
            cursor.execute(sql)
            user = cursor.fetchone()
            return user


def find_user_by_national_code(national_code):
    with database.connect_to_database() as connection:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM' + table_names.user_table + 'where `national_code` =' + str(national_code)
            cursor.execute(sql)
            user = cursor.fetchone()
            return user


def register_user(user: UserDto, cursor):
    try:
        user_status_category_type_id = categoryType_repository.find_category_type_id_by_cat_title(
            UserStatus.__name__, cursor)
        user_status_category_id = categories_repository.find_category_id_by_title_and_category_type_id(
            UserStatus.NOT_APPROVED.name, user_status_category_type_id, cursor)
        sql = 'INSERT INTO ' + table_names.user_table + '(`fname`, `lname`, `national_code`, `phone_number`, ' \
                                                        '`birth_date`, `email_address`, `f_status_id`) ' \
                                                        'VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql,
                       (user.fname, user.lname, user.national_code, user.phone_number, user.birth_date,
                        user.email_address, user_status_category_id))
        # connection.commit()
        user_id = cursor.lastrowid

        return user_id
    except Exception:
        response = jsonMaker.generate_json_for_500_status_code(
            messages.some_thing_went_wrong_please_call_support
        )
        raise Exception(response)
