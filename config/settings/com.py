"""Django 4.2"""
import sys
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as message_constants
import os
import environ

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path("main")
CONF_DIR = ROOT_DIR.path("config")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()
env.read_env("Sample.env")

SECRET_KEY = os.environ.get(
    "SECRET_KEY", default="8na#(#x@0i*3ah%&$-q)b&wqu5ct_a3))d8-sqk-ux*5lol*wl"
)

DEBUG = bool(os.environ.get("DEBUG", ""))

SITE_ID = int(os.environ.get("SITE_ID", default="1"))

INSTALLED_APPS = [
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    # 'channels',
    "crequest",  # noqa
    "rest_framework",
    "main.api",
    "main.core",
    "main.users",
    "main.web",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "crequest.middleware.CrequestMiddleware",  # noqa
    "main.core.middleware.AjaxMiddleware",
    "main.core.middleware.TelnetConnectionMiddleware",
    "main.core.middleware.UserAgentMiddleware",
    "main.users.middleware.LastUserActivityMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(APPS_DIR.path("templates")),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "main.core.context_processors.site",
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

ASGI_APPLICATION = "config.asgi.application"

WSGI_APPLICATION = "config.wsgi.application"

ROOT_URLCONF = "config.urls"

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = ("main.users.backends.UserModelBackend",)

LOGIN_URL = "/account/login/"

ADMIN_URL = os.environ.get("ADMIN_URL", default="admin/")

LOCALE_PATHS = (
    str(APPS_DIR("locale")),
    str(CONF_DIR("locale")),
)

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", default="en")

LANGUAGES = (
    ("en", _("English")),
    ("tr", _("Türkçe")),
)

TIME_ZONE = os.environ.get("TIME_ZONE", default="UTC")

USE_I18N = True

USE_TZ = True

SITE_TITLE = "Jasmin site admin"
SITE_HEADER = "Jasmin administration"
INDEX_TITLE = "Dashboard administration"

SITE_NAME = os.environ.get("SITE_NAME", default="Jasmin Panel")
SITE_NAME_HTML = os.environ.get("SITE_NAME_HTML", default="<b>Jasmin</b> Panel")


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("HOST")  # Replace with your SMTP server
EMAIL_PORT = os.getenv("PORT")  # Replace with your SMTP server port
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("USERNAME")  # Replace with your email
EMAIL_HOST_PASSWORD = os.getenv("PASSWORD")

MESSAGE_TAGS = {
    message_constants.DEBUG: "info",
    message_constants.INFO: "info",
    message_constants.SUCCESS: "success",
    message_constants.WARNING: "warning",
    message_constants.ERROR: "danger",
}

STATIC_ROOT = str(ROOT_DIR("public/static"))

STATIC_URL = "/static/"

STATICFILES_DIRS = (
    str(
        APPS_DIR.path(
            "static",
        )
    ),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MEDIA_ROOT = str(ROOT_DIR("public/media"))

MEDIA_URL = "/media/"

REDIS_HOST = os.environ.get("REDIS_HOST", default="jasmin_redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", default=6379))
REDIS_DB = int(os.environ.get("REDIS_DB", default=0))
REDIS_URL = (REDIS_HOST, REDIS_PORT)

DEFAULT_USER_AVATAR = STATIC_URL + "assets/img/user.png"
DEFAULT_USER_FOLDER = "users"
LAST_ACTIVITY_INTERVAL_SECS = 3600

# REST API Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.CoreJSONRenderer",
        # 'rest_framework_swagger.renderers.SwaggerUIRenderer',
        # 'rest_framework_swagger.renderers.OpenAPIRenderer',
    ),
}

SWAGGER_SETTINGS = {
    "LOGIN_URL": "rest_framework:login",
    "LOGOUT_URL": "rest_framework:logout",
    "USE_SESSION_AUTH": True,
    "DOC_EXPANSION": "list",
    "APIS_SORTER": "alpha",
    "SHOW_REQUEST_HEADERS": True,
}

# Jasmin SMS Gateway Settings - telnet configurations
TELNET_HOST = os.environ.get("TELNET_HOST", default="127.0.0.1")
TELNET_PORT = int(os.environ.get("TELNET_PORT", default=8990))
TELNET_USERNAME = os.environ.get("TELNET_USERNAME", default="jcliadmin")  # noqa
# no alternative storing as plain text
TELNET_PW = os.environ.get("TELNET_PW", default="jclipwd")  # noqa
# reasonable value for intranet.
TELNET_TIMEOUT = int(os.environ.get("TELNET_TIMEOUT", default=10))
# There should be no need to change this
STANDARD_PROMPT = "jcli : "
# Prompt for interactive commands
INTERACTIVE_PROMPT = "> "
# This is used for DLR Report
SUBMIT_LOG = bool(os.environ.get("SUBMIT_LOG", "0"))

"""
SYSCTL_HEALTH_CHECK boolean field to enable Jasmin Health Check UI Monitoring
SYSCTL_HEALTH_CHECK_SERVICES list of available services:
- jasmin-celery
- jasmin-dlrd
- jasmin-dlrlookupd
- jasmin-interceptord
- jasmin-restapi
- jasmind
- sms_logger
Additional Services:
- redis
- rabbitmq
- postgresql
"""
SYSCTL_HEALTH_CHECK = os.environ.get("SYSCTL_HEALTH_CHECK", default=False)
SYSCTL_HEALTH_CHECK_SERVICES = os.environ.get(
    "SYSCTL_HEALTH_CHECK_SERVICES", default="jasmind"
)

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

CELERY_BROKER_URL = os.environ.get(
    "CELERY_BROKER_URL", default="redis://localhost:6379/0"
)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", default="redis://localhost:6379/0"
)


if "test" in sys.argv:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
