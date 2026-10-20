//최대값
console.log(Math.max(1, 2, 3, 4, 5)); //5

//최소값
console.log(Math.min(1, 2, 3, 4, 5)); //1

//절대값
console.log(Math.abs(-10)); //10

//반올림 - 자릿수 지정할 수 없음
console.log(Math.round(25.3533)); //25

//올림
console.log(Math.ceil(23.344)); //24

//버림
console.log(Math.floor(23.56)); //23

//난수 0.0이상 ~ 1.0 미만
console.log(Math.random());

//반올림
console.log((25.523).toFixed(2)); //25.52
console.log((25.526).toFixed(2)); //25.53

let date = new Date();
// Mon Feb 26 2024 12:54:28 GMT+0900 (한국 표준시)
console.log(date);

console.log(date.getFullYear()); //년도
console.log(date.getMonth() + 1); //월
console.log(date.getDate()); //일
console.log(date.getDay()); //요일  0일요일 6토요일
