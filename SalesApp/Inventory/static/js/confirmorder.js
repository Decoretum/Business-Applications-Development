        let cost = document.getElementById('productcost').dataset.val;
        let chosen = document.getElementById('drop');
        chosen.addEventListener('change',()=>{
            let result = document.getElementById('totalcost');
            let chosen = document.getElementById('drop');
            let val = chosen.value;
            console.log(val);
            console.log(cost);
            result.value = "$" + parseFloat(parseInt(val) * parseFloat(cost.slice(0))).toFixed(2);
        })