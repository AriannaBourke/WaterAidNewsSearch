from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(5, 15)

    @task(1)
    def get_token(self):
        self.client.get("/login")

    @task(2)
    def logout(self):
        self.client.get("/logout")

    @task(3)
    def trends(self):
        self.client.get("/trends")

    @task(4)
    def search_results(self):
        self.client.get("/search_results?search=water+shortage")

    @task(5)
    def account(self):
        self.client.get("/account")

    @task(6)
    def article(self):
        self.client.get("/article/JhplaTZRDV3tbn3MC0u_iFW79YNqgwEnw6lSP5IKiJFjqNUO8aIls9zqcxVhLFpD")

    @task(7)
    def help(self):
        self.client.get("/help")
    
    @task(8)
    def register(self):
        self.client.get("/register")

    @task(9)
    def home(self):
        self.client.get("/")
