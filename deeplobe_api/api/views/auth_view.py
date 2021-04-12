import uuid
import json
import requests

from django.http import HttpRequest
from django.conf import settings
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from allauth.account.views import PasswordResetView, PasswordSetView

from ...db.models import SocialProvider
from ...db.models import User
from django.views.decorators.csrf import csrf_exempt

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def payload_generate(self, user):
    
    payload = jwt_payload_handler(user)

    token = jwt_encode_handler(payload)

    # user_data being passed into Response
    data = self.user_data(user, token)

    return data

def google_verify(request):
 
    try:
        # token = "ya29.a0AfH6SMDa54m4QZ--pwi7YfTqmm6HA-WNCj08ZUQMABQHfc6TGAxVvLNQuqtVYIbrMn-6bH68MZZHH4MHBG3GclzXH3I6cbHYH4WwQGBt4ZkqOUVu1Di3N8qw6pyfJNYjQpUdWG8P2F-sV6f5dOo0Q2mq-PikFxc"
        response = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={request.data['token']}")
        data = response.json()
        return data
    
    except Exception as e:
        print(e)
        return {
        "error": "invalid_request",
        "error_description": "Invalid Credentials"
        }


class LoginDetailMixin:
    def user_data(self, user, token):
        user_data = {}
        user_data["user_id"] = user.id
        user_data["email"] = user.email
        user_data["user_first_name"] = user.first_name
        user_data["user_last_name"] = user.last_name
        user_data["username"] = user.username
        user_data["user_is_staff"] = user.is_staff
        user_data["user_is_active"] = user.is_active
        user_data["user_is_superuser"] = user.is_superuser
        user_data["token"] = token
        
        return user_data

    def social_provider_auth(self, user, provider, extra):
        provider, created = SocialProvider.objects.get_or_create(
            user=user, provider=provider
        )
        provider.extra = extra
        provider.save()
        return

class SocialAuthView(LoginDetailMixin, APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SocialAuthView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        Generate JWT Token
        """
        return_data = google_verify(request)
        if ("error" in return_data) or ("error_description" in return_data):
            return Response(return_data, status=status.HTTP_400_BAD_REQUEST)
        else:
         
            email = return_data.get("email", None)
            first_name = return_data.get("family_name", None)
            last_name = return_data.get("given_name", None)
            provider = "Google"
            extra = return_data
            if email !=None:
                try:
                    user = User.objects.get(email=email)
                    data = payload_generate(self, user)
                    # Update Social Provider Details
                    self.social_provider_auth(user, provider, extra)
                    return Response(data, status=status.HTTP_200_OK)

                except:
                    
                    pw = str(uuid.uuid4())
                    user = User.objects.create_user(email=email, password=pw, company="google sign up",
                    job_title="google sign up",
                    first_name=first_name,
                    last_name=last_name,
                    terms_conditions=True,
                    username = last_name+" "+first_name
                    )
                    data = payload_generate(self, user)

                    self.social_provider_auth(user, provider, extra)
                    return Response({}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST) 


class EmailAuthView(LoginDetailMixin, APIView):
   
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EmailAuthView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        Generate JWT Token
        """
        str_data = json.dumps(request.data)
        payload = json.loads(str_data)
        email = payload["email"]
        password = payload["password"]
        auth = payload["auth"]
        if auth == "in":
            try:
                user = User.objects.get(email=email)
            
                if user.check_password(password):
                    data = payload_generate(self, user)
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"message": "authentication failed"},
                        status=status.HTTP_200_OK,
                    )
            except User.DoesNotExist:
                return Response(
                    {"message": "account does not exist"},
                    status=status.HTTP_200_OK,
                )

        if auth == "up":
            
            first_name = payload.get("first_name", None)
            last_name = payload.get("last_name", None)
            email = payload.get("email", None)

            password = payload.get("password", None)
            company = payload.get("company", None)
            job_title = payload.get("job_title", None)
            terms = payload.get("terms", None)
            if (first_name !=None) and (last_name !=None) and (email !=None) and (password !=None) and (company !=None) and (job_title !=None) and (terms !=None):
                try:
                    user = User.objects.get(email=email)
                    return Response(
                        {"message": "account already exists"},
                        status=status.HTTP_200_OK,
                    )
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                        company= company,
                        job_title=job_title,
                        terms_conditions=terms,
                        username=last_name+" "+first_name
                    )
                    
                    data = payload_generate(self, user)
                 
                    return Response(data, status=status.HTTP_201_CREATED)
            else:
               return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST) 






# class APIPasswordResetView(PasswordResetView):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):

#         return super(APIPasswordResetView, self).dispatch(request, *args, **kwargs)


# class ForgotPassword(APIView):
#     def post(self, request):
#         str_data = json.dumps(request.data)
#         payload = json.loads(str_data)
#         email = payload.get("email", False)

#         # First create a post request to pass to the view
#         request = HttpRequest()
#         request.method = "POST"

#         # add the absolute url to be be included in email
#         if settings.DEBUG:
#             request.META["HTTP_HOST"] = "127.0.0.1:8000"
#         else:

#             request.META["HTTP_HOST"] = "fashopi-staging.herokuapp.com"
#         # pass the post form data
#         request.POST = {"email": email}

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             user = False
#         if email and user:
#             APIPasswordResetView.as_view()(request)
#             return Response({"message": "sent"}, status=201)
#         else:
#             return Response({"message": "failed"}, status=200)


# class APIPasswordsetView(PasswordSetView):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):

#         return super(APIPasswordsetView, self).dispatch(request, *args, **kwargs)


# class PasswordSet(APIView):
#         def post(self, request):
#             str_data = json.dumps(request.data)
#             payload = json.loads(str_data)
#             password1 = payload.get("password1", False)
#             password2 = payload.get("password2", False)


#             # First create a post request to pass to the view
#             request = HttpRequest()
#             request.method = "POST"
#             if settings.DEBUG:
#                 request.META["HTTP_HOST"] = "127.0.0.1:8000"
#             else:
#                 request.META["HTTP_HOST"] = "fashopi-staging.herokuapp.com"

#             request.POST = {"password1": password1, "password2": password2}

#             # request.META["user"]= old_request.user
#             if password1 == password2:
#                     APIPasswordsetView.as_view()(request)
#                     return Response({"message": "sent"}, status=201)
#             else:
#                     return Response({"message": "failed"}, status=200)