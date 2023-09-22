from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class DefaultPagination(PageNumberPagination):
  # template = 

  def get_paginated_response(self, data):
    return Response(OrderedDict([
      ('count', self.page.paginator.count),
      ('html_page', self.get_html_context()),
      ('next', self.get_next_link()),
      ('previous', self.get_previous_link()),
      ('results', data)
    ]))


  page_size = 50

  