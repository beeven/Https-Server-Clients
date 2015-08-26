(function($){
    $(document).ready(function(){
        $("#date_created_now").click(function(evt){
            evt.preventDefault();
            $("#datecreated").val(moment().utc().format())

        })

        $("#dataform").validator().on('submit',function(evt){
            if(evt.isDefaultPrevented()){
            } else {
                console.log("hello")
                var data = {
                    protocol: $("#httpprotocol").prop("checked") ? "http" : "https",
                    url: $("")
                }
            }
        })
    })
})(jQuery);