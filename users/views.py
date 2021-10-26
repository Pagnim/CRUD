import json
import jwt
import bcrypt

from django.http  import JsonResponse
from django.views import View

from users.models import User
from my_settings import SECRET_KEY, ALGORITHM

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body) 
            if not User.objects.filter(name = data['name']).exists():

                encode_password = bcrypt.hashpw(data['password'].encode("utf-8"), bcrypt.gensalt())
                decode_password = encode_password.decode('utf-8')

                User.objects.create(
                    name     = data['name'],
                    password = decode_password
                )
                
                return JsonResponse({"message": "CREATED!"}, status=201)
            return JsonResponse({'message' : 'DUPLICATED_NAME'}, status=400)
            
        except KeyError:
            return JsonResponse({"message": "KEYERROR"}, status=401)

class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if not User.objects.filter(name = data['name']).exists():
                return JsonResponse({"message" : "DO NOT EXIST!"}, status=401)
                
            users = User.objects.get(name = data['name'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), users.password.encode('utf-8')):

                access_token = jwt.encode({'id' : users.id}, SECRET_KEY, algorithm=ALGORITHM)

                return JsonResponse({"access_token" : access_token}, status=201)
            
            return JsonResponse({"message": "DO NOT EXIST!"}, status=401)
        
        except KeyError:
            return JsonResponse({"message":"KEYERROR"}, status=401)