var nb = document.getElementById("nb_elem").innerHTML 
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
function get_db_id(id){
    var ident = "tab_db_id_" + id.id.slice(-1)
    var db_id = document.getElementById(ident).innerHTML
    return db_id
}
