var nb = document.getElementById("nb_elem").innerHTML

function get_db_id(id){
    var ident = "tab_db_id_" + id.id.slice(-1)
    var db_id = document.getElementById(ident).innerHTML
    return db_id
}
function efface(id){
    var db_id = get_db_id(id)
    $.post("/inventaire2/",
        {'command':'del',
         'ligne':id.id,
         'db_id':db_id,
        },    
        function(results){
            var res = JSON.parse(results)
            if(res.message == 'ok'){
                document.location.reload(true)
            } 
        }
    )
}
art_valide.onclick = function(){
    event.preventDefault()
    var article = new_art_nom.value
    var quant = new_art_quant.value
    var perime = new_art_date.value
    console.log('formulaire rempli:'+ article +':'+ quant +':'+ perime)
    $.post("/inventaire2/",
        {'command':'add',
         'article':article,
         'quantité':quant,
         'date_fin':perime
        },    
        function(results){
            document.location.reload(true)
            var res = JSON.parse(results)
            if(res.message == 'ok'){
                console.log('add ok')
            } 
        }
    )
}