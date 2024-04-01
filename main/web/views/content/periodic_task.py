import threading
import time
from django.test import RequestFactory

from main.web.views.content.user_stats import user_stat_view_manage


def run_periodic_task():
    while True:
        # Create a fake HTTP request
        request_factory = RequestFactory()
        request = request_factory.get("/users_stats/manage/", {"s": "list"})

        # Call the view function directly
        response = user_stat_view_manage(request)

        # Do something with the response, if needed
        print(response.status_code)
        print(response.content)

        # Wait for 5 seconds before executing the task again
        time.sleep(5)


if __name__ == "__main__":
    # Start the periodic task in a separate thread
    thread = threading.Thread(target=run_periodic_task)
    thread.start()
