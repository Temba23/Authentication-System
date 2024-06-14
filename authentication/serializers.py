from rest_framework import serializers
from .models import CustomUser, SecurityQuestion
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.core.mail import send_mail


User = CustomUser
  
class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
            'email', 'first_name', 'last_name')
        extra_kwargs = {
        'first_name': {'required': True},
        'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def send_mail(self):
       subject = 'Welcome Onboard'
       message = f'Hi {self.instance.username}, You have registered in my localhost.'
       email_from = settings.EMAIL_HOST_USER
       recipient_list = [self.instance.email,]
       send_mail( subject, message, email_from, recipient_list)
    
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ["id", "first_name", "last_name", "username"]


class SecurityQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityQuestion
        fields = "__all__"

    def validate(self, data):
        user = self.context['request'].user
        question = data.get('questions')
        method = self.context['request'].method

        if method != "PUT":
            if SecurityQuestion.objects.filter(user=user, questions=question).exists():
                raise serializers.ValidationError("You have already answered this question.")
                    
        return data
    
def update(self, instance, validated_data):
    instance.questions = validated_data.get('questions', instance.questions)
    instance.answer = validated_data.get('answer', instance.answer)
    instance.save()
    return instance