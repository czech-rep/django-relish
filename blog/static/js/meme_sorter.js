// $(document).ready(function() { // to bylo by dla całego portalu

function meme_index(){
    // document.addEventListener("load", ()=>{

        var deletable = document.getElementsByClassName('deletion');
        console.log(deletions.length);
        for(var i = 0; i < deletions.length; i++) {
            deletable[i].addEventListener("click", alert('alert'))
            //delete_image(this.text));
        }
    // })
};

function delete_image(content){
    alert(content);
}
function signalize(){
    alert('hello');
    console.log('elo');
}