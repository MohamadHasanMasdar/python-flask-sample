from main.service.dto.user_document_dto import UserDocumentDto
from main.utils.enums.userDocument import UserDocument as user_doc
from main.utils.enums.userDocument import UserDocument
from main.dal import category_repository, categoryType_repository, user_repository, user_document_repository


def register_user_document(user_document_dto: UserDocumentDto):
    try:
        doc_cat_type_id = categoryType_repository.find_category_type_id_by_cat_title(UserDocument.__name__)
        document_type_cat_id = category_repository \
            .find_category_id_by_title_and_category_type_id(UserDocument.NATIONAL_CARD_IMAGE.name, doc_cat_type_id)

        user_document_dto.doc_type_id = document_type_cat_id
        user_document_repository.insert_user_document(user_document_dto)
    except Exception as e:
        raise Exception(str(e))



