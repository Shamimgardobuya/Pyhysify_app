from app import db
class Pagination:
    page = 1
    perPage = 1
    
    @classmethod
    def paginate(cls, query, page_from_request = None):
        if page_from_request:
            return db.paginate(query, page= page_from_request, per_page= cls.perPage, error_out= False)
        return db.paginate(query, page= cls.page, per_page= cls.perPage, error_out= False)
