from main.service.dto.user_document_dto import UserDocumentDto
from main.utils.database import connect_to_database
from bundles import table_names


def insert_user_document(user_document_dto: UserDocumentDto):
    try:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                sql = 'INSERT INTO ' + table_names.user_document_table + '  (`f_user_id`, `f_document_type_id`, `file_name`)' \
                                                                         ' VALUES (%s, %s, %s)'
                cursor.execute(sql,
                               (user_document_dto.user_id, user_document_dto.doc_type_id, user_document_dto.file_name))
                connection.commit()
                user_doc_id = cursor.lastrowid
                return user_doc_id
    except Exception:
        response = jsonMaker.generate_json_for_500_status_code(
            messages.some_thing_went_wrong_please_call_support
        )
        raise Exception(response)
