from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # количество объектов на странице по умолчанию
    page_size_query_param = 'page_size'  # можно менять через query params
    max_page_size = 50  # максимум объектов на странице

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,      # всего объектов
            'page': self.page.number,                # текущая страница
            'page_size': self.get_page_size(self.request),  # размер страницы
            'total_pages': self.page.paginator.num_pages,   # всего страниц
            'results': data                          # объекты текущей страницы
        })
