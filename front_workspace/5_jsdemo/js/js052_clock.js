function leftPad(num) {
  if (num < 10)
    return `0${num}`;
  else
    return `${num}`;
}

function setText(selector, text) {
  let targetElement = document.querySelector(selector);
  targetElement.innerText = leftPad(text);
}

function watchTime() {
  let present = new Date();
  const dayList = ["일", "월", "화", "수", "목", "금", "토"];
  
  setText('#hours', present.getHours());
  setText('#minute', present.getMinutes());
  setText('#seconds', present.getSeconds());

  setText('#year', present.getFullYear());
  setText('#month', present.getMonth() + 1);
  setText('#date', present.getDate());

  const day = present.getDay();
  setText('#day', dayList[day]);
}

watchTime();

let clockInterval = setInterval(watchTime, 1000);

let btn = document.querySelector('button');

btn.onclick = () => {
  if (btn.innerText == '시간종료') {
    clearInterval(clockInterval);
    btn.innerText = '시간시작';
  } else {
    clockInterval = setInterval(watchTime, 1000);
    btn.innerText = '시간종료';
  }
}

/*
 setTimeout(실행함수, 시간) :  일정한 시간이 지난후 한번만 실행함 - 한번수행
 setInterval(실행함수, 시간) : 일정 시간 간격을 두고 반복 실행함- 반복수행

 clearTimeout, clearInterval : 해제
*/

