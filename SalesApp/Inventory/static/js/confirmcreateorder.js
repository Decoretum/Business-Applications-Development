        let cost = document.getElementById('costval').dataset.val;
        let chosen = document.getElementById('drop');
        chosen.addEventListener('change',()=>{
            let result = document.getElementById('totalcost');
            let chosen = document.getElementById('drop');
            let val = chosen.value;
            result.value = "$" + parseFloat(parseInt(val) * parseFloat(cost.slice(0))).toFixed(2);
        })

        /*let order = document.getElementById('Order')
        let person = document.getElementById('Person')
        order.addEventListener('change',()=>{
            let obj = {

            }
            let query = "{% for i in Orders %} {{ i.BL }} {% endfor %}"
            let queries = query.trim().replaceAll(" ","")
            let sam = 0;
            if (queries.length === 0){
                console.log('empty')
                person.value = "Type Name of Consignee"
                console.log("queries.`${sam}`")
            }
            else{
                let data = order.value;
                let sam = 0;
            

            }
           
            
        })*/

        
        


        