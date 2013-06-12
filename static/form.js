$(document).ready(function () {
    
    var _k1price = parseInt($("#k1Price").text().replace(".", ""));
    var _k16price = parseInt($("#k16Price").text().replace(".", ""));
    var _k64price = parseInt($("#k64Price").text().replace(".", ""));
    
    function renumber_group_buys($container) {
        var prefix = $container.attr("data-prefix");

        $container.find("div.group_buy").each(function (index, div) {
            var $div = $(div);
            var oldPrefix = prefix + "-" + $div.attr("data-index") + "-";
            var newPrefix = prefix + "-" + index + "-";
            var oldPrefixRegex = new RegExp(oldPrefix, 'g');

            $div.find("input").each(function (i, input) {
                var $input = $(input);

                newInputName = $input.attr("name").replace(oldPrefixRegex, newPrefix);
                $input.attr("id", newInputName);
                $input.attr("name", newInputName);
                $input.prev("label").attr("for", newInputName);
            });

            $div.attr("data-index", index);
        });
    }
    
    function update_subtotal() {
        var k1s = parseInt($("#miners-k1s").val()) || 0;
        var k16s = parseInt($("#miners-k16s").val()) || 0;
        var k64s = parseInt($("#miners-k64s").val()) || 0;
        
        var price = (k1s * _k1price) + (k16s * _k16price) + (k64s * _k64price);
        
        $("#subtotal").text(price / 100.0);
    }

    $('#add_group_buy').click(function (e) {
        var $oldDiv = $('div.group_buy:last');
        var $newDiv = $oldDiv.clone();

        $("ul.errors", $newDiv).remove();
        $newDiv.find("input[name!=csrf_token]").val("");
        $newDiv.hide().insertAfter($oldDiv).slideDown();
        renumber_group_buys($(".group_buys.form_section"));
    });

    $(".subform input").focus(function (e) {
        $(this).closest(".form_section").find(".form_error").slideUp();
        $(this).next(".errors").slideUp();
    });

    $(document).on("click", ".subform .remove.btn", function (e) {
        $(this).closest(".group_buy").slideUp(function () { $(this).remove(); });
        renumber_group_buys($(".group_buys.subform"));
    });
    
    $("#miners_form input").change(function () {
        update_subtotal();
    });

    // Navigate to the first order form error, if there is one.
    (function () {
        var $errors = $(".error, .form_error");
        if ($errors.length > 0) {
            window.location.hash = $errors.first().closest(".subform").attr("id");
        }
    })();
    
    update_subtotal();
});
