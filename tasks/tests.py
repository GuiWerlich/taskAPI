from rest_framework.test import APITestCase

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
        
        register_user_url = 'register-users/'

        register_user = self.client.post(f"/api/{register_user_url}", self.user_data, format='json')

        login_data = {
            'username': 'john_admin',
            'password': '12345'
        }

        login_url = 'users/login/'

        user_login = self.client.post(f"/api/{login_url}", login_data, format='json')

        response = user_login.json()

        self.access_token = response['access']

        self.tasks_url = 'tasks/'

        self.post_task_data_1 = {
            "title": "Bate papo com a equipe",
            "description": "Reunião para discutir o progresso do projeto e definir próximas etapas.",
            "due_date": "2024-10-25"
        }


    
    def test_post_tasks(self):

        post_task = self.client.post(f"/api/{self.tasks_url}", self.post_task_data_1, HTTP_AUTHORIZATION=f'Bearer {self.access_token}', format='json')
       
        self.assertEqual(post_task.status_code, 201)

        missing_fields_data = {
            "title": "Bate papo com a equipe",
            "description": "Reunião para discutir o progresso do projeto e definir próximas etapas.",
        }

        invalid_data = {
            "title": True,
            "description": "Reunião para discutir o progresso do projeto e definir próximas etapas.",
            "due_date": '25/10/2024'
        }

        post_missing_fields = self.client.post(f"/api/{self.tasks_url}", missing_fields_data, HTTP_AUTHORIZATION=f'Bearer {self.access_token}', format='json')
        self.assertEqual(post_missing_fields.status_code, 400)

        post_invalid_data = self.client.post(f"/api/{self.tasks_url}", invalid_data, HTTP_AUTHORIZATION=f'Bearer {self.access_token}', format='json')
        self.assertEqual(post_invalid_data.status_code, 400)

        post_invalid_credentials = self.client.post(f"/api/{self.tasks_url}", self.post_task_data_1, HTTP_AUTHORIZATION=f'Bearer 1234', format='json')
        self.assertEqual(post_invalid_credentials.status_code, 401)


    def test_get_tasks(self):
        id = self.client.post(f"/api/{self.tasks_url}", self.post_task_data_1, HTTP_AUTHORIZATION=f'Bearer {self.access_token}', format='json').json()['id']

        get_all = self.client.get(f"/api/{self.tasks_url}", HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(get_all.status_code, 200)
        
        get_by_id = self.client.get(f"/api/{self.tasks_url}{id}/", HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(get_by_id.status_code, 200)

        get_by_filter_due_date = self.client.get(f"/api/{self.tasks_url}?due_date=2024-10-25", HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(get_by_filter_due_date.status_code, 200)

        invalid_due_date = self.client.get(f"/api/{self.tasks_url}?due_date=2024", HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        expected_invalid_due_date_response = {"message": "Invalid due_date format. Use YYYY-MM-DD."}
        self.assertEqual(invalid_due_date.status_code, 400)
        self.assertEqual(expected_invalid_due_date_response, invalid_due_date.json())

        not_found_due_date = self.client.get(f"/api/{self.tasks_url}?due_date=2034-05-03", HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        expected_not_found_due_date_response = {"message": "No tasks found with the given due_date"}
        self.assertEqual(not_found_due_date.status_code, 404)
        self.assertEqual(expected_not_found_due_date_response, not_found_due_date.json())

        case_insensitive_title = self.client.get(f"/api/{self.tasks_url}?title=BATE%20PAPO%20COM%20A%20EQUIPE", HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(case_insensitive_title.status_code, 200)

        not_found_title = self.client.get(f"/api/{self.tasks_url}?title=abobrinha", HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        not_found_title_expected_response = {"message": "No tasks found with the given title"}
        self.assertEqual(not_found_title.status_code, 404)
        self.assertEqual(not_found_title_expected_response, not_found_title.json())


        get_invalid_credentials = self.client.get(f"/api/{self.tasks_url}", HTTP_AUTHORIZATION=f'Bearer 1234')
        self.assertEqual(get_invalid_credentials.status_code, 401)

        get_not_found_task = self.client.get(f"/api/{self.tasks_url}1234/", HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(get_not_found_task.status_code, 404)
    

    def test_put_tasks(self):
        id = self.client.post(f"/api/{self.tasks_url}", self.post_task_data_1, HTTP_AUTHORIZATION=f'Bearer {self.access_token}', format='json').json()['id']

        put_data = {
            "title": "Revisar conceitos de Django",
            "description": "Estudar os principais conceitos do Django para melhorar o conhecimento do framework.",
            "due_date": "2024-08-30"
        }

        put_partial_data = {
            "due_date": "2025-08-30"
        }

        put_task = self.client.put(f"/api/{self.tasks_url}{id}/", put_data, HTTP_AUTHORIZATION=f'Bearer {self.access_token}', format='json')
        self.assertEqual(put_task.status_code, 200)

        put_task_with_partial_data = self.client.put(f"/api/{self.tasks_url}{id}/", put_partial_data, HTTP_AUTHORIZATION=f'Bearer {self.access_token}', format='json')
        self.assertEqual(put_task_with_partial_data.status_code, 200)

        put_empty_data = self.client.put(f"/api/{self.tasks_url}{id}/", HTTP_AUTHORIZATION=f'Bearer {self.access_token}', format='json')
        self.assertEqual(put_empty_data.status_code, 400)

        empty_data_expected_response = {'message': 'No data provided. Accepted fields: title, description, due_date'}
        self.assertEqual(empty_data_expected_response, put_empty_data.json())
        
        put_invalid_credentials = self.client.put(f"/api/{self.tasks_url}{id}/", put_data, HTTP_AUTHORIZATION=f'Bearer 1234', format='json')
        self.assertEqual(put_invalid_credentials.status_code, 401)

        not_found_task = self.client.put(f"/api/{self.tasks_url}1234/", HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(not_found_task.status_code, 404)
    

    def test_delete_tasks(self):
        id = self.client.post(f"/api/{self.tasks_url}", self.post_task_data_1, HTTP_AUTHORIZATION=f'Bearer {self.access_token}', format='json').json()['id']

        delete_task = self.client.delete(f"/api/{self.tasks_url}{id}/", HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(delete_task.status_code, 204)  

        delete_invalid_credentials = self.client.delete(f"/api/{self.tasks_url}{id}/", HTTP_AUTHORIZATION=f'Bearer 1234')
        self.assertEqual(delete_invalid_credentials.status_code, 401)

        delete_same_task = self.client.delete(f"/api/{self.tasks_url}{id}/", HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(delete_same_task.status_code, 404)

        delete_not_found_task = self.client.delete(f"/api/{self.tasks_url}1234/", HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(delete_not_found_task.status_code, 404)



        

        




        


