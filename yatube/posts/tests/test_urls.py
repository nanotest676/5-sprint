from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Group, User

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username="NoName")
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            text='Тестовый текст',
            slug='test-slug'
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(PostURLTests.user)

    def test_urls_uses_correct_template(cls):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        cls.templates_url_names = {
            "": "posts/index.html",
            f"/group/{cls.group.slug}/": "posts/group_progect.html",
            f"/profile/{cls.user.username}/": "posts/profile.html",
            f"/posts/{cls.post.id}/": "posts/post_detail.html",
            f"/posts/{cls.post.id}/edit/": "posts/create_post.html",
            "/create/": "posts/post_create.html",
        }

        cls.post_create = Post.objects.create(
            author=cls.user,
            text="Тестовая пост",
        )

        cls.templates = [
            "/",
            f"/group/{cls.group.slug}/",
            f"/profile/{cls.user}/",
            f"/posts/{cls.post.id}/",
        ]

    def test_urls_exists_at_desired_location(self):
        for adress in self.templates:
            with self.subTest(adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, 200)

    def test_posts_post_id_edit_url_exists_at_author(self):
        """Страница /posts/post_id/edit/ доступна только автору."""
        self.user = User.objects.get(username=self.user)
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)
        response = self.authorized_client.get(f"/posts/{self.post.id}/edit/")
        self.assertEqual(response.status_code, 200)

    def test_create_url_redirect_anonymous_on_auth_login(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.guest_client.get("/create/", follow=True)
        self.assertRedirects(response, "/auth/login/?next=/create/")
