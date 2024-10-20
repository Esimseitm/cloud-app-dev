from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_tasks(self):
        """Simulate a user fetching tasks"""
        self.client.get("/tasks")

    @task
    def add_task(self):
        """Simulate a user adding a new task"""
        self.client.post("/tasks", json={"task": "Load Test Task", "done": False})

    @task
    def update_task(self):
        """Simulate a user updating a task"""
        self.client.put("/tasks/1", json={"task": "Updated Load Test Task", "done": True})

    @task
    def delete_task(self):
        """Simulate a user deleting a task"""
        self.client.delete("/tasks/1")
