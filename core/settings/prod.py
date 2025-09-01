from .base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]

# Database overrides for production
DATABASES["default"].update({
    "NAME": os.environ["DB_NAME"],
    "USER": os.environ["DB_USER"],
    "PASSWORD": os.environ["DB_PASSWORD"],
    "HOST": os.environ["DB_HOST"],
    "PORT": os.environ.get("DB_PORT", "5432"),
})

# Allow frontend to access API without CORS restrictions
CORS_ALLOW_ALL_ORIGINS = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

