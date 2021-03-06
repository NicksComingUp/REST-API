from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# most effective way to authenticate with the api
from rest_framework.authentication import  TokenAuthentication
# adding search profile features
from rest_framework import filters
#login api view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions

# Create your views here.
# . import from the root directory
class HelloApiView(APIView):
    """Test API VIEW."""
    serializer_class = serializers.HelloSerializer
    def get(self,request, format=None):
        """Returns a list of APIView features."""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]
        return Response({'message': 'Hello', 'an_apiview': an_apiview})
    def post(self, request):
        """Create a hello message with our name."""
        serializer = serializers.HelloSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
            serializer.errors,
             status= status.HTTP_400_BAD_REQUEST
             )
    #pk - primary key
    def put(self, request, pk=None):
        """Handles updating an object."""
        return Response({'method':'put'})
    def patch(self,request, pk=None):
        """Patch requet, only updates fields provided in the request."""
        return Response({'method': 'patch'})
    def delete(self,request,pk=None):
        "Deletes an object."
        return Response({'method':'delete'})

class HelloViewSet(viewsets.ViewSet):
    """Test API VewSet."""
    serializer_class = serializers.HelloSerializer

    def list(self,request):
        """Return a hello message."""
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code.'
        ]
        return Response({'message':'Hello', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message."""
        serializer = serializers.HelloSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hi {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
            serializer.errors,
             status=status.HTTP_400_BAD_REQUEST
             )
    # def retrieve(self, request, pk=None):
        """Handles getting an object by its ID."""
        return Response({'http_method':'GET'})
    def update(self, request, pk=None):
        """Handles updating an object"""
        return Response({'http_method':'PUT'})
    def partial_update(self, request, pk=None):
        """Handles updating part of an object."""
        return Response({'http_method':'PATCH'})
    def destroy(self, request, pk=None):
        """Handles removing an object"""
        return Response({'http_method':'DELETE'})



class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profiles."""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    #Adding authenticate and permission to the view set
    authentication_classes = (TokenAuthentication,) # toople
    permission_classes = (permissions.UpdateOwnProfile,)
    # adding search profile features
    filter_backends = (filters.SearchFilter,)
    #which fill we want the user to filter by
    search_fields = ('name', 'email',)
class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token."""
    serializer_class = AuthTokenSerializer
    def create(self, request):
        """Use the ObtainAuthToken ApiView to validate and create a token."""
        return ObtainAuthToken().post(request)
class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items."""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    # permissions for feed
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""
        serializer.save(user_profile=self.request.user)
