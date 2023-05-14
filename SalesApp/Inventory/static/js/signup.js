function hasnumber(string){
    return /[\d]/.test(string);
}
let ferror = document.getElementById('ferror');
let firstn = document.getElementById('firstn');

let lerror = document.getElementById('lerror');
let lastn = document.getElementById('lastn');

firstn.addEventListener('keyup',()=>{
    if (hasnumber(firstn.value.trim())){
        ferror.innerHTML = "Numbers not allowed";
    }
    else{
        ferror.innerHTML = "";
    }
})

lastn.addEventListener('keyup',()=>{
    if (hasnumber(lastn.value.trim())){
        lerror.innerHTML = "Numbers not allowed";
    }
    else{
        lerror.innerHTML = "";
    }
})