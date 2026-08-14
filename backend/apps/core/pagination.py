from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    """
    Standard pagination class for all list endpoints.
    Allows clients to request a specific page size up to 100.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100