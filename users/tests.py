from rest_framework.test import APITestCase
from rest_framework import status

class TasksAPITestCase(APITestCase):
    
    def setUp(self):

        self.user_data = {
            'username': 'john_admin',
            'password': '12345',
            'email': 'john@admin.com',
            'first_name': 'John',
            'last_name': 'Admin',
            'birthdate': '2000-01-01',
            'is_employee': True
        }
        
        self.register_user_url = 'register-users/'

    
    def test_post_register_user(self):
        register_user = self.client.post(f"/api/{self.register_user_url}", self.user_data, format='json')
        
        expected_response = {'id': 1, 'username': 'john_admin', 'email': 'john@admin.com', 'birthdate': '2000-01-01', 'first_name': 'John', 'last_name': 'Admin', 'is_employee': True, 'is_superuser': True}

        self.assertEqual(register_user.status_code, 201)
        self.assertEqual(expected_response, register_user.json())

        invalid_data = {
            'username': 'john_admin',
            'password': '12345',
            'email': 'john@admin.com',
            'first_name': 'John',
            'last_name': 'Admin',
            'birthdate': '2000/01/01',
            'is_employee': "true"
        }

        post_invalid_data = self.client.post(f"/api/{self.register_user_url}", invalid_data, format='json')
        self.assertEqual(post_invalid_data.status_code, 400)

        duplicate_username_data = {
            'username': 'john_admin',
            'password': '54321',
            'email': 'peter@admin.com',
            'first_name': 'Peter',
            'last_name': 'Admin',
            'birthdate': '2000-01-01',
            'is_employee': True
        }

        post_duplicate_username = self.client.post(f"/api/{self.register_user_url}", duplicate_username_data, format='json')        
        expected_duplicate_username_response = {'username': ['username already taken.']}

        self.assertEqual(post_duplicate_username.status_code, 400)
        self.assertEqual(expected_duplicate_username_response, post_duplicate_username.json())

        duplicate_email_data = {
            'username': 'peter_admin',
            'password': '54321',
            'email': 'john@admin.com',
            'first_name': 'Peter',
            'last_name': 'Admin',
            'birthdate': '2000-01-01',
            'is_employee': True
        }

        post_duplicate_email = self.client.post(f"/api/{self.register_user_url}", duplicate_email_data, format='json')
        expected_duplicate_email_response = {'email': ['email already registered.']}

        self.assertEqual(post_duplicate_email.status_code, 400)
        self.assertEqual(expected_duplicate_email_response, post_duplicate_email.json())
