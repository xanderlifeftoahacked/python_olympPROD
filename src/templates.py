
def profile(user_data):
    return f'''    <u>Ваш профиль</u>

    Возраст: <b>{user_data['age']}</b>
    Описание: <b>{user_data['bio']}</b>
    Местоположение: <b>{user_data['city']}</b>

        '''
