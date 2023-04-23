let tempbox = document.getElementById('tempbox');
        let trigger = document.getElementById('edittemp');
        let back = document.getElementById('hideme');
        trigger.addEventListener('click',() => {
            tempbox.style.display = "inline";
            tempbox.classList.add("shade");
        })
        back.addEventListener('click',()=>{
            tempbox.style.display = "none";
            tempbox.classList.remove("shade");
        })

        let c = document.getElementById('Cost');
        let cnote = document.getElementById('costnote');

        c.addEventListener('keyup',(e)=>{

            if (c.value.trim() === ""){
                cnote.innerHTML = "";
            }

            else if (Number(c.value.slice(0)) <= 0){
                cnote.innerHTML = "Stock cannot be less than 0!";
            }

            else if (isNaN(c.value.slice(0))){
                cnote.innerHTML = "Not an integer/float"
            }


            else{
                cnote.innerHTML = "";
            }
        })

        let s = document.getElementById('stock')
        let snote = document.getElementById('stocknote');
        s.addEventListener('keyup',(e)=>{

            if (!Number.isInteger(Number(s.value)) || Number(s.value) === NaN || s.value.includes(".")){
                snote.innerHTML = "Not an integer!";
            }

            else if (Number(s.value) <= 0 && s.value !== ""){
                snote.innerHTML = "Stock cannot be less than 0!";
            }


            else{
                snote.innerHTML = "";
            }
        })