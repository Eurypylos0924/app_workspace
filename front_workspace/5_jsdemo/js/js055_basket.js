let basket = {
    totalCount:0,
    totalPrice: 0,
    //체크한 장바구니 상품 비우기
    delCheckedItem: function () {
        document.querySelectorAll("input[name=buy]:checked").forEach(function (item) { 
            item.parentElement.parentElement.parentElement.remove();            
        });

        //AJAX 서버 업데이트 전송

        //전송 처리 결과가 성공이면
        this.reCalc();
        this.updateUI();
    },
    //장바구니 전체 비우기
    delAllItem: function () {
        document.querySelectorAll(".row.data").forEach(function (item) {
            item.remove();
        });
        //AJAX 서버 업데이트 전송

        //전송 처리 결과가 성공이면
        this.totalCount = 0;
        this.totalPrice = 0;
        this.reCalc();
        this.updateUI();
    },

    //재계산
    reCalc: function () {
        this.totalCount = 0;
        this.totalPrice = 0;
        document.querySelectorAll(".p_num").forEach(function (item) {
            let count = parseInt(item.getAttribute("value"));
            this.totalCount += count;
            let price = item.parentElement.parentElement.previousElementSibling.firstElementChild.getAttribute("value"); 
            price = parseInt(price);
            this.totalPrice += count * price;
        }, this); //forEach 2번째 파라미터로 객체를 넘겨서 this가 객체리터널을 가리키도록 함
    },

    //화면업데이트
    updateUI: function () {
        document.querySelector('#sum_p_num').textContent =
            '상품갯수: ' + this.totalCount.formatNumber() + '개';
        document.querySelector("#sum_p_price").textContent =
            '합계금액: ' + this.totalPrice.formatNumber() + '원';
    },

    //개별 수량 변경
    changePNum: function (pos) {
        let item = document.querySelector('input[name=p_num' + pos + ']');
        let p_num = parseInt(item.getAttribute('value'));        
        let newval = event.target.classList.contains('up') ? p_num + 1 : event.target.classList.contains('down') ? p_num - 1 : event.target.value;
        //console.log(newval); 

        //상품갯수가 1보다 작거나 99보다 크면 안됨
        if (parseInt(newval) < 1 || parseInt(newval) > 99) { return false; }
        console.log(newval);
        console.log("value:" + item.value);
        item.setAttribute("value", newval);         
        
        let price = item.parentElement.parentElement.previousElementSibling.firstElementChild.getAttribute("value"); 
        item.parentElement.parentElement.nextElementSibling.textContent = (newval * price).formatNumber() + "원";
        //Ajax 업데이터 전송

        //전송 처리 결과가 성공이면
        this.reCalc();
        this.updateUI();
    },

    //삭제버튼이 있는 행 상품삭제
    delItem: function () {
        event.target.parentElement.parentElement.parentElement.remove();
        //AJAX 서버 업데이트 전송

         //전송 처리 결과가 성공이면
         this.reCalc();
         this.updateUI();
    }
    
}

//숫자 3자리 콤마찍기
Number.prototype.formatNumber = function () {
    //여기에서 this는 formatNumber()메서드를 호출하는 Number객체 자체를 의미한다.(즉 숫자이다.)
    if (this == 0) return 0;
    console.log("this:" + this);

    //3자리마다 콤마를 찍기 위한 정규식
    //(^[+-]?\d+) : 문자열 시작부터 + 또는 - 가  없거나 1개 있을 수 있고,  숫자가 1개 이상 나오는 그룹1
    //(\d{3}) : 숫자 3자리 그룹2
    let regex = /(^[+-]?\d+)(\d{3})/;
    // 숫자를 문자열로 변경(문자열이 되여야 정규식을 적용할 수 있기 때문에)
    let nstr = (this + '');
    console.log(regex.test(nstr));
    //정규식에 매칭될때마다 (즉, 3자리마다 콤마를 찍어야 할 때마다)
    while (regex.test(nstr)) {
        //첫 번째 그룹 + ',' + 두번째 그룹으로 문자열을 바꿔서 3자리마다 콤마를 추가한다.
        nstr = nstr.replace(regex, '$1' + ',' + '$2');
    }
    //최종 콤마가 찍힌 문자열을 반환한다.
    return nstr;        
}

