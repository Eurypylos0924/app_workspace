let hNode = document.getElementById("selector");
console.log(hNode);  //<h1 ird="selector" class="choice">선택자</h1>
console.log(typeof hNode);  //object

let hClass = document.getElementsByClassName("choice");
console.log(hClass);  //HTMLCollection [h1#selector.choice, selector: h1#selector.choice]
console.log(typeof hClass);  //object
console.log(hClass.length); //1

let pNode = document.getElementsByTagName("p");
console.log(pNode); //HTMLCollection(4) [p, p, p, p]
console.log(pNode.length); //4

//innerText, textContent,innerHTML
console.log(pNode[0]);    //p
console.log(pNode.item(0)); //p
console.log(pNode[0].innerText);  //content1
console.log(pNode[1].innerText);  //content2
console.log(pNode[0].textContent) //content1
console.log(pNode[1].textContent) //content2
pNode[0].style.backgroundColor = "blue";

console.log('=========================')
//부모위치에서 자손요소의 컨텐츠를 가져올때 차이보기 (innerText, textContent)
let divNode = document.getElementsByTagName('div')[0];
console.log(divNode);
console.log(divNode.innerText); // content1  content3
console.log(divNode.textContent); // content1 content2 content3 content4
console.log(divNode.innerHTML); //
//  <p style="background-color: blue;">content1</p>
//   <p style="display: none">content2</p>
//   <p>content3</p>
//   <p style="display: none">content4</p>
console.log('=========================')
//////////////////////////////////////
let hId = document.querySelector("#selector");   //Element
console.log(hId); //<h1 id="selector" class="choice">선택자</h1>

let hData = document.querySelector(".choice");  //Element
console.log(hData); //<h1 id="selector" class="choice">선택자</h1>

let pList = document.querySelector("p");   //HTMLParagraphElement
console.log(pList); //<p style="background-color: blue;">content1</p>

let pList2 = document.querySelectorAll("p");
console.log(pList2);  //NodeList(4) [p, p, p, p]


function process() {
    //  alert('click');
    let fname = document.frm.fname;
    console.log(fname, typeof fname);
    console.log(fname.value); 
    console.log(fname.defaultValue);
    return false;
}


