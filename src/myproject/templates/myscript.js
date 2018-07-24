let manufacturer_select = document.getElementById('manufacturer');
let model_select = document.getElementById('model');
let trim_select = document.getElementById('trim');
manufacturer_select.onchange = function(){
  manufacturer_id = manufacturer_select.value;
  fetch('/models/' + manufacturer_id).then(function(response){
    response.json().then(function(data){
      let optionHTML = "";
      for(let model from data.models){
        optionHTML += '<option value="' + model.id + '">' + model.name + '</option>'
      }
      model_select.innerHTML = optionHTML;
    });
  });
}




















//The stuff below is from the
$(document).ready(function() {
        $('#foodkind').change(function() {

          var foodkind = $('#foodkind').val();

          // Make Ajax Request and expect JSON-encoded data
          $.getJSON(
            '/get_food' + '/' + foodkind,
            function(data) {

              // Remove old options
              $('#food').find('option').remove();

              // Add new items
              $.each(data, function(key, val) {
                var option_item = '<option value="' + val + '">' + val + '</option>'
                $('#food').append(option_item);
              });
            }
          );
        });
      });




      <body>
   <form>
     {{ form.foodkind() }}
     {{ form.food() }}
   </form>
 </body>
</html>
