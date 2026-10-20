function display() {
    for (let i = 0; i <= 5; i++){
        console.log(`i=${i}`);
    }
}

console.log("start=============");
//setTimeout() : 일정 시간이 지난 후에 함수를 실행하는 방법 - 한번만 수행
//setInterval() : 일정 시간 간격을 두고 함수를 실행하는 방법 - 반복 수행

//1000이 1초
//setTimeout(실행함수, 시간);
//setTimeout(display, 5000);

setInterval(display, 5000);

console.log("end===============");