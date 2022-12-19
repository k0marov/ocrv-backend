from . import config

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    config.FRONTEND_URL,
]
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

# ===== Localization and Internationalization =====
LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', 'Russian'),
)
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

