//DOMContentLoaded: dom이 로딩이 되면 등록된 함수를 수행
//load : css, img, js등의 리소스등이 로딩이 된후 등록된 함수를 수행

document.addEventListener('DOMContentLoaded', function () {
  banner.rollInit(2000);// 베너 롤링

  //앞뒤 클릭 이벤트 리스너
  document.querySelectorAll(".btnmove").forEach(function (item) {
    item.addEventListener('click', function (e) {
      clearInterval(banner.rollId);
      console.log("item:", e.target);  //<i class="fas fa-chevron-left"> <i class="fas fa-chevron-right">
      if (e.target.parentElement.parentElement.classList.contains("prev")) {
        banner.rollPrev();
      } else {
        banner.rollNext();
      }
      banner.rollId = setInterval(banner.rollPrev, banner.interval); //롤링 인터벌 호출
    });
  });
});
 


let banner = {
  rollId: null,
  interval:2000,
  
  //롤링 배너 초기화
  rollInit: function (newinterval) {
    if (parseInt(newinterval) > 0) {
      this.interval = newinterval;
    }

    //현재 배너
    let firstitem = document.querySelector(".rollimgs li");
    if (firstitem) {
      firstitem.classList.add('currentroll');
    }

    //다음 배너
    let seconditem = document.querySelectorAll(".rollimgs li")[1];
    if (seconditem) {
      seconditem.classList.add("nextroll");
    }

    //이전 배너
    document.querySelector(".rollimgs li:last-child").classList.add("prevroll");
    this.rollId = setInterval(this.rollPrev, this.interval); //롤링 인터벌 호출
  },

  //이전 배너 롤링
  rollPrev: function () {
    document.querySelector(".rollimgs").classList.add('reverse');
    if (document.querySelector('.nextroll')) {
      document.querySelector(".nextroll").classList.remove("nextroll");      
    }

    if (document.querySelector('.currentroll')) {
      document.querySelector(".currentroll").classList.add("nextroll");
      document.querySelector(".currentroll").classList.remove("currentroll");
    }

    if (document.querySelector(".prevroll")) {
      document.querySelector(".prevroll").classList.add("currentroll");
      document.querySelector(".prevroll").classList.remove("prevroll");
    }
  
    if (document.querySelector(".currentroll").previousElementSibling) {
      document.querySelector(".currentroll").previousElementSibling.classList.add("prevroll");
    } else {
      document.querySelector(".rollimgs li:last-child").classList.add("prevroll");
    }
  },
   //다음 배너 롤링
   rollNext: function () {
    document.querySelector(".rollimgs").classList.remove("reverse");
    if (document.querySelector(".prevroll")) {
      document.querySelector(".prevroll").classList.remove("prevroll");
    }
    if (document.querySelector(".currentroll")) {
      document.querySelector(".currentroll").classList.add("prevroll");
      document.querySelector(".currentroll").classList.remove("currentroll");
    }
    if (document.querySelector(".nextroll")) {
      document.querySelector(".nextroll").classList.add("currentroll");
      document.querySelector(".nextroll").classList.remove("nextroll");
    }
    if (document.querySelector(".currentroll").nextElementSibling) {
      document
        .querySelector(".currentroll")
        .nextElementSibling.classList.add("nextroll");
    } else {
      document.querySelector(".rollimgs li").classList.add("nextroll");
    }
  }
}