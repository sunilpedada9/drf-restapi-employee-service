from django.shortcuts import render
from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from utils.util_logging import LoggingConfig
import logging
import yaml
from django.db.models import Q
from rest_framework.response import Response
from api_service.models import CustomUser
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.
class Home(APIView):
    permission_classes = (AllowAny,)
    def get(self,request):
        return Response({"message":"Please check api doc."})

class CustomUserList(APIView):
    """ view class for customuser for GET,POST,DELETE operation"""
    permission_classes = (AllowAny,)
    def __init__(self):
        self.logging_config = LoggingConfig()
        self.logger = logging.getLogger('CustomerUserList.log')
        self.logger.info("In CustomUserList")
        with open('config/config.yaml','r') as fd:
            self.config = yaml.safe_load(fd)

    def get(self,request):
        try:
            self.logger.info('In get call')
            search = request.query_params.get("search",None)
            query = Q()
            custom_users = CustomUser.objects.all()
            if search:
                cil_list = self.config['customuser_config']['customuser_colmuns_list']
                for col in cil_list:
                    query |= Q(**{f"{col}__iexact":search})
                custom_users = CustomUser.objects.filter(query)
            serialized = CustomUserSerializer(custom_users,many=True)
            return Response(serialized.data,status=200)

        except Exception as err:
            self.logger.error(f"get call error:{str(err)}")
            return Response({"error":str(err)},status=500)
        
    def post(self,request):
        try:
            self.logger.info("In post call")
            serialized = CustomUserSerializer(data=request.data,many=True)
            if serialized.is_valid(raise_exception=True):
                serialized.save()
                return Response(serialized.data,status=201)
            return Response(serialized.errors,status=400)
        except Exception as err:
            self.logger.error(f"Post call error:{str(err)}")
            return Response({"error":str(err)},status=500)

    def delete(self,request):
        try:
            self.logger.info('In delete')
            count = CustomUser.objects.all().delete()
            return Response({"message":count[0]},status=204)
        except Exception as err:
            self.logger.error(f"Delete error:{str(err)}")
            return Response({"error":str(err)},status=500)
        
class CustomUserDetails(APIView):
    """"  GET,UPDATE,DELETE call cased on id"""

    permission_classes = (AllowAny,)
    def __init__(self):
        self.logging_config = LoggingConfig()
        self.logger = logging.getLogger('CustomUserDetails.log')
        self.logger.info("In CustomUserDetails")
        with open('config/config.yaml','r') as fd:
            self.config = yaml.safe_load(fd)

    def get(self,request,pk=''):
        try:
            self.logger.info('In get call')
            user = CustomUser.objects.get(pk=pk)
            return Response(data=CustomUserSerializer(user).data,status=200)
        except Exception as err:
            self.logger.error(f"GET error: {str(err)}")
            return Response({"error":str(err)},status=500)
        
    def patch(self,request,pk=''):
        try:
            self.logger.info("In put call")
            user = CustomUser.objects.get(pk=pk)
            if not user:
                return Response({"message":"Not Found"},status=404)
            serialized = CustomUserSerializer(instance=user,data=request.data,partial=True)
            if serialized.is_valid(raise_exception=True):
                serialized.save()
                return Response(data=serialized.data,status=200)
            return Response(data=serialized.errors,status=400)
        except Exception as err:
            self.logger.error(f"PATCH error: {str(err)}")
            return Response({"error":str(err)},status=500)
        
    def delete(self,request,pk=''):
        try:
            self.logger.info('In delete call')
            CustomUser.objects.get(pk=pk).delete()
            return Response({"messgae":"Success"},status=204)
        except Exception as err:
            self.logger.error(f"DELETE error: {str(err)}")
            return Response({"error":str(err)},status=500)   
