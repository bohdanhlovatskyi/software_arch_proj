from domain.userinfo import UserInfo
from repository.auth import create_user, check_password, get_current_user_by_id
from service.jwt import create_access_token




def register(user: UserInfo):
    print(f'[INFO] Registering new user: \nLogin: {user.login}')
    new_user = create_user(user)
    print("[INFO] Registration complected")
    return new_user.json()


def login(payload: UserInfo):
    print("[INFO] Login user: " + payload.login)
    login = check_password(payload)
    user = login.json()
    print("[INFO] Generating JWT for: " + payload.login)

    jwt_token = create_access_token(data={
        'login': payload.login,
        'id': user['id']
    })

    user = get_current_user_by_id(user['id'])

    return {
        'token': jwt_token,
        'status': 'success',
        'user': user.json()
    }