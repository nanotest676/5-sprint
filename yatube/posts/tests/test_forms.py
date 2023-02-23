# deals/tests/tests_form.py
import shutil
import tempfile

from posts.forms import PostForm
from posts.models import Group

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title='Тестовый заголовок',
            description="Текстовое поле",
            slug='first'
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()

    def test_create_group(self):
        """Валидная форма создает запись в Group."""
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content_type='image/gif'
        )
        form_data = {
            'title': 'Тестовый заголовок',
            'text': 'Тестовый текст',
            'image': uploaded,
        }
        response = self.guest_client.post(
            reverse('deals:home'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse("posts:post_create"))
        self.assertTrue(
            Group.objects.filter(
                title='Тестовый заголовок',
                description="Текстовое поле",
                slug='first'
            ).exists()
        )

        # при отправке валидной формы со страницы редактирования поста
        # reverse('posts:post_edit', args=('post_id',))
        # происходит изменение поста с post_id в базе данных.
