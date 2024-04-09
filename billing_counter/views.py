from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.


@api_view(['GET'])
def index(request):
    data = {'Name': 'Json', 'Age': '21'}
    return Response(data)


# add_product
# update_product
# delete_product
# add_customer
# update_customer
# delete_customer