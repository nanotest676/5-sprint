from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from http import HTTPStatus

from ..models import Post, Group, User

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="NoName")
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug",
            description="Описание",
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовая пост",
            group=cls.group,
        )

        cls.templates_url_names = [
            ("/", "posts/index.html"),
            (f"/group/{cls.group.slug}/", "posts/group_progect.html"),
            (f"/profile/{cls.user.username}/", "posts/profile.html"),
            (f"/posts/{cls.post.id}/", "posts/post_detail.html"),
            (f"/posts/{cls.post.id}/edit/", "posts/create_post.html"),
            ("/create/", "posts/post_create.html"),
        ]

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)

    def test_urls(self):
        """URL-адрес использует соответствующий шаблон."""
        for url, template in PostURLTests.templates_url_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                )

    def test_uknown_page(self):
        """Тест на несуществующую страницу"""
        response = self.authorized_client.get("/unknown/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
