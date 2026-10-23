"""상품 등록을 위한 ModelForm: Model의 필드 정의를 재사용한다."""
from django import forms
from .models import Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # 관리자가 직접 입력할 필드만 폼에 노출한다.
        fields = ["category", "name", "price", "stock", "description"]
