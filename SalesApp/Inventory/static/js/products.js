/*let tables = document.getElementsByTagName('table');
    let rows = document.getElementsByTagName('tr');
    let lastrow = document.querySelector('last')
    for (let i = 0; i < tables.length; i++){
        let len = tables.childNodes[1].childNodes.length
        tables[i].childNodes[1].childNodes[len-2].childNodes[2].nodeValue = "Additional Information"
   }*/
   function myFunction(){
    let list, filtered, header;
    
    let products = document.getElementsByTagName('tr');
    let search = document.getElementById('searchbar');
    let tbody = document.getElementById('products');
    let sum = 0;
    let coveredsum = 0;
    header = document.querySelector('.identify');   
    filtered = search.value.toUpperCase().replaceAll(" ", "");

    for (let i = 1; i < products.length; i++){
        let text = products[i].childNodes[3].textContent;
        let newtext = text.replaceAll(" ", "")
        if (newtext.toUpperCase().indexOf(filtered) > -1){
            products[i].style.display = ""; 
        }
        else{
            products[i].style.display = "none";
            coveredsum += 1;
        }
        sum += 1;
    }

    if (coveredsum === sum){
        //console.log(tbody.childNodes[1])
        //console.log(header.childNodes)
        tbody.style.borderRadius = "9px";
        tbody.childNodes[1].style.borderRadius = "9px";
        header.innerHTML = "<div style='background-color : azure;'> No results! </div>";
        header.classList.add("headerreveal");
    }

    else{
        header.classList.remove("headerreveal");
        //header.childNodes.style.backgroundColor = "rgb(232, 213, 196)"; 
        header.innerHTML = "<tr class='identify'> <th style='border-top-left-radius: 9px;'> Image </th> <th> Product </th><th> Length </th> <th> Manufacturer Name </th> <th> Quantity </th> <th style='border-top-right-radius: 9px;''> Action </th> </tr>"
    }

   }