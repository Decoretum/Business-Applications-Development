let placeholder = document.getElementById('drop');
        let prodplaceholder = document.getElementById('proddrop')
        let result = document.getElementById('Manufacturer');
        let cost = '{{K.Order.Cost}}';
        let quant = document.getElementById('num');
        result.value = parseInt(quant.value) * parseInt(cost.slice(1));

        placeholder.addEventListener('change',()=>{
            let chosen = document.getElementById('drop');
            let val = chosen.value;
            console.log(val);
            console.log(cost);
            result.value = parseInt(val) * parseInt(cost.slice(1));
        })