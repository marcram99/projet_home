card_maison.onclick = function(){
    event.preventDefault()
    console.log('click on maison')
    menu_maison.className = 'card col-3 m-2'
    menu_jardin.className = 'card col-3 m-2 d-none'
    menu_appareil.className = 'card col-3 m-2 d-none'
}
card_jardin.onclick = function(){
    event.preventDefault()
    console.log('click on maison')
    menu_maison.className = 'card col-3 m-2 d-none'
    menu_jardin.className = 'card col-3 m-2 '
    menu_appareil.className = 'card col-3 m-2 d-none'
}
card_appareil.onclick = function(){
    event.preventDefault()
    console.log('click on maison')
    menu_maison.className = 'card col-3 m-2 d-none'
    menu_jardin.className = 'card col-3 m-2 d-none'
    menu_appareil.className = 'card col-3 m-2'
}