from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


class User(AbstractUser):
    CATEGORY_CHOICES = (
        ("Female", "Female"),
        ("Male", "Male"),
        ("Alien", "Alien"),
    )
    # 이메일 중복허용x Emailvalidator로 유효성검사
    email = models.EmailField(
        max_length=255, unique=True, validators=[EmailValidator()])
    # 비밀번호, 이메일, 이름, 닉네임, 생일 필수 입력하며 성별, 자기소개 생략 가능
    name = models.CharField(max_length=30, null=False, blank=False)
    nickname = models.CharField(max_length=30, null=False, blank=False)
    birth = models.DateField(null=False, blank=False)
    category = models.CharField(max_length=6, choices=CATEGORY_CHOICES)
    introduce = models.TextField(max_length=200, blank=True)
