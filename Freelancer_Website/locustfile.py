import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):        

    @task
    def hello_world(self):
        self.client.get("profile/")
        self.client.get("search/")
        self.client.get("provide_service/")
        self.client.get("edit_profile/")
        self.client.get("tickets/")
        self.client.get("updateprofile/")
        self.client.get("wishlist/")
        self.client.get("cart/")
        self.client.get("ticket_list/")
        self.client.get("invite/")
        self.client.get("activity/")
        self.client.get("mainchat/")

    def on_start(self):
        response = self.client.get('login/') # load the login page
        csrf_token = response.cookies['csrftoken'] # extract the CSRF token from the response cookie
        login_data = {'username': 'SI_GNANA', 'password': 'Ranju@23', 'csrfmiddlewaretoken': csrf_token}
        response = self.client.post('login/', data=login_data) # submit the login form with the credentials