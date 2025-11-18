import requests
import factory


class UserFactory(factory.Factory):
    class Meta:
        model = dict

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    password = factory.Sequence(lambda n: f"@test{n}")



for _ in range(1000):
    user_data = UserFactory()

    resp = requests.post(
        "https://fast-api-k9as.onrender.com/user/Create_Account",
        json=user_data
    )

    print(resp.status_code)
    try:
        print(resp.json())
    except:
        print(resp.text)

    login = requests.post(
        'https://fast-api-k9as.onrender.com/auth/Login',
        json={
            'username': user_data['email'],
            'password': user_data['password'],
        }
    )

    print(resp.status_code)
    try:
        print(resp.json())
    except:
        print(resp.text)