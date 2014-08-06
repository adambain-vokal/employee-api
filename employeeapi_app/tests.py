from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class AuthTests(APITestCase):
    fixtures = ['test.json',]

    def test_get_auth_token(self):
        """
        Make sure we can get an auth token via the API.
        """
        url = reverse('rest_framework.authtoken.views.obtain_auth_token')
        data = {'username': 'root', 'password':'toor'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_get_auth_token_reg(self):
        """
        Make sure we can get an auth token via the API.
        """
        url = reverse('rest_framework.authtoken.views.obtain_auth_token')
        data = {'username': 'root', 'password':'toor'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_auth_token_fail(self):
        """
        Make sure non-existant users can't get a token.
        """
        url = reverse('rest_framework.authtoken.views.obtain_auth_token')
        data = {'username': 'nobody', 'password':'definitely_wrong'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)


class EmployeeCreate(APITestCase):
    fixtures = ['test.json']

    def setUp(self):
        url = reverse('rest_framework.authtoken.views.obtain_auth_token')
        data = {'username': 'root', 'password':'toor'}
        response = self.client.post(url, data, format='json')
        self.token = response.data['token']
        data = {'username': 'reg', 'password':'reg'}
        response = self.client.post(url, data, format='json')
        self.regular_token = response.data['token']

    def test_employee_create(self):
        """
        Test that we can POST to create an employee
        """
        url = reverse('employee-list')
        data = {'first_name': 'John', 'last_name': 'Doe', 'title':'Manager'}
        response = self.client.post(url, data, format='json',
                                    HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual({k:v for k,v in response.data.iteritems() if k != 'url'}, data)

    def test_employee_create_no_permission_fail(self):
        """
        Test that we can not POST to create an employee without proper permissions
        """
        url = reverse('employee-list')
        data = {'first_name': 'John', 'last_name': 'Doe', 'title':'Manager'}
        response = self.client.post(url, data, format='json',
                                    HTTP_AUTHORIZATION="Token " + self.regular_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_employee_create_unauth_fail(self):
        """
        Test that we cannot create employees without authenticating
        """
        url = reverse('employee-list')
        data = {'first_name': 'John', 'last_name': 'Doe', 'title':'Manager'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_employee_create_not_enough_fields_fail(self):
        """
        Test failing a create if not enough fields are provided
        """
        url = reverse('employee-list')
        data = {'first_name': 'John', 'last_name': 'Doe'}
        response = self.client.post(url, data, format='json',
                                    HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employee_create_too_long_name_fail(self):
        """
        Test failing a create if the first_name is too long
        """
        url = reverse('employee-list')
        data = {
            'first_name': 'Johniddasfeufhfweffsdfdsbvsdvdsuhfiuhwefwef', 
            'last_name': 'Doe', 'title':'Manager'}
        response = self.client.post(url, data, format='json',
                                    HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class EmployeeList(APITestCase):
    fixtures = ['test.json', 'employees.json']

    def test_list_employees(self):
        """
        Test that listing all employees returns the two initialized
        """
        url = reverse('employee-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class EmployeeGet(APITestCase):
    fixtures = ['test.json', 'employees.json']

    def test_get_employee(self):
        """
        Test getting an individual employee by pk out of the API
        """
        url = reverse('employee-detail', kwargs={'pk':'1'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "John")

    def test_get_employee_pk_not_found_fail(self):
        """
        Test that the API 404's on an pk that is not found
        """
        url = reverse('employee-detail', kwargs={'pk':'3'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_employee_pk_improper_fail(self):
        """
        Test that the API handles an improper pk
        """
        url = reverse('employee-detail', kwargs={'pk':'John'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class EmployeePut(APITestCase):
    fixtures = ['test.json', 'employees.json']

    def setUp(self):
        url = reverse('rest_framework.authtoken.views.obtain_auth_token')
        data = {'username': 'root', 'password':'toor'}
        response = self.client.post(url, data, format='json')
        self.token = response.data['token']
        data = {'username': 'reg', 'password':'reg'}
        response = self.client.post(url, data, format='json')
        self.regular_token = response.data['token']
    
    def test_put_employee(self):
        """
        Test that we can update an employee via PUT
        """
        url = reverse('employee-detail', kwargs={'pk':'1'})
        data = {'first_name': 'Johnny', 'last_name': 'Doe', 'title':'Manager'}
        response = self.client.put(url, data, format='json',
                                   HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Johnny")
    
    def test_put_employee_no_permission_fail(self):
        """
        Test that we can not PUT an employee without proper permissions
        """
        url = reverse('employee-detail', kwargs={'pk':'1'})
        data = {'first_name': 'John', 'last_name': 'Doe', 'title':'Manager'}
        response = self.client.put(url, data, format='json',
                                    HTTP_AUTHORIZATION="Token " + self.regular_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_put_employee_unauth_fail(self):
        """
        Test that we cannot modify employees without authenticating
        """
        url = reverse('employee-detail', kwargs={'pk':'1'})
        data = {'first_name': 'John', 'last_name': 'Doe', 'title':'Manager'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_employee_partial_fail(self):
        """
        Test that a partial update will be rejected
        """
        url = reverse('employee-detail', kwargs={'pk':'7'})
        data = {'first_name': 'Jane', 'title':'Manager'}
        response = self.client.put(url, data, format='json',
                                   HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_put_employee_not_found_pk_create(self):
        """
        Test that a not found pk creates a new object
        """
        url = reverse('employee-detail', kwargs={'pk':'3'})
        data = {'first_name': 'Michael', 'last_name':'Bolton', 'title':'Engineer'}
        response = self.client.put(url, data, format='json',
                                   HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['url'] = 'http://testserver' + url
        self.assertEqual(response.data, data)

    def test_put_employee_too_long_name_fail(self):
        """
        Test failing a PUT if the first_name is too long
        """
        url = reverse('employee-detail', kwargs={'pk':'1'})
        data = {
            'first_name': 'Johniddasfeufhfweffsdfdsbvsdvdsuhfiuhwefwef', 
            'last_name': 'Doe', 'title':'Manager'}
        response = self.client.put(url, data, format='json',
                                    HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class EmployeePatch(APITestCase):
    fixtures = ['test.json', 'employees.json']

    def setUp(self):
        url = reverse('rest_framework.authtoken.views.obtain_auth_token')
        data = {'username': 'root', 'password':'toor'}
        response = self.client.post(url, data, format='json')
        self.token = response.data['token']
        data = {'username': 'reg', 'password':'reg'}
        response = self.client.post(url, data, format='json')
        self.regular_token = response.data['token']
    
    def test_patch_employee(self):
        """
        Test that we can update an employee via PATCH
        """
        url = reverse('employee-detail', kwargs={'pk':'1'})
        data = {'first_name': 'Johnny'}
        response = self.client.patch(url, data, format='json',
                                   HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Johnny")
    
    def test_patch_employee_no_permission_fail(self):
        """
        Test that we can not PATCH an employee without proper permissions
        """
        url = reverse('employee-detail', kwargs={'pk':'1'})
        data = {'first_name': 'John', 'last_name': 'Doe', 'title':'Manager'}
        response = self.client.patch(url, data, format='json',
                                    HTTP_AUTHORIZATION="Token " + self.regular_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_patch_employee_unauth_fail(self):
        """
        Test that we cannot modify employees without authenticating
        """
        url = reverse('employee-detail', kwargs={'pk':'1'})
        data = {'first_name': 'John', 'last_name': 'Doe', 'title':'Manager'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_employee_not_found_pk_fail(self):
        """
        Test that a not found pk gives a 404
        """
        url = reverse('employee-detail', kwargs={'pk':'6'})
        data = {'title':'Engineer'}
        response = self.client.patch(url, data, format='json',
                                   HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_employee_no_data(self):
        """
        Test that PATCH with no data is ok
        """
        url = reverse('employee-detail', kwargs={'pk':'1'})
        data = {}
        response = self.client.patch(url, data, format='json',
                                   HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "John")

    def test_patch_employee_too_long_name_fail(self):
        """
        Test failing a PATCH if the first_name is too long
        """
        url = reverse('employee-detail', kwargs={'pk':'1'})
        data = {'first_name': 'Johniddasfeufhfweffsdfdsbvsdvdsuhfiuhwefwef'}
        response = self.client.patch(url, data, format='json',
                                    HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class EmployeeDelete(APITestCase):
    fixtures = ['test.json', 'employees.json']

    def setUp(self):
        url = reverse('rest_framework.authtoken.views.obtain_auth_token')
        data = {'username': 'root', 'password':'toor'}
        response = self.client.post(url, data, format='json')
        self.token = response.data['token']
        data = {'username': 'reg', 'password':'reg'}
        response = self.client.post(url, data, format='json')
        self.regular_token = response.data['token']

    def test_delete_employee(self):
        """
        Test that we can delete an employee
        """
        url = reverse('employee-detail', kwargs={'pk':'1'})
        response = self.client.delete(url, HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url, HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_employee_no_permission_fail(self):
        """
        Test that we can not DELETE an employee without proper permissions
        """
        url = reverse('employee-detail', kwargs={'pk':'7'})
        response = self.client.delete(url, format='json',
                                      HTTP_AUTHORIZATION="Token " + self.regular_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_employee_unauth_fail(self):
        """
        Test that we cannot delete employees without authenticating
        """
        url = reverse('employee-detail', kwargs={'pk':'7'})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_employee_not_found_pk_fail(self):
        """
        Test that a not found pk gives a 404
        """
        url = reverse('employee-detail', kwargs={'pk':'6'})
        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
