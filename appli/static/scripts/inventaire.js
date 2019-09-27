var nb = document.getElementById("nb_elem").innerHTML 
function recup_id(id){
    console.log("poubelle no:" + id.id)
    var ident = "tab_db_" + id.id.slice(-1) + "_id"
    var db_id = document.getElementById(ident).innerHTML
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
