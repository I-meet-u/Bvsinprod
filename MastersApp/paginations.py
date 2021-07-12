from rest_framework import pagination

class CustomPagination(pagination.LimitOffsetPagination):
    default_limit = 25
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 1000