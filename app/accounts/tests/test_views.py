from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail


def create_user(**params):
    return get_user_model().objects.create_user(**params)


User = get_user_model()


class PublicViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')
        self.feedback_url = reverse('accounts:feedback')

    def test_create_user_with_empty_username(self):
        """
        Test create user with empty username fails
        """
        data = {
            'username': '', 'password1': '12345sss',
            'password2': '12345sss'
        }
        res = self.client.post(
            self.signup_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        dict_res = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertIn('Обязательное поле.', dict_res['errors'])
        self.assertFalse(dict_res['success'])

    def test_create_user_with_short_password(self):
        """
        Test create user with short password fails
        """
        data = {'username': 'test', 'password1': '123', 'password2': '123'}
        res = self.client.post(
            self.signup_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        dict_res = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertIn(
            'Введённый пароль слишком короткий. Он должен содержать ' +
            'как минимум 8 символов.', dict_res['errors']
        )

    def test_create_user_same_username(self):
        """
        Test create user with username already taked fails
        """
        create_user(username='test', password='passtest123')
        data = {
            'username': 'test', 'password1': '123xxxc123',
            'password2': '123xxxc123'
        }
        res = self.client.post(
            self.signup_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        dict_res = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertFalse(dict_res['success'])
        self.assertIn(
            'Пользователь с таким именем уже существует.', dict_res['errors']
        )

    def test_create_user_successfully(self):
        """
        Test user with valid credentials successfull created
        """
        data = {
            'username': 'test', 'password1': '1234567test',
            'password2': '1234567test'
        }
        res = self.client.post(
            self.signup_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        user = User.objects.filter(username=data['username']).first()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(user.check_password(data['password1']))

    def test_user_login_with_invalid_credentials(self):
        """
        Test user login with invalid credentials fails
        """
        data = {'username': 'test', 'password': '1234567test'}
        create_user(**data)
        invalid_data = {'username': 'test', 'password': '7test'}

        res = self.client.post(
            self.login_url, invalid_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        dict_res = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertIn(
            'Введите правильное имя пользователя и пароль', dict_res['errors']
        )
        self.assertFalse(dict_res['success'])

    def test_user_login_successfully(self):
        """
        Test user login with valid credentials success
        """
        data = {'username': 'test', 'password': '1234567test'}
        create_user(**data)
        res = self.client.post(
            self.login_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        dict_res = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(dict_res['success'])

    def test_get_feedback_page_redirected(self):
        """
        Test get feedback page unuthorized user redirected
        """
        res = self.client.get(self.feedback_url)
        self.assertEqual(res.status_code, 302)


class PrivateViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = create_user(username='test', password='1234567test')
        self.client.force_login(self.user)
        self.feedback_url = reverse('accounts:feedback')

    def test_get_feedback_page(self):
        """
        Test get feedback page
        """
        res = self.client.get(self.feedback_url)
        self.assertEqual(res.status_code, 200)

    def test_send_feedback_with_empty_email(self):
        """
        Test feedback send fails
        """
        sender = ''
        body = (
            'Давно выяснено, что при оценке дизайна и композиции читаемый '
            'текст мешает сосредоточиться. Lorem Ipsum используют потому,'
            ' что тот обеспечивает более или менее стандартное'
            ' заполнение шаблона.'
        )
        data = {'sender': sender, 'body': body}
        res = self.client.post(
            self.feedback_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        dict_res = res.json()
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(dict_res['success'])
        self.assertIn('Обязательное поле.', dict_res['errors'])

    def test_send_feedback_with_empty_body(self):
        """
        Test feedback send fails
        """
        sender = 'sender@iii.com'
        body = ''
        data = {'sender': sender, 'body': body}
        res = self.client.post(
            self.feedback_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        dict_res = res.json()
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(dict_res['success'])
        self.assertIn('Обязательное поле.', dict_res['errors'])

    def test_send_feedback_to_admin_success(self):
        """
        Test feedback sended successfully
        """
        data = {
            'username': 'admin', 'password': '333admin',
            'email': 'admin@admin.a', 'is_superuser': True
        }
        create_user(**data)

        sender = 'sender@iii.com'
        body = (
            'Давно выяснено, что при оценке дизайна и композиции читаемый '
            'текст мешает сосредоточиться. Lorem Ipsum используют потому,'
            ' что тот обеспечивает более или менее стандартное'
            ' заполнение шаблона.'
        )
        data = {'sender': sender, 'body': body}
        res = self.client.post(
            self.feedback_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        dict_res = res.json()
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(dict_res['success'])
        self.assertIn('Письмо успешно отправлено', dict_res['message'])
