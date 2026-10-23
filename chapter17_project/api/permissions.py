"""조회는 공개하고 변경은 관리자(staff)에게만 허용한다."""
from rest_framework.permissions import BasePermission, SAFE_METHODS

class ReadOnlyOrStaff(BasePermission):
    # GET/HEAD/OPTIONS는 로그인 없이 허용한다.
    # POST/PUT/PATCH/DELETE는 staff 사용자만 수행한다.
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
