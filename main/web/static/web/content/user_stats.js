(function($){
    var local_path = window.location.pathname;
    var users_view="#users_view";
    var variant_boxes = [users_view];
    var USERS_DICT = {}; var USER_DICT={};
    var collectionlist_check = function(){
        $.ajax({
            url: local_path + 'manage/',
            type: "GET",
            data: {
                s: "list",

            },
            dataType: "json",
            success: function(data){
                var datalist = data["users"];
                var output = $.map(datalist, function(val, i){
                    var html = "";
                    html += `<tr>
                        <td>${i+1}</td>
                        <td>${val.uid}</td>
                        <td>${val.smpp_bound_conn}</td>
                        <td>${val.smpp_la}</td>
                        <td>${val.http_req_counter}</td>
                        <td>${val.http_la}</td>
                        <td class="text-center" style="padding-top:4px;padding-bottom:4px;">
                            <div class="btn-group btn-group-sm">
                                <a href="javascript:void(0)" class="btn btn-light" onclick="return collection_manage('user', '${val.uid}');"><i class="fas fa-play-circle"></i></a>
                            </div>
                        </td>
                    </tr>`;
                    USERS_DICT[i+1] = val;
                    return html;
                },
                console.log(data)
                );
                $("#collectionlist").html(datalist.length > 0 ? output : $(".isEmpty").html());
            }, error: function(jqXHR, textStatus, errorThrown){quick_display_modal_error(jqXHR.responseText);}
        });
    }; 

    collectionlist_check();
    window.collection_manage = function(cmd, uid) {
        if (cmd === "user") {
            var datalist;  // Define datalist in the broader scope
    
            $.ajax({
                url: local_path + 'manage/',
                type: "GET",
                data: {
                    s: "user",
                    uid: uid,
                },
                dataType: "json",
                success: function(data) {
                    datalist = data["user"];
                    var output = `
                        <table>
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Items</th>
                                    <th>Type</th>
                                    <th>Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                <!-- Iterate through your data and generate rows -->
                                ${datalist.map((row, index) => `
                                    <tr>
                                        <td>${index + 1}</td>
                                        <td><span style="margin-right: 15px;">${row.item}</span></td>
                                        <td><span style="margin-right: 10px;">${row.type}</span></td>
                                        <td><span style="margin-right: 10px;">${row.value}</span></td>
                                    </tr>`).join('')}
                            </tbody>
                        </table>
                    `;
                    
                    // Populate USER_DICT (if needed)
                    USER_DICT = datalist.reduce((dict, val, i) => {
                        dict[i + 1] = val;
                        return dict;
                    }, {});
    
                    // Append the HTML content to the modal body
                    $("#usersDetailContent").html(datalist.length > 0 ? output : $(".isEmpty").html());
    
                    // Show the modal
                    $("#usersDetailModal").modal("show");
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    quick_display_modal_error(jqXHR.responseText);
                },
            });
        }
    };

            // You can use datalist here if needed, or perform other actions after initiating the AJAX request.
    $("#users_view_obj").on('click', function(e){collection_manage('user');});
    $("li.nav-item.stats-menu").addClass("active");
    $("li.nav-item.usersubstats-menu").addClass("active");

})(jQuery);

