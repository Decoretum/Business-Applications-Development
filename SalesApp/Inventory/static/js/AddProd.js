let s = document.getElementById('Stock')
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
        
        let c = document.getElementById('Cost');
        let cnote = document.getElementById('costnote');

        c.addEventListener('keyup',(e)=>{

            if (c.value.trim() === ""){
                cnote.innerHTML = "";
            }

            else if (isNaN(c.value)){
                cnote.innerHTML = "Not an integer/float"
            }   

            else if (Number(c.value) <= 0){
                cnote.innerHTML = "Stock cannot be less than or equal to 0!";
            }

            else{
                cnote.innerHTML = "";
            }
        })