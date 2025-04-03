from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView,status
from rest_framework.response import Response
from .models import *
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes,api_view
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
            
        
            transaction.set_autocommit(False)
            user_obj = CustomUser(
            first_name=first_name,
            last_name=last_name,
            username=first_name+" "+last_name,
            email=email,
            mobile_number=mobile,
            is_staff=is_staff,
            is_superuser=is_superuser
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


