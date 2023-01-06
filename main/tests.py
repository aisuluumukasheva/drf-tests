from collections import OrderedDict
from django.test import TestCase

from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict


from .views import PostViewSet
from .models import Post
from account.models import User



class PostTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(
            email='test@gmail.com',
            password='12345678'
        )
        posts = [
            Post(author=user, title='1 post', description='...'),
            Post(author=user, title='2 post'),
            Post(author=user, title='3 post', description='some desc'),
        ]
        Post.objects.bulk_create(posts)  # создает в одно время посты не по одному, а bulk

    def test_listing(self):
        request = self.factory.get('/posts/')
        view = PostViewSet.as_view({'get':'list'})  #get method -> list request
        # print(view)
        response = view(request)
        # print(response)
        # print(response.data)

        assert response.status_code == 200
        assert len(response.data) == 3
        assert type(response.data) == ReturnList
        assert type(response.data[0]) == OrderedDict
        assert response.data[0]['title'] == '1 post'

    def test_details(self):
        post = Post.objects.first()  # достает первый пост
        request = self.factory.get(f'/posts/{post.id}/')
        view = PostViewSet.as_view({'get':'retrieve'})
        response = view(request, pk=post.id)
        # print(response)
        # print(response.data)

        assert response.status_code == 200
        assert type(response.data) == ReturnDict
        assert response.data['title'] == '1 post'

    def test_permissions(self):
        data = {
            'title': '4 post'
        }
        request = self.factory.post('/posts/', data, format='json')
        view = PostViewSet.as_view({'post':'create'})
        response = view(request)
        # print(response)

        assert response.status_code == 401

    def test_create(self):
        user = User.objects.first()
        data = {
            'title': '4 post'
        }
        request = self.factory.post('/posts/', data, format='json')
        force_authenticate(request, user)  # добавляет юзера в запрос
        view = PostViewSet.as_view({'post':'create'})
        response = view(request)
        # print(response)

        assert response.status_code == 201
        assert Post.objects.filter(author=user, title='4 post', description='').exists()