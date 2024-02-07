import requests

proxy_list = []


def get_proxy_list():
    response = requests.get("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt")
    for i in response.text.splitlines():
        proxy_list.append("http://" + i)

def check_proxy():
    pass


if __name__ == "__main__":
    get_proxy_list()
    print(proxy_list)
