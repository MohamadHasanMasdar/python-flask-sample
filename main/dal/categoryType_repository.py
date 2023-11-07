from main.utils import database
import bundles.table_names as tableNames


def find_category_type_id_by_cat_title(category_type, cursor):
    '''
    This method get category type title as parameter and return its id inside database
    :param category_type: category type title. title is a unique value in category type table
    :return: category type id
    '''
    try:
        # with database.connect_to_database() as connection:
        #     with connection.cursor() as cursor:
        sql = 'SELECT id FROM ' + tableNames.category_type_table + ' WHERE title = %s'
        cursor.execute(sql, category_type)
        category_type_id = cursor.fetchone()
        return category_type_id.get('id')
    except Exception:
        response = jsonMaker.generate_json_for_500_status_code(
            messages.some_thing_went_wrong_please_call_support
        )
        raise Exception(response)
