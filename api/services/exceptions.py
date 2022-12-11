from rest_framework.views import exception_handler
from googletrans import Translator

translator = Translator()


def custom_exception_handler(exc, content):
    response = exception_handler(exc, content)
    if response.status_code == 401:
        response.data['detail'] = 'Вы не вошли в свой аккаунт!'
    elif response.status_code == 403:
        response.data['detail'] = 'Отказано в доступе!'
    else:
        translated = translator.translate(response.data['detail'], dest='ru', src='en')
        response.data['detail'] = translated.text
    return response
