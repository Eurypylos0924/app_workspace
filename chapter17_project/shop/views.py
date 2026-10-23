"""HTTP 요청을 처리하고 ORM 조회 결과를 Template에 전달한다."""
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from decimal import InvalidOperation
from django.views.decorators.http import require_POST
from .forms import ProductForm
from .models import Product, Category

def product_list(request):
    """상품 검색·카테고리 필터·가격 필터·정렬·페이지네이션을 처리한다."""
    # 상품과 카테고리를 한 번의 JOIN 쿼리로 조회하여 N+1 문제를 줄인다.
    products = Product.objects.select_related("category").all()
    # GET 파라미터를 읽고, 앞뒤 공백을 제거하여 검색 조건을 정규화한다.
    keyword = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    sort = request.GET.get("sort", "newest")
    # 상품명 또는 설명에 검색어가 포함된 상품만 남긴다.
    if keyword:
        products = products.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
    # 잘못된 카테고리 ID는 무시하지 않고 빈 결과를 반환한다.
    if category_id:
        products = products.filter(category_id=category_id) if category_id.isdecimal() else products.none()
    # 가격 입력은 Decimal로 검증한다. 유효하지 않은 값은 필터에서 제외한다.
    for raw, lookup in ((min_price, "price__gte"), (max_price, "price__lte")):
        if raw:
            try:
                value = Decimal(raw)
                if value.is_finite() and value >= 0:
                    products = products.filter(**{lookup: value})
            except (InvalidOperation, ValueError):
                pass
    # 클라이언트가 전달한 정렬 문자열을 그대로 order_by에 사용하지 않는다.
    allowed_sorts = {"newest": "-created_at", "price_asc": "price", "price_desc": "-price", "name": "name"}
    sort = sort if sort in allowed_sorts else "newest"
    products = products.order_by(allowed_sorts[sort], "id")
    # 페이지당 6개씩 나누고 잘못된 페이지 번호는 첫/마지막 페이지로 보정한다.
    page_obj = Paginator(products, 6).get_page(request.GET.get("page", 1))
    print('page_obj:', page_obj)
    # 페이지 이동 시 검색·필터·정렬 조건을 보존하도록 `page를 제외한 쿼리 문자열을 만든다.
    params = request.GET.copy()
    params.pop("page", None)
    return render(request, "shop/product_list.html", {
        "page_obj": page_obj,
        "products": page_obj.object_list,
        "categories": Category.objects.order_by("name"),
        "keyword": keyword, "selected_category": category_id,
        "min_price": min_price, "max_price": max_price,
        "sort": sort, "query_string": params.urlencode(),
    })

def product_detail(request, pk):
    # 존재하지 않는 상품 ID를 요청하면 HTTP 404를 반환한다.
    product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
    return render(request, "shop/product_detail.html", {"product": product})

@login_required
def product_create(request):
    # 등록 기능은 로그인한 사용자만 접근할 수 있다(실무에서는 별도 권한 검사 필요).
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect("product_detail", pk=product.pk)
    else:
        form = ProductForm()
    return render(request, "shop/product_form.html", {"form": form})

# 장바구니 로직은 별도 모듈에서 재사용한다.
from django.contrib import messages
from django.core.exceptions import ValidationError
from .cart import build_cart_context, get_cart, parse_quantity, remove_item, set_quantity

@require_POST
def cart_add(request, pk):
    # 요청한 상품이 존재하는지 확인한다.
    product = get_object_or_404(Product, pk=pk)
    # 화면에서 전송한 수량을 검사하고 기존 수량과 합산한다.
    try:
        added = parse_quantity(request.POST.get("quantity", "1")) 
        current = int(get_cart(request).get(str(pk), 0))
        set_quantity(request, product, current + added)
        messages.success(request, "장바구니에 상품을 담았다.")
    except (ValidationError, ValueError, TypeError) as exc:
        messages.error(request, str(exc))
    return redirect("cart_detail")

@require_POST
def cart_update(request, pk):
    # 수량 변경은 CSRF 보호가 적용되는 POST 요청에서만 처리한다.
    product = get_object_or_404(Product, pk=pk)
    try:
        quantity = parse_quantity(request.POST.get("quantity", ""))
        set_quantity(request, product, quantity)
        messages.success(request, "상품 수량을 변경하였다.")
    except ValidationError as exc:
        messages.error(request, str(exc))
    return redirect("cart_detail")

@require_POST
def cart_remove(request, pk):
    # 존재하지 않는 상품 번호도 안전하게 제거 처리한다.
    remove_item(request, pk)
    messages.success(request, "장바구니에서 상품을 삭제하였다.")
    return redirect("cart_detail")

@require_POST
def cart_clear(request):
    # 세션의 다른 로그인 정보는 유지하고 장바구니 키만 삭제한다.
    request.session.pop("cart", None)
    request.session.modified = True
    messages.success(request, "장바구니를 비웠다.")
    return redirect("cart_detail")

def cart_detail(request):
    # 가격은 세션이 아니라 MySQL Product 테이블을 기준으로 계산한다.
    return render(request, "shop/cart.html", build_cart_context(request))
