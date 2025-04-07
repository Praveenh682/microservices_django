from django.shortcuts import render
import jwt
from rest_framework.response import Response
from rest_framework.views import APIView,status

from .consumer import start_consumer
from .models import *
from .producer import *
from django.conf import settings

RABBITMQ_HOST = 'localhost'
class ProductMasterAPI(APIView):
    def get(self,request):
        try:
            product_id=request.query_params.get('product_id')

            try:
                product_obj = ProductMaster.objects.get(id=product_id)
                print(product_obj.created_by)
            except ProductMaster.DoesNotExist:
                return Response({'status':'error','message':'details not found'},status=status.HTTP_404_NOT_FOUND)
            
            publish_message(product_obj.created_by)
            user_data = start_consumer()

            return Response({"status":"success","user_details":user_data,"product_details":{'id':product_obj.id}},status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'status':'error','message':str(e)},status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        try:
            name = request.data.get('name')
            description = request.data.get('description')

            auth_header = request.headers.get('Authorization')
            secret_key = 'django-insecure-rf!)lupbt186*y-ypnlcboc%=$k)^exc2y8#o&!oz)!@#j=ud8'
            token = auth_header.split(" ")[1]
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")

            
            product_obj = ProductMaster(
                name = name,
                description = description,
                created_by = user_id
            )
            product_obj.save()
            return Response({'status':'success','message':'details created successfully'},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status':'error','message':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
