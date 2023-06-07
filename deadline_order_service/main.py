import schedule
import requests
import environ

env = environ.Env()
environ.Env.read_env()

def check_and_set_overdue_deadline_status():
    response = requests.post(
        env("SERVICE_URL") + "/api/orders/deadline_check_service/")
    print(response)


def main():
    schedule.every().day.at('07:49').do(check_and_set_overdue_deadline_status)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()