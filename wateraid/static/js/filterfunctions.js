function addSearchElement(element) {
    document.getElementById('filter_form').innerHTML += 
    '<div id="'+element+'"><input id="'+element+'" type="hidden" value="'+element+'" name="search_form"/> \
    <button type="button" id="'+element+'" onclick="removeElement(' +"'"+ element + "'" + ')" \
    class="btn btn-default button3"\
    name="search_form" value="'+element+'">'+element+'<i class="fa fa-times fa-fw" aria-hidden="true"></i></button></div>';
}

function addConceptElement(element) {
    document.getElementById('button'+element).disabled = true;
    document.getElementById('filter_form').innerHTML += 
    '<div id="'+element+'"><input id="'+element+'" type="hidden" value="'+element+'" name="concept_form"/> \
    <button type="button" id="'+element+'" onclick="removeElement(' +"'"+ element + "'" + ')"  \
    class="btn btn-default button3" \
    name="concept_form" value="'+element+'">'+element+'<i class="fa fa-times fa-fw" aria-hidden="true"></i></button></div>';
}

function addEntityElement(element) {
    document.getElementById('button'+element).disabled = true;
    document.getElementById('filter_form').innerHTML += 
    '<div id="'+element+'"><input id="'+element+'" type="hidden" value="'+element+'" name="entities_form"/> \
    <button type="button" id="'+element+'" onclick="removeElement(' +"'"+ element + "'" + ')" \
    class="btn btn-default button3" \
    name="entities_form" value="'+element+'">'+element+'<i class="fa fa-times fa-fw" aria-hidden="true"></i></button></div>';
}

function addSentimentElement(element) {
    var buttons = document.getElementsByName("sentiment_term");
    for (let i = 0; i < buttons.length; i++) {
      buttons[i].disabled = true;
    }
    document.getElementById('filter_form').innerHTML += 
    '<div id="'+element+'"><input id="'+element+'" type="hidden" value="'+element+'" name="sentiment_form" style="display: inline-block;"/> \
    <button type="button" id="'+element+'" onclick="removeSentimentElement(' +"'"+ element + "'" + ')" \
    class="btn btn-default button3" style="display:inline;" \
    name="sentiment_form" value="'+element+'">'+element+'<i class="fa fa-times fa-fw" aria-hidden="true"></i></button></div>';
}

function addDateElement(element) {
    var buttons = document.getElementsByName("date_term");
    for (let i = 0; i < buttons.length; i++) {
      buttons[i].disabled = true;
    }

    document.getElementById('filter_form').innerHTML += 
    '<div id="'+element+'"><input id="'+element+'" type="hidden" value="'+element+'" name="date_form" style="display: inline-block;"/> \
    <button type="button" id="'+element+'" onclick="removeDateElement(' +"'"+ element + "'" + ')" \
    class="btn btn-default button3" style="display:inline;" \
    name="date_form" value="'+element+'">'+element+'<i class="fa fa-times fa-fw" aria-hidden="true"></i></button></div>';

}

function addLocElement(element) {
    document.getElementById('button'+element).disabled = true;
    document.getElementById('filter_form').innerHTML += 
    '<div id="'+element+'"><input id="'+element+'" type="hidden" value="'+element+'" name="locations_form"/> \
    <button type="button" id="'+element+'" onclick="removeElement(' +"'"+ element + "'" + ')" \
    class="btn btn-default button3" \
    name="locations_form" value="'+element+'">'+element+'<i class="fa fa-times fa-fw" aria-hidden="true"></i></button></div>';
}

function addLangElement(element) {
    var buttons = document.getElementsByName("language_term");
    for (let i = 0; i < buttons.length; i++) {
      buttons[i].disabled = true;
    }
    document.getElementById('filter_form').innerHTML += 
    '<div id="'+element+'"><input id="'+element+'" type="hidden" value="'+element+'" name="lang_form"/> \
    <button type="button" id="'+element+'" onclick="removeLangElement(' +"'"+ element + "'" + ')" \
    class="btn btn-default button3" style="display: inline-block" \
    name="lang_form" value="'+element+'">'+element+'<i class="fa fa-times fa-fw" aria-hidden="true"></i></button></div>';    
}

function addSourceElement(element) {
    document.getElementById('button'+element).disabled = true;
    document.getElementById('filter_form').innerHTML += 
    '<div id="'+element+'"><input id="'+element+'" type="hidden" value="'+element+'" name="source_form"/> \
    <button type="button" id="'+element+'" onclick="removeElement(' +"'"+ element + "'" + ')" \
    class="btn btn-default button3" \
    name="source_form" value="'+element+'">'+element+'<i class="fa fa-times fa-fw" aria-hidden="true"></i></button></div>';
}

function addWaterAidElement(element) {
    document.getElementById('button'+element).disabled = true;
    document.getElementById('filter_form').innerHTML += 
    '<div id="'+element+'"><input id="'+element+'" type="hidden" value="'+element+'" name="wateraid_form" /> \
    <button type="button" id="'+element+'" onclick="removeElement(' +"'"+ element + "'" + ')" \
    class="btn btn-default button3" \
    name="wateraid_form" value="'+element+'">'+element+'<i class="fa fa-times fa-fw" aria-hidden="true"></i></button></div>';
}

function removeElement(element) {
    var myobj = document.getElementById(element);
    myobj.remove();
    document.getElementById('button'+element).disabled = false;
}

function removeLangElement(element) {
    var myobj = document.getElementById(element);
    myobj.remove();
    var buttons = document.getElementsByName("language_term");
    for (let i = 0; i < buttons.length; i++) {
      buttons[i].disabled = false;
    }
}

function removeDateElement(element) {
    var myobj = document.getElementById(element);
    myobj.remove();
    var buttons = document.getElementsByName("date_term");
    for (let i = 0; i < buttons.length; i++) {
      buttons[i].disabled = false;
    }
}

function removeSentimentElement(element) {
    var myobj = document.getElementById(element);
    myobj.remove();
    var buttons = document.getElementsByName("sentiment_term");
    for (let i = 0; i < buttons.length; i++) {
      buttons[i].disabled = false;
    }
}

