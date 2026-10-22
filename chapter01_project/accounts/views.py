# HTTP 응답을 생성하는 클래스를 가져온다.
from django.http import HttpResponse

# 회원 관리 앱의 기본 화면을 반환한다.
def home(request):
    return HttpResponse("<h1>회원 관리 앱 실행 성공</h1>")