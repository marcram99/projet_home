$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip()
  })

function get_db_id(id){
    var ident = "tab_db_id_" + id.id.slice(-1)
    var db_id = document.getElementById(ident).innerHTML
    return db_id
}
function efface(id){
    var db_id = get_db_id(id)
    $.post(window.location.href,
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
function modifie(id){
    db_id = get_db_id(id)
    $("#new_article").modal("show")
    console.log(db_id)
    new_art_nom.value = document.getElementById("tab_db_art_" + id.id.slice(-1)).innerHTML
    new_art_quant.value = document.getElementById("tab_db_qua_" + id.id.slice(-1)).innerHTML
    new_art_date.value = document.getElementById("tab_db_per_" + id.id.slice(-1)).innerHTML
    art_valide.innerHTML = 'Modifier'
}
function copie(id){
    db_id = get_db_id(id)
    new_art_nom.value = document.getElementById("tab_db_art_" + id.id.slice(-1)).innerHTML
    new_art_quant.value = document.getElementById("tab_db_qua_" + id.id.slice(-1)).innerHTML
    new_art_date.value = document.getElementById("tab_db_per_" + id.id.slice(-1)).innerHTML
    var article = new_art_nom.value
    var quant = new_art_quant.value
    var perime = new_art_date.value
    $.post(window.location.href,
        {'command': 'add',
        'article': article,
        'quantite': quant,
        'date_fin': perime,
        'db_id': db_id
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
function ajoute(id){
    db_id = false
    $("#new_article").modal("show")
    art_valide.innerHTML = 'Ajouter'
}
art_valide.onclick = function(){
    event.preventDefault()
    var article = new_art_nom.value
    var quant = new_art_quant.value
    var perime = new_art_date.value
    if(art_valide.innerHTML == 'Modifier'){var command = 'mod' }
    if(art_valide.innerHTML == 'Ajouter'){var command = 'add' }
    $.post(window.location.href,
        {'command': command,
        'article': article,
        'quantite': quant,
        'date_fin': perime,
        'db_id': db_id
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
function pdf(id){
    event.preventDefault()
    $.post(window.location.href,
        {'command': 'pdf',
        'database': 'cave'
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