let collect = document.getElementById('collect');
let prepaid = document.getElementById('prepaid');

function val(e){
    let holder = document.getElementById('fin');
    holder.value = e.target.value;
}

collect.addEventListener('click', val);
prepaid.addEventListener('click', val);


/*let s = document.getElementById('voyage');
        let snote = document.getElementById('voy');
        console.log(s.value);
        s.addEventListener('keyup',(e)=>{

            if (!Number.isInteger(Number(s.value)) || Number(s.value) === NaN || s.value.includes(".") || s.value.includes("-")){
                snote.innerHTML = "Not a valid Voyage number!";
            }

            else if (Number(s.value) <= 0 && s.value !== ""){
                snote.innerHTML = "Stock cannot be less than 0!";
            }


            else{
                snote.innerHTML = "";
            }
        })*/

        let c = document.getElementById('charges');
        let cnote = document.getElementById('coy');

        c.addEventListener('keyup',(e)=>{
            if (isNaN(c.value % 1)){
                cnote.innerHTML = "Not a valid Charges number!";
            }

            else if (Number(c.value) < 0 && c.value !== "" || c.value.includes('-')){
                cnote.innerHTML = "Charges cannot be less than 0!";
            }


            else{
                cnote.innerHTML = "";
            }
        })

        let r = document.getElementById('rate');
        let rnote = document.getElementById('roy');
        r.addEventListener('keyup',(e)=>{

            if (isNaN(r.value % 1)){
                rnote.innerHTML = "Not a valid rate number!";
            }

            else if (Number(r.value) < 0 && r.value !== "" || r.value.includes('-')){
                rnote.innerHTML = "Rate cannot be less than 0!";
            }


            else{
                rnote.innerHTML = "";
            }
        })