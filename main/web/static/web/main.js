(function ($) {
    var local_path = window.location.pathname, csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var add_modal_form = "#add_modal_form", edit_modal_form = "#edit_modal_form";
    var variant_box = [add_modal_form, edit_modal_form];
    var DATA_DICT = {};
    var EDIT_DICT = {};
    var collectionlist_check = function () {
        $.ajax({
            url: local_path + 'manage/',
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrfmiddlewaretoken,
                s: "list",
            },
            dataType: "json",
            success: function (data) {
                var datalist = data;
                var output = $.map(datalist, function (val, i) {
                    var html = "";
                    html += `<tr>
                        <td>${i + 1}</td>
                        <td>${val.id}</td>
                        <td>${val.name}</td>
                        <td>${val.jasmin_host}</td>
                        <td>${val.jasmin_port}</td>
                        <td>${val.domain_name}</td>
                        
                        <td class="text-center" style="padding-top:4px;padding-bottom:4px;">
                            <div class="btn-group btn-group-sm">
                                <a href="javascript:void(0)" class="btn btn-light" onclick="return collection_manage('edit', '${i + 1}');"><i class="fas fa-edit"></i></a>
                                <a href="javascript:void(0)" class="btn btn-light" onclick="return collection_manage('delete', '${i + 1}');"><i class="fas fa-trash"></i></a>
                            </div>
                        </td>
                    </tr>`;
                    EDIT_DICT[val.id] = val;
                    DATA_DICT[i + 1] = val;
                    return html;
                });
                $("#collectionlist").html(datalist.length > 0 ? output : $(".isEmpty").html());

                if (!$.fn.DataTable.isDataTable('#sortable-table')) {
                    $('#sortable-table').DataTable({
                        "pageLength": 25,
                        // other DataTable options...
                    });
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                quick_display_modal_error(jqXHR.responseText);
            }
        });
    }
    collectionlist_check();
    window.collection_manage = function (cmd, index) {
        index = index || -1;
        if (cmd == "add") {
            showThisBox(variant_box, add_modal_form);
            $("#collection_modal").modal("show");
        } else if (cmd == "edit") {
            showThisBox(variant_box, edit_modal_form);
            var data = EDIT_DICT[index];
            console.log(data.id)
            $(edit_modal_form + " input[name=id]").val(data.id);
            $(edit_modal_form + " input[name=schema_name]").val(data.schema_name);
            $(edit_modal_form + " input[name=name]").val(data.name);
            $(edit_modal_form + " input[name=jasmin_host]").val(data.jasmin_host);
            $(edit_modal_form + " input[name=jasmin_port]").val(data.jasmin_port);
            $(edit_modal_form + " input[name=jasmin_username]").val(data.jasmin_username);
            $(edit_modal_form + " input[name=jasmin_password]").val(data.jasmin_password);
            $(edit_modal_form + " input[name=description]").val(data.description);
            $(edit_modal_form + " input[name=domain]").val(data.domain);
            $("#collection_modal").modal("show");
        } else if (cmd == "delete") {
            sweetAlert({
                title: global_trans["areyousuretodelete"],
                text: global_trans["youwontabletorevertthis"],
                type: 'warning',
                showCancelButton: true,
                cancelButtonClass: "btn btn-secondary m-btn m-btn--pill m-btn--icon",
                cancelButtonText: global_trans["no"],
                confirmButtonClass: "btn btn-danger m-btn m-btn--pill m-btn--air m-btn--icon",
                confirmButtonText: global_trans["yes"],
            }, function (isConfirm) {
                if (isConfirm) {
                    var data = DATA_DICT[index];
                    $.ajax({
                        type: "POST",
                        url: local_path + 'manage/',
                        data: {
                            csrfmiddlewaretoken: csrfmiddlewaretoken,
                            s: cmd,
                            id: data.id,
                        },
                        beforeSend: function () { },
                        success: function (data) {
                            toastr.success(data["message"], { closeButton: true, progressBar: true, });
                            collectionlist_check();
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            toastr.error(JSON.parse(jqXHR.responseText)["message"], { closeButton: true, progressBar: true, });
                        }
                    })
                }
            });
        }
    };

    $("#add_new_obj").on('click', function (e) {
        collection_manage('add');
    });
    $(add_modal_form + "," + edit_modal_form).on("submit", function (e) {
        e.preventDefault();
        var serializeform = $(this).serialize();
        var inputs = $(this).find("input, select, button, textarea");
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: serializeform,
            beforeSend: function () {
                inputs.prop("disabled", true);
            },
            success: function (data) {
                toastr.success(data["message"], {
                    closeButton: true,
                    progressBar: true,
                });
                inputs.prop("disabled", false);
                $(".modal").modal("hide");
                collectionlist_check();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                toastr.error(JSON.parse(jqXHR.responseText)["message"], {
                    closeButton: true,
                    progressBar: true,
                });
                inputs.prop("disabled", false);
            }
        });
    });
})(jQuery);