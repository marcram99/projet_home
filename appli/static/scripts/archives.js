var tab_p = document.getElementById("tab_photo");
var tab_a = document.getElementById("tab_admin");

tab_a.onclick = function(){
    tab_a.className = "nav-link active";
    tab_p.className = "nav-link";  
}
tab_p.onclick = function(){
    tab_p.className = "nav-link active";
    tab_a.className = "nav-link";  
}

