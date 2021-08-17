from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is not provided')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is not provided')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=25, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import hashlib
        string = self.email + (str(id))
        encode = string.encode()
        mg5 = hashlib.md5(encode)
        activation_code = hashlib.hexdigest(mg5)
        self.activation_code = activation_code

    """
    IN SETTINGS:
        STATIC_ROOT = os.path.join(BASE_DIR, 'static')

        MEDIA_URL = '/media/'
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
        
        AUTH_USER_MODEL = 'account.CustomUser'
        
        EMAIL_BACKEND = 'django.core.main.backends.console.EmailBackend'
        #2
        admin.site.register(CustomUser)
    """