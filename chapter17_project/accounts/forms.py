"""회원가입 폼: Django 기본 User 모델과 비밀번호 검증을 재사용한다."""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class SignUpForm(UserCreationForm):
    # UserCreationForm이 비밀번호 일치 여부와 정책을 검증한다.
    class Meta(UserCreationForm.Meta):
        model = User
        # 사용자명과 이메일을 입력받고 비밀번호 필드는 부모 폼에서 제공한다.
        fields = ("username", "email")
