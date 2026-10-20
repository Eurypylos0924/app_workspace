//Destructuring (구조 분해 할당)
// : Destructuring(디스트럭쳐링)은 structuring(구조화)된 배열 또는 객체를 Destructuring(비구조화)
//   하여 개별적으로 변수에 할당하는 개념이다.

//1. 배열 Destructuring
let level = [5, 10];
let a, b;
a = level[0];
b = level[1];
console.log(`a=${a}, b=${b}`);  //a=5, b=10

let c, d;
[c, d] = [5, 10];
console.log(`c=${c}, d=${d}`); //c=5, d=10

let k, p, next;
[k, p, next] = [1, 2, 3, 4, 5, 6, 7, 8];
console.log(`k=${k}`);  //k=1
console.log(`p=${p}`);  //p=2
console.log(`next=${next}`);  //next=3

[k, p, ...next] = [1, 2, 3, 4, 5, 6, 7, 8];
console.log(`k=${k}`);  //k=1
console.log(`p=${p}`); //p=2
console.log(`next=${next}`);  //next=3,4,5,6,7,8
console.log(next); //[3, 4, 5, 6, 7, 8]

[k, _, p, _, ...next] = [1, 2, 3, 4, 5, 6, 7, 8];
console.log(`k=${k}`);  //k=1
console.log(`p=${p}`); //p=3
console.log(`next=${next}`); //next=5,6,7,8

let u, t, w;
[u, t, w] = [1, 2];
console.log(`u=${u}, t=${t}, w=${w}`);  //u=1, t=2, w=undefined

[u, t, w=3] = [1, 2];
console.log(`u=${u}, t=${t}, w=${w}`); //u=1, t=2, w=3

[u, t = 4, w = 5] = [1, 2];
console.log(`u=${u}, t=${t}, w=${w}`); //u=1, t=2, w=5

//2. 객체 Destructuring
const customer = { fullname: '고수', job: '연기자' };
let fullname = customer.fullname;
let job = customer.job;
console.log(`fullname=${fullname}, job=${job}`); //fullname=고수, job=연기자

let { fullname: fn, job: jb } = customer;
console.log(`fullname:${fn}, job:${jb}`); //fullname:고수, job:연기자

let { job: jb2, fullname: fn2 } = customer;
console.log(`job:${jb2}, fullname:${fn2}`); //job:연기자, fullname:고수

let { fullname: fn3, job: jb3, loc = '서울' } = customer;
console.log(`fullname:${fn3}, job:${jb3}, loc=${loc}`); //fullname:고수, job:연기자, loc=서울

// let { s, r } = { s: 1, r: 2 };
// console.log(s, r);  //1 2

let { r, s } = { s: 1, r: 2 };
console.log(r, s);  //2 1

//////////////////////////////////////////////////////////////////
//completed의 값이 true인 데이터만 검색하라.
let habits = [
    { id: 1, content: "수영", completed: false },
    { id: 2, content: "걷기", completed: true },
    { id: 3, content: "명상", completed: true },
    { id: 4, content: "독서", completed: false },
];

let listHabit = [];
for (let i = 0; i < habits.length; i++){
    if (habits[i].completed) {
        listHabit.push(habits[i]);
    }
}
console.log(listHabit); //[{id: 2, content: '걷기', completed: true},{ id: 3, content: '명상', completed: true } ]
/////////////////////////

let completedHabit = habits.filter((element) => { return element.completed });
console.log(completedHabit);//[{id: 2, content: '걷기', completed: true},{ id: 3, content: '명상', completed: true } ]

let completedHabit2 = habits.filter(element =>  element.completed);
console.log(completedHabit2);//[{id: 2, content: '걷기', completed: true},{ id: 3, content: '명상', completed: true } ]

/////////////////////////////////////////////////////////////
//member변수에서 데이터를 추출하여 '고수 고객님은 서울에 거주합니다.' 라고 출력하세요.

let member = {
    hname: "고수",
    address: {
      zipCode: "526-143",
      city: "서울",
    },
};
  
// let { hname, address } = member;
// console.log(`${hname} 고객님은 ${address.city}에 거주합니다.`);  //고수 고객님은 서울에 거주합니다.

let { hname, address : {zipCode, city} } = member;
console.log(`${hname} 고객님은 ${city}에 거주합니다.`);  //고수 고객님은 서울에 거주합니다.


  
