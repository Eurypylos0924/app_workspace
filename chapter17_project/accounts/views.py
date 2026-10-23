"""회원가입 요청을 처리하는 View이다."""
from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import SignUpForm

def signup(request):
    # POST 요청은 사용자가 제출한 폼 데이터이다.
    if request.method == "POST":
        form = SignUpForm(request.POST)
        # 폼 유효성 검사: 비밀번호 정책, 중복 사용자명 등을 확인한다.
        if form.is_valid():
            user = form.save()
            # 가입 직후 로그인 상태를 설정한다.
            login(request, user)
            return redirect("product_list")
    else:
        # GET 요청은 비어 있는 회원가입 화면을 제공한다.
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})
