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
from ...bgtasks import mail_sending

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
                    return Response(data, status=status.HTTP_201_CREATED)
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

class ForgotPasswordView(APIView):
    def post(self, request):
        
        email = request.data.get("email", None)
        if email != None:
            try: 
                user = User.objects.get(email=email)
            
                token = uuid.uuid4()
                user.token = token
                user.token_status = True
                user.save()

                subject = "Reset Your Password"
                body = """
                <div style="height:100%;margin:0;padding:0;width:100%;background-color:#fafafa">
                <center>
                <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" style="border-collapse:collapse;height:100%;margin:0;padding:0;width:100%;background-color:#fafafa">
                <tbody><tr>
                <td align="center" style="height:100%;margin:0;padding:10px;width:100%;border-top:0">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;border:0;max-width:600px!important">
                <tbody>
                <tr>
                <td style="background:#ffffff none no-repeat center/cover;background-color:#ffffff;background-image:none;background-repeat:no-repeat;background-position:center;background-size:cover;border-top:0;border-bottom:2px solid #eaeaea;padding:9px 18px;">
                <div style="padding:20px 18px 25px;text-align:center;width:100%">
                </div>
                <h1 style="display:block;margin:0;padding:0;color:#202020;font-family:Helvetica;font-size:26px;font-style:normal;font-weight:bold;line-height:125%;letter-spacing:normal;text-align:left">Hello {username},
                </h1><br>
                <p style="margin:10px 0;padding:0;color:#202020;font-family:Helvetica;font-size:16px;line-height:150%;text-align:left">
                Someone request to reset password!</p><br>
                <a href="https://frappy-cms.vercel.app/password_reset/token/{token}/">https://frappy-cms.vercel.app/password_reset/token/{token}/</a>
                <p>Thanks From Deeplobe Team,</p>
                </tbody>
                </table>
                </td>
                </tr>
                </tbody></table>
                </center>
                </div>""".format(
                username=user.username, token=token)

                mail_sending(email, subject, body)
                return Response({"message": "Email sent"}, status=status.HTTP_200_OK) 
            except Exception as e:
                print(e)
                return Response({"error": "Email not present in database"}, status=status.HTTP_400_BAD_REQUEST) 

        else:
            return Response({"error": "Email required"}, status=status.HTTP_400_BAD_REQUEST) 

class ForgotPasswordConfirmView(APIView):
    def post(self, request):
        
        token = request.data.get("token", None)
        password1 = request.data.get("password1", None)
        password2 = request.data.get("password2", None)
        if (token != None) and (password1 != None) and (password2 != None):
            try: 
                user = User.objects.get(token=token, token_status=True)
            
                user.set_password(password1)
                user.token_status = False
                user.save()
                return Response({"message": "New password set"}, status=status.HTTP_200_OK)  

            except Exception as e:
                print(e)
                return Response({"error": "token expired"}, status=status.HTTP_400_BAD_REQUEST)  
        else:
            return Response({"error": "Can't be null passwords and token"}, status=status.HTTP_400_BAD_REQUEST)  