from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView,status
from rest_framework.response import Response
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes,api_view
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from django.db import transaction

# Create your views here.

class RoleMasterAPI(APIView):
    def post(self,request):
        try:
            data=request.data
        
            name=data.get('name')
            description=data.get('description')
            
        
            transaction.set_autocommit(False)
            roleobj = RoleMaster(
                name=name,
                description=description,
            )
            roleobj.save()
            transaction.commit()
            return Response({"status":"sucess","message":"user created successfully"})

        except Exception as e:
            transaction.rollback()
            return Response({"status":"error","message":e})

class UserCreateAPI(APIView):
    def post(self,request):
        try:
            data=request.data
        
            first_name=data.get('first_name')
            last_name=data.get('last_name')
            email=data.get('email')
            mobile=data.get('mobile')
            is_staff=data.get('is_staff',False)
            is_superuser=data.get('is_superuser',False)
            role=data.get('role','customer')
            password = data.get('password')
            
        
            transaction.set_autocommit(False)
            user_obj = CustomUser(
            first_name=first_name,
            last_name=last_name,
            username=first_name+" "+last_name,
            email=email,
            mobile_number=mobile,
            is_staff=is_staff,
            is_superuser=is_superuser,
            password=make_password(password)
            )
            user_obj.save()

            try:
                role_obj = RoleMaster.objects.get(name=role)
            except RoleMaster.DoesNotExist:
                return Response({"status":"error","message":e})

            rolemap_obj = RoleMapping(
                role=role_obj,
                user=user_obj
                
            )
            rolemap_obj.save()

            transaction.commit()
            return Response({"status":"sucess","message":"user created successfully"})

        except Exception as e:
            transaction.rollback()
            return Response({"status":"error","message":e})
        
@api_view(['POST'])
@permission_classes([AllowAny,])
def authenticate_user(request):
    try:
        mobileno = request.data.get('mobileno')
        password = request.data.get('password')

        try:
            user_obj = CustomUser.objects.get(mobilenumber=mobileno,password=check_password(password))
        except Exception as e:
            return Response({'status':'error','message':'invalid credentials'},status=status.HTTP_400_BAD_REQUEST)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)

        return Response({'status':'success','message':'login successfully','token':token},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status':'error','message':str(e)},status=status.HTTP_400_BAD_REQUEST)


