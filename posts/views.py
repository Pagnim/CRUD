import json

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Count

from posts.models          import Post
from users.models          import User

from utils                 import login_decorator

class tests(View):
    def get(self,request):
        test1 = User.objects.all()
        test2 = test1.filter(id=1)
        print(test2)
        
        
        return JsonResponse({"message":"CREATED!"}, status=201)
class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = request.user

            Post.objects.create(
                title     = data['title'],
                content   = data['content'],
                post_user = user.name,
                user_id   = user.id
            )

            return JsonResponse({"message":"CREATED!"}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEYERROR"}, status=401)
    
class ReadView(View):
    def get(self, request, posts_id):
        count     = Post.objects.all().annotate(post_count = Count('title'))
        user      = User.objects.prefetch_related('post_set')
        page      = int(request.GET.get("page", 1))
        page_size = 5
        limit     = int(page_size * page)
        offset    = int(limit - page_size)

        if posts_id == 0 :
            result = {"count":count.count(),
            "posts": [
                {   "user"    : user.filter(id = posts.user_id).first().name,
                    "title"   : posts.title,
                    "user_id" : user.filter(id = posts.user_id).first().id
                    }
            for posts in Post.objects.all()][offset:limit]}
            
            return JsonResponse({"data":result}, status=201)
        
        posts = Post.objects.get(id = posts_id)

        result = {
            "post_id": posts.id,
            "user"   : posts.post_user,
            "title  ": posts.title,
            "content": posts.content
        }

        return JsonResponse({"data":result}, status=201)

    @login_decorator
    def put(self, request, posts_id):
        data = json.loads(request.body)
        user = request.user
        post = Post.objects.get(id = posts_id)

        if post.user_id == user.id:
            post.title   = data['title']
            post.content = data['content']
            post.save()

            return JsonResponse({"message":"UPDATED!"}, status=201)
        return JsonResponse({"message":"Unauthorized"})
    
    @login_decorator
    def delete(self, request, posts_id):
        user = request.user
        post = Post.objects.get(id = posts_id)
        
        if post.user_id == user.id:
            post.delete()
    
            return JsonResponse({"message":"DELETED!"}, status=201)
        return JsonResponse({"message":"Unauthorized"})
