from rest_framework.views import APIView
from django.db.utils import IntegrityError
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Organization, User
from .serializers import UserCreateSerializer, LoginSerializer, UserSerializer, OrganizationSerializer, AddUserToOrganizationSerializer

def home(request):
       return render(request, 'home.html')


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        empty_fields = [field for field, value in request.data.items() if value in [None, '', []]]
        if empty_fields:
                        error_message = f"Empty fields found: {', '.join(empty_fields)}"
                        return Response({"error": error_message, }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


        if serializer.is_valid():
            try:
                user = serializer.save()
                organization = Organization.objects.create(
                        name=f"{user.firstName}'s Organization",
                        description = f"This organization was created by {user.get_full_name()}"
                )
                organization.users.add(user)
                refresh = RefreshToken.for_user(user)
                return Response({
                        'status': 'success',
                        'message': 'Registration successful',
                        'data': {
                        'accessToken': str(refresh.access_token),
                        'user': UserSerializer(user).data
                        }
                }, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({
                    'status': 'Bad request',
                    'message': 'Registration unsuccessful',
                    'errors': str(e)
                }, status=status.HTTP_400_BAD_REQUEST) 
        
               
        return Response({
            'status': 'Bad request',
            'message': 'Registration unsuccessful',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        empty_fields = [field for field, value in request.data.items() if value in [None, '', []] and field != 'phone']
        if empty_fields:
                        error_message = f"Empty fields found: {', '.join(empty_fields)}"
                        return Response({"error": error_message, }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                        'status': 'success',
                        'message': 'Login successful',
                        'data': {
                        'accessToken': str(refresh.access_token),
                        'user': UserSerializer(user).data
                        }
                }, status=status.HTTP_200_OK)
            
        return Response({
            'status': 'Bad request',
            'message': 'Authentication failed',
        }, status=status.HTTP_401_UNAUTHORIZED)


class UserListAndDetailView(viewsets.ModelViewSet):
       queryset = User.objects.all()
       serializer_class = UserSerializer

       def list(self, request, *args, **kwargs):
                user_list = self.get_queryset()

                # Serialize the queryset
                serializer = self.serializer_class(user_list, many=True)

                user_data = {
                'status': 'success',
                'message': 'Users fetched successfully',
                'data': {
                        'users': serializer.data
                }
                }

                return Response(user_data, status=status.HTTP_200_OK)

       def retrieve(self, request, *args, **kwargs):
                instance = self.get_object()
                serializer = self.get_serializer(instance)

                response_data = {
                'status': 'success',
                'message': 'User retrieved successfully',
                'data': {
                        'userId': serializer.data['user_id'],
                        'firtName': serializer.data['firstName'],
                        'lastName': serializer.data['lastName'],
                        'email': serializer.data['email'],
                        'phone': serializer.data['phone']
                }
                }

                return Response(response_data, status=status.HTTP_200_OK)


class UserOrganizationView(viewsets.ModelViewSet):
       queryset = Organization.objects.all()
       serializer_class = OrganizationSerializer

       def get_queryset(self):
                # Filter organizations based on the current user
                return self.request.user.organizations.all()

       def list(self, request, *args, **kwargs):
                user_organisations = self.get_queryset()

               
                serializer = self.serializer_class(user_organisations, many=True)

                user_organisation_data = {
                'status': 'success',
                'message': 'Organizations fetched successfully',
                'data': {
                        'organisations': serializer.data
                }
                }

                return Response(user_organisation_data, status=status.HTTP_200_OK) 


       def retrieve(self, request, *args, **kwargs):
                instance = self.get_object()
                serializer = self.get_serializer(instance)

                response_data = {
                'status': 'success',
                'message': 'Organization retrieved successfully',
                'data': {
                        'orgId': serializer.data['org_id'],
                        'name': serializer.data['name'],
                        'description': serializer.data['description']
                }
                }

                return Response(response_data, status=status.HTTP_200_OK)

       
       def create(self, request, *args, **kwargs):
              serializer = self.get_serializer(data=request.data)
              serializer.is_valid(raise_exception=True)

              # Perform name validation
              if not self.request.data.get('name'):
                return Response({
                        'error': 'Name field is required.'
                        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

              # Create the organization
              self.perform_create(serializer)

              response_data = {
                        'status': 'success',
                        'message': 'Organisation created successfully',
                        'data': {
                                'orgId': serializer.data['org_id'],
                                'name': serializer.data['name'],
                                'description': serializer.data.get('description', '')
                        }
                }

              return Response(response_data, status=status.HTTP_201_CREATED)
       

       def perform_create(self, serializer):
                # Save the organization without users first
                organization = serializer.save()

                # Associate the current user with the organization
                organization.users.add(self.request.user)

       
       @action(detail=True, methods=['post'], url_path='users')
       def add_user(self, request, pk=None):
                organization = self.get_object()
                serializer = AddUserToOrganizationSerializer(data=request.data)
                if serializer.is_valid():
                        user = serializer.validated_data['user']
                        organization.users.add(user)
                        return Response({
                                'status': 'success',
                                'message': 'User added to organization successfully',
                        }, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






                
        



        
        
