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