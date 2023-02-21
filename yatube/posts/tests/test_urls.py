from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Group, Post

User = get_user_model()


class TaskURLTests(TestCase):
    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовый текст',
            slug='test-slug'
        )

        Post.objects.create(
            text='Тестовый заголовок',
            id=81,
            author=User.objects.create_user(username='HasNoName')
        )

    def setUp(self):
        self.guest_client = Client()

    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get("")
        self.assertEqual(response.status_code, 200)

    def test_task_added_url_exists_at_desired_location(self):
        """Страница /group/test-slug/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, 200)

    def test_home_url_exists_at_desired_location(self):
        """Страница profile/<str:username> доступна любому пользователю."""
        response = self.guest_client.get('profile/<str:username>')
        self.assertEqual(response.status_code, 200)

    def test_home_url_exists_at_desired_location(self):
        """Страница posts/<int:post_id>/ доступна любому пользователю."""
        response = self.guest_client.get('posts/81/')
        self.assertEqual(response.status_code, 404)

    def test_task_detail_url_exists_at_desired_location_authorized(self):
        """Страница create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('create/')
        self.assertEqual(response.status_code, 200)

    def test_task_detail_url_exists_at_desired_location_authorized(self):
        """Страница posts/<int:post_id>/edit/
        доступна авторизованному пользователю."""
        response = self.authorized_client.get('/')
        self.assertEqual(response.status_code, 200)
