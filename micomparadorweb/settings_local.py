DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ISO',
        'USER': 'remoto',
        'PASSWORD': '1234',
        'HOST': '212.47.235.212',  # Tu dirección IP de MySQL
        'PORT': '3306',  # Puerto por defecto de MySQL
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    }
}


SECRET_KEY = 'django-insecure-@ii#+xed2d+kukpn0(b=$7k8^zcpvo4!(@m@#s6shgh35@cpm-'