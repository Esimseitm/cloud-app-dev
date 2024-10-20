import unittest
import requests

class LocalAppIntegrationTestCase(unittest.TestCase):

    BASE_URL = 'http://localhost:8080'

    def test_full_task_lifecycle(self):
        
        new_task = {"task": "Integration Test Task", "done": False}
        response = requests.post(f'{self.BASE_URL}/tasks', json=new_task)
        self.assertEqual(response.status_code, 201)
        created_task = response.json()
        self.assertIn("Integration Test Task", response.text)

        task_id = created_task['id']
        
        updated_task = {"task": "Updated Integration Test Task", "done": True}
        response = requests.put(f'{self.BASE_URL}/tasks/{task_id}', json=updated_task)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated Integration Test Task", response.text)

        response = requests.delete(f'{self.BASE_URL}/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Задача удалена", response.text)

if __name__ == '__main__':
    unittest.main()
