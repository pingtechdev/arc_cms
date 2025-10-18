lsettings = {
    'db_name': 'arc_cms',
    'db_user': 'arc_user',
    'db_pass': 'your_secure_password',
    'db_host': 'localhost',
    'db_port': '3306',

    'MAIN_LOG_FILE': '/var/log/arc',
    'MEDIA_ROOT': '/home/ubuntu/projects/arc-deploy/arc_cms/media',
    'MEDIA_URL': '/media/',
    'STATIC_ROOT': '/home/ubuntu/projects/arc-deploy/arc_cms/staticfiles',
    'STATIC_URL': '/static/',

    'DEBUG': False,
    'IS_MAINTENANCE': False,
    'PROD': True,
    'ENABLE_EMAIL_HANDLER': True,

    'ALLOWED_HOSTS': ['api.arc.pingtech.dev', 'arc.pingtech.dev', 'localhost', '127.0.0.1'],
    'CORS_ORIGIN_WHITELIST': ["https://arc.pingtech.dev"],
    'CORS_ALLOW_ALL_ORIGINS': False,
    'CORS_ALLOWED_ORIGINS': [
        'https://arc.pingtech.dev',
        'https://api.arc.pingtech.dev',
    ],
    'IS_MAINTENANCE': False,
    'DEPLOY_LOCATION': 'PRODUCTION'
}
