function enable() {
    if(document.getElementById("advanced").value==="") { 
           document.getElementById('advanced-btn-search').disabled = true; 
       } else { 
           document.getElementById('advanced-btn-search').disabled = false;
       }
   }

   function enable_home() {
    if(document.getElementById("txt-search").value==="") { 
           document.getElementById('btn-search').disabled = true; 
       } else { 
           document.getElementById('btn-search').disabled = false;
       }
   }

   function enable_search() {
    if(document.getElementById("txt-search").value==="") { 
           document.getElementById('btn-search').disabled = true; 
       } else { 
           document.getElementById('btn-search').disabled = false;
       }
   }