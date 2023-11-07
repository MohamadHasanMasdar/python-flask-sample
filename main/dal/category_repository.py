from main.utils import database
import bundles.table_names as tableNames


def find_category_id_by_title(category_title):
    '''
    This method get category title as parameter and return its id inside database
    :param category_title: category title. title is a unique value in category table
    :return: category id
    '''
    with database.connect_to_database() as connection:
        with connection.cursor() as cursor:
            sql = 'SELECT id FROM ' + tableNames.category_table + ' WHERE title = %s'
            category_id = cursor.execute(sql, category_title)
            return category_id.get('id')


def find_category_id_by_title_and_category_type_id(category_title, category_type_id, cursor):
    '''
    This method get category title and category_type_id as parameters and return its id inside database.
    in category table rules, for one category type, category titles should be unique
    :param category_title:
    :param category_type_id:
    :return: category id
    '''
    try:
        # with database.connect_to_database() as connection:
        #     with connection.cursor() as cursor:
        sql = 'SELECT id FROM ' + tableNames.category_table + ' WHERE f_category_type_id = %s and title = %s'
        cursor.execute(sql, (category_type_id, category_title))
        category_id = cursor.fetchone()
        return category_id.get('id')
    except Exception:
        response = jsonMaker.generate_json_for_500_status_code(
            messages.some_thing_went_wrong_please_call_support
        )
        raise Exception(response)
