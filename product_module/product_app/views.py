from django.shortcuts import render
import jwt
from rest_framework.response import Response
from rest_framework.views import APIView,status
from .models import *
from django.conf import settings

class ProductMasterAPI(APIView):
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
        
