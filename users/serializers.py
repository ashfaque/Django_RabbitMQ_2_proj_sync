from rest_framework import serializers
from .models import UserDetail
# from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.exceptions import APIException
from django.conf import settings
import datetime

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ListCreateUserSerializer(serializers.ModelSerializer):
    registered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # password = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = UserDetail
        fields = (
            'username'
            , 'first_name'
            , 'last_name'
            , 'middle_name'
            , 'email'
            , 'user_type'
            # , 'user_code'
            , 'gender'
            , 'phone_no'
            , 'profile_img'
            , 'class_teacher'
            , 'session'
            , 'semester'
            , 'stream'
            , 'course'
            , 'dob'
            , 'nationality'
            , 'address'
            , 'is_deleted'
            , 'registered_on'
            , 'registered_by'
            , 'updated_at'
            , 'updated_by'
            , 'deleted_at'
            , 'deleted_by'
            , 'is_active'
            , 'is_superuser'
        )

    def create(self, validated_data):
        try:
            with transaction.atomic():
                login_user_id = self.context['request'].user.id
                # username = validated_data['username']
                username = validated_data.get('username', None)
                if not username:
                    raise APIException('Username is required')
                user_detail_count = UserDetail.objects.filter(username=username).count()
                if user_detail_count:
                    raise APIException('Username already exists')
            
                # password = User.objects.make_random_password()
                # password = UserDetail.objects.make_random_password()
                password = settings.NEW_USER_DEFAULT_PASSWORD

                validated_data['password_to_know'] = password

                user_create = UserDetail.objects.create(**validated_data)    # ! NB: Here we are creating a UserDetail instance.
                user_create.set_password(password)                           # ! NB: Here we are updating a UserDetail instance. And this is the reason the pre_save and post_save signals are being called twice, once for creation and another for updation.
                user_create.save()

            return validated_data

        except Exception as ex:
            raise ex


class LoginUserSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = dict(attrs)['username'] if 'username' in dict(attrs) else None
        is_user_exist = UserDetail.objects.filter(username=user).first()
        if is_user_exist:
            if is_user_exist.is_active:
                try:
                    data = super().validate(attrs)    # Generate Token
                    data['user_details'] = UserDetail.objects.filter(id=self.user.id).values().first()
                    data['request_status'] = 1
                    data['msg'] = 'Success'
                    return data
                except Exception as get_exception:                  
                    if get_exception == 'No active account found with the given credentials':    ## This exceltion is comming from JWT default_error_messages
                        raise APIException({'request_status':0, 'msg':'Please check the password!!'})  
                    else:
                        raise APIException({'request_status':0, 'msg':'Invalid credentials!!'})
            else:
                raise APIException({'request_status':0, 'msg':'User is Deactivated!!'})
        else:
            raise APIException({'request_status':0, 'msg':'User does not exist!!'})


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
