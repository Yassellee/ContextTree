import requests, time, json


def examine_key_validity():
    url = "http://166.111.139.133:2260/Context/test_key"

    # send a get request every 10 minutes
    while True:
        try:
            response = requests.get(url, timeout=10)
            print(response.json().get("data"), flush=True)
        except Exception as e:
            print("Error when examining key from database: {}".format(e))

        time.sleep(600)


def main():
    examine_key_validity()


if __name__ == "__main__":
    main()
