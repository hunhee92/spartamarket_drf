from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    # 쓰기전용 데이터 전송할때 password 필드 안보임
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            nickname=validated_data['nickname'],
            birth=validated_data['birth'],
            category=validated_data['category']
        )
        user.set_password(validated_data['password'])  # 비밀번호 해싱하긔
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'email': {'required': True},
            'nickname': {'required': True},
            'name': {'required': True},
            'birth': {'required': True},
        }


class UserDeleteSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("이전 비밀번호가 올바르지 않습니다.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        print("기존 비밀번호 동일한가 ?")
        if not user.check_password(value):
            print("동일하지 않다 ")
            raise serializers.ValidationError("이전 비밀번호가 올바르지 않습니다.")
        print("동일하다")
        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        validate_password(value)  # validate_password 장고의 비밀번호 유효성 검사
        if user.check_password(value):
            print("새 비밀번호는 이전 비밀번호와 달라야 합니다.")
            raise serializers.ValidationError(
                "새 비밀번호는 이전 비밀번호와 달라야 합니다.")

        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
