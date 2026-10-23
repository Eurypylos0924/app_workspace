"""세션 기반 장바구니 비즈니스 로직이다. 가격은 DB에서만 읽고 세션에는 수량만 저장한다."""
from decimal import Decimal
from django.core.exceptions import ValidationError
from .models import Product

CART_SESSION_KEY = "cart"
MAX_QUANTITY = 99

def get_cart(request):
    """현재 요청의 장바구니 딕셔너리를 가져온다."""
    # 세션 값이 없거나 훼손된 경우 빈 장바구니로 안전하게 초기화한다.
    cart = request.session.get(CART_SESSION_KEY, {})
    return cart if isinstance(cart, dict) else {}

def parse_quantity(raw):
    """POST로 받은 수량을 1~99 사이의 정수로 검증한다."""
    # bool은 int의 하위 타입이므로 문자열로 변환해 숫자 형식을 검사한다.
    text = str(raw).strip()
    if not text.isdecimal():
        raise ValidationError("수량은 1 이상의 정수여야 한다.")
    quantity = int(text)
    if not 1 <= quantity <= MAX_QUANTITY:
        raise ValidationError("수량은 1~99 사이여야 한다.")
    return quantity

def set_quantity(request, product, quantity):
    """상품의 장바구니 수량을 지정하고 세션을 갱신한다."""
    # 재고를 초과하는 수량을 장바구니에 저장하지 않는다.
    if quantity > product.stock:
        raise ValidationError("상품 재고를 초과할 수 없다.")
    cart = get_cart(request).copy()
    cart[str(product.pk)] = quantity
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

def remove_item(request, product_id):
    """지정한 상품만 장바구니에서 제거한다."""
    cart = get_cart(request).copy()
    cart.pop(str(product_id), None)
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

def build_cart_context(request):
    """현재 DB 가격으로 품목별 소계와 전체 합계를 계산한다."""
    cart = get_cart(request)
    # DB 조회에 사용할 키를 숫자로 제한하여 잘못된 세션 값에 대응한다.
    ids = [int(key) for key in cart if str(key).isdecimal()]
    products = Product.objects.filter(pk__in=ids).select_related("category")
    items = []
    total = Decimal("0.00")
    for product in products:
        # 저장된 수량이 손상된 경우 해당 품목은 화면에서 제외한다.
        try:
            quantity = parse_quantity(cart[str(product.pk)])
        except (ValidationError, KeyError):
            continue
        subtotal = product.price * quantity
        total += subtotal
        items.append({"product": product, "quantity": quantity, "subtotal": subtotal})
    return {"items": items, "total": total, "item_count": sum(i["quantity"] for i in items)}
