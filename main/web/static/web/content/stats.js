(function($){
    var local_path = window.location.pathname, csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var service_modal_form = "#service_modal_form";
    var variant_boxes = [service_modal_form];
    var STATS_DICT = {};
    var collectionlist_check = function(){
        $.ajax({
            url: local_path + 'manage/',
            type: "GET",
            data: {
                csrfmiddlewaretoken: csrfmiddlewaretoken,
                s: "list",

            },
            dataType: "json",
            success: function(data){
                var datalist = data["stats"];
                var output = $.map(datalist, function(val, i){
                    var html = "";
                    html += `<tr>
                        <td>${i+1}</td>
                        <td>${val.uid}</td>
                        <td>${val.smpp_bound}</td>
                        <td>${val.smpp_la}</td>
                        <td>${val.http_request_counter}</td>
                        <td class="text-center" style="padding-top:4px;padding-bottom:4px;">
                            <div class="btn-group btn-group-sm">
                                <a href="javascript:void(0)" class="btn btn-light" onclick="return collection_manage('service', '${i+1}');"><i class="fas fa-play-circle"></i></a>
                                <a href="javascript:void(0)" class="btn btn-light" onclick="return collection_manage('delete', '${i+1}');"><i class="fas fa-trash"></i></a>
                            </div>
                        </td>
                    </tr>`;
                    USERS_DICT[i+1] = val;
                    return html;
                });
                $("#collectionlist").html(datalist.length > 0 ? output : $(".isEmpty").html());
            }, error: function(jqXHR, textStatus, errorThrown){quick_display_modal_error(jqXHR.responseText);}
        });
    }
    collectionlist_check();
    window.collection_manage = function(cmd, index){
        index = index || -1;
        if (cmd == "delete") {
            sweetAlert({
                title: global_trans["areyousuretodelete"],
                text: global_trans["youwontabletorevertthis"],
                type: 'warning',
                showCancelButton: true,
                cancelButtonClass: "btn btn-secondary m-btn m-btn--pill m-btn--icon",
                cancelButtonText: global_trans["no"],
                confirmButtonClass: "btn btn-danger m-btn m-btn--pill m-btn--air m-btn--icon",
                confirmButtonText: global_trans["yes"],
            }, function(isConfirm){
                if (isConfirm) {
                    var data = USERS_DICT[index];
                    $.ajax({
                    	type: "POST",
                    	url: local_path + 'manage/',
                    	data: {
                    		csrfmiddlewaretoken: csrfmiddlewaretoken,
                    		s: cmd,
                    		uid: data.uid,
                    	},
                    	beforeSend: function(){},
						success: function(data){
							toastr.success(data["message"], {closeButton: true, progressBar: true,});
							collectionlist_check();
						},
						error: function(jqXHR, textStatus, errorThrown){
							toastr.error(JSON.parse(jqXHR.responseText)["message"], {closeButton: true, progressBar: true,});
						}
                    })
                }
            });
        } else if (cmd == "service") {
            var data = STATS_DICT[index];
            $(service_modal_form+" input[name=uid]").val(data.uid);
            showThisBox(variant_boxes, service_modal_form);
            $("#collection_modal").modal("show");
        } 
    }
    collection_manage("groups");
    // $("#add_new_obj").on('click', function(e){collection_manage('add');})/;
    $(service_modal_form).on("submit", function(e){
        e.preventDefault();
        var serializeform = $(this).serialize();
		var inputs = $(this).find("input, select, button, textarea");
		//inputs.prop("disabled", true);
		$.ajax({
			type: "POST",
			url: $(this).attr("action"),
			data: serializeform,
			beforeSend: function(){inputs.prop("disabled", true);},
			success: function(data){
				toastr.success(data["message"], {closeButton: true, progressBar: true,});
				inputs.prop("disabled", false);
				$(".modal").modal("hide");
				collectionlist_check();
				//setTimeout(location.reload.bind(location), 2000);
			},
			error: function(jqXHR, textStatus, errorThrown){
				toastr.error(JSON.parse(jqXHR.responseText)["message"], {closeButton: true, progressBar: true,});
				inputs.prop("disabled", false);
			}
		});
    });
    $("li.nav-item.users-menu").addClass("active");
})(jQuery);