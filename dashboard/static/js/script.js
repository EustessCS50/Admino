
var user = '{{ request.user }}'


//var menuList = document.getElementById("menuList");
//
//menuList.style.maxHeight = "0px";
//
//function togglemenu(){
//    if(menuList.style.maxHeight == "0px")
//    {
//        menuList.style.maxHeight = "130px";
//    }
//    else
//    {
//        menuList.style.maxHeight = "0px";
//    }
//}
//
//var side-menuList = document.getElementById("side-menuList");
//
//side-menuList.style.maxHeight = "0px";

//function sidetogglemenu(){
//    if(side-menuList.style.maxHeight == "0px")
//    {
//        side-menuList.style.maxHeight = "fit-content";
//    }
//    else
//    {
//        side-menuList.style.maxHeight = "0px";
//    }
//}
var article-form = document.getElementById('article-form')
if (user != 'AnonymousUser'){
    article-form.innerHTML = ""
}

function addArticle(){
    alert("Ok")
    if (article-form.innerHTML == ""){
        article-form.classList.remove("hidden")
    }
}
