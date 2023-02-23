from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="NoName")
        cls.group = Group.objects.create(
            title="Титул",
            slug="slug",
            description="описание",
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text="Текст",
            group=cls.group,
        )

        cls.templates_pages_names = {
            reverse("posts:index"): "posts/index.html",
            reverse("posts:group_progect", kwargs={"slug": cls.group.slug}):
                "posts/group_progect.html",# не работает
            reverse(
                "posts:profile", kwargs={"username": cls.post.author}
            ): "posts/profile.html",
            reverse(
                "posts:post_detail", kwargs={"post_id": cls.post.id}
            ): "posts/post_detail.html",
            reverse(# не работает
                "posts:post_edit", kwargs={"post_id": cls.post.id}
            ): "posts/create_post.html",
            reverse("posts:post_create"): "posts/create_post.html",# не работает
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostPagesTests.user)

    def test_adres(self):
        """Адрес использует соответствующий шаблон"""
        for template, reverse_name in self.templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(template)
                self.assertTemplateUsed(response, reverse_name)

    def test_index(self):
        """index соответствует ожидаемому контексту"""
        expected = list(Post.objects.all()[:10])
        response = self.guest_client.get(reverse("posts:index"))
        self.assertEqual(list(response.context["page_obj"]), expected)

    def test_group(self):
        """group_progect соответствует ожидаемому контексту"""
        expected = list(Post.objects.filter(group_id=self.group.id)[:10])
        response = self.guest_client.get(
            reverse("posts:group_progect", kwargs={"slug": self.group.slug})
        )
        self.assertEqual(list(response.context["page_obj"]), expected)

    def test_profile(self):
        """profile соответствует ожидаемому контексту"""
        response = self.guest_client.get(
            reverse("posts:profile", args=(self.post.author,))
        )
        expected = list(Post.objects.filter(author_id=self.user.id)[:10])
        self.assertEqual(list(response.context["page_obj"]), expected)

    def test_post_detail(self):
        """post_detail соответствует ожидаемому контексту"""
        response = self.guest_client.get(
            reverse("posts:post_detail", kwargs={"post_id": self.post.id})
        )
        self.assertEqual(response.context.get("post").group, self.post.group)
        self.assertEqual(response.context.get("post").author, self.post.author)
        self.assertEqual(response.context.get("post").text, self.post.text)

    def test_post_edit(self):
        """post_edit соответствует ожидаемому контексту"""
        response = self.authorized_client.get(
            reverse("posts:post_edit", kwargs={"post_id": self.post.id})
        )
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_create(self):
        """create соответствует ожидаемому контексту"""
        response = self.authorized_client.get(reverse("posts:post_create"))
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.models.ModelChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_group_test(self):
        """Проверяем создание поста на страницах с выбранной группой"""
        form_fields = {
            reverse("posts:index"): Post.objects.get(group=self.post.group),
            reverse(
                "posts:profile", kwargs={"username": self.post.author}
            ): Post.objects.get(group=self.post.group),
            reverse(
                "posts:group_progect", kwargs={"slug": self.group.slug}
            ): Post.objects.get(group=self.post.group),
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                response = self.authorized_client.get(value)
                form_field = response.context["page_obj"]
                self.assertIn(expected, form_field)

    def test_group_not_in_post(self):
        """Проверка пост не попал в группу, для которой не был предназначен"""
        form_fields = {
            reverse(
                "posts:group_progect", kwargs={"slug": self.group.slug}
            ): Post.objects.exclude(group=self.post.group),
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                response = self.authorized_client.get(value)
                form_field = response.context["page_obj"]
                self.assertNotIn(expected, form_field)
