let myNode = document.querySelector('#p2');

//parentNode 부모
let ptNode = myNode.parentNode;
console.log(ptNode); // <div id="wrap">…</div>
console.log(`${ptNode}`);  //[object HTMLDivElement]
//////////////////////////////////////
//previousSibling
let prevNode = myNode.previousSibling;
console.log(`prevNode=${prevNode}`);  //prevNode=[object Text]

prevNode = prevNode.previousSibling;
console.log(prevNode); //<p id="p1">content1</p>
console.log(`prevNode=${prevNode}`); //prevNode=[object HTMLParagraphElement]

//////////////////////////////////////////
//nextSibling
let nextNode = myNode.nextSibling;
console.log(`nextNode=${nextNode}`); //nextNode=[object Text]

nextNode = nextNode.nextSibling;
console.log(nextNode); //<p id="p3">content3</p>
console.log(`nextNode=${nextNode}`); //nextNode=[object HTMLParagraphElement]

/////////////////////////////////////
//previousElementSibling
let prevEleNode = myNode.previousElementSibling;
//prevEleNode:[object HTMLParagraphElement],  content1
console.log(`prevEleNode:${prevEleNode},  ${prevEleNode.innerText}`); 

/////////////////////////////
//nextElementSibling
let nextEleNode = myNode.nextElementSibling;
//nextEleNode=[object HTMLParagraphElement],  content3 
console.log(`nextEleNode=${nextEleNode},  ${nextEleNode.innerText} `);

////////////////////////////
//childNodes
let divNode = document.querySelector('#wrap');
//divNode:[object HTMLDivElement]
console.log(`divNode:${divNode}`);

let divChildesNode = divNode.childNodes;
//divChildesNode=[object NodeList]
console.log(`divChildesNode=${divChildesNode}`);
//NodeList(9) [text, p#p1, text, p#p2, text, p#p3, text, p#p4, text]
console.log(divChildesNode);

//////////////////////////////////////
//children
let divChildren = divNode.children;
//divChildren=[object HTMLCollection]
console.log(`divChildren=${divChildren}`);
//HTMLCollection(4) [p#p1, p#p2, p#p3, p#p4, p1: p#p1, p2: p#p2, p3: p#p3, p4: p#p4]
console.log(divChildren);
console.log(divChildren[0]); //<p id="p1">content1</p>
console.log(divChildren.item(0)); //<p id="p1">content1</p>
console.log(divChildren.namedItem('p1')); //<p id="p1">content1</p>

//////////////////////////////////
//firstChild, firstElementChild
let pNode = document.querySelector('#p4');
let aNode = pNode.firstChild;
console.log(aNode); //#text

let imgNode = pNode.firstElementChild;
//<img src="images/gosu.jpg" alt="영화배우 고수"></img>
console.log(imgNode); 

///////////////////////////////////////
// 객체.getAttribute("속성명"), 객체.setAttribute("속성명", "속성값")
// 객체.속성명,                 객체.속성명="속성값"

let imgAttrNode = imgNode.getAttribute("src");
//images/gosu.jpg
console.log(imgAttrNode);

imgAttrNode = imgNode.src;
//http://127.0.0.1:50342/jsdemo/images/gosu.jpg
console.log(imgAttrNode); 

imgNode.setAttribute('title', '스타배우');  //<img  title="스타배우" />
imgNode.width = 300; 
imgNode.height = 300;




