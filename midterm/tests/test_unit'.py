import unittest
import requests

class LocalAppTestCase(unittest.TestCase):

    BASE_URL = 'http://127.0.0.1:8080/'

    def test_index(self):
        """Test the index route"""
        response = requests.get(f'{self.BASE_URL}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("To-DO list by Midterm tsk!", response.text)

    def test_get_tasks(self):
        """Test retrieving the tasks"""
        response = requests.get(f'{self.BASE_URL}/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Cloud-app-dev: Assignment 3", response.text)

    def test_add_task(self):
        """Test adding a new task"""
        new_task = {"task": "Test Task", "done": False}
        response = requests.post(f'{self.BASE_URL}/tasks', json=new_task)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Test Task", response.text)

    def test_update_task(self):
        """Test updating an existing task"""
        updated_task = {"task": "Updated Test Task", "done": True}
        response = requests.put(f'{self.BASE_URL}/tasks/1', json=updated_task)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated Test Task", response.text)

    def test_delete_task(self):
        """Test deleting a task"""
        response = requests.delete(f'{self.BASE_URL}/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Задача удалена", response.text)

if __name__ == '__main__':
    unittest.main()
