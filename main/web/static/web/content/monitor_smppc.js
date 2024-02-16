(function($){
    var local_path = window.location.pathname, csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;;
    var smppc_view="#smppc_view";
    var variant_boxes = [smppc_view];
    var STATS_DICT = {};
    function sendEmailNotification(cid) {
        $.ajax({
            url: local_path + 'send_email_notification/'+ cid,  // Replace with your Django URL
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrfmiddlewaretoken,
                cid: cid,
            },
            dataType: 'json',
            success: function(data) {
                console.log('Success response:', data);
                console.log(data.message);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error sending email notification:', jqXHR.responseText);
            }
        });
    }
    var collectionlist_check = function () {
        $.ajax({
            url: local_path + 'manage/',
            type: "GET",
            data: {
                s: "list",
            },
            dataType: "json",
            success: function (data) {
                var datalist = data["stats"];
                var output = $.map(datalist, function (val, i) {
                    var statusClass = '';
                
                    // Set class based on status
                    if (val.status === 'DOWN') {
                        statusClass = 'text-danger'; // Red color for DOWN
                    } else if (val.status === 'BOUND') {
                        statusClass = 'text-success'; // Green color for BOUND
                    } else if (val.status === 'UNBOUND') {
                        statusClass = 'text-warning'; // Yellow color for UNBOUND
                    }
                
                    var html = `<tr>
                        <td>${i + 1}</td>
                        <td>${val.cid}</td>
                        <td>${val.connected_at}</td>
                        <td>${val.bound_at}</td>
                        <td>${val.disconnected_at}</td>
                        <td>${val.submits}</td>
                        <td>${val.delivers}</td>
                        <td>${val.qos_err}</td>
                        <td>${val.other_err}</td>
                        <td class="text-center"><i class="fas fa-circle fa-lg ${statusClass}"><i/></td>
                    </tr>`;
                
                    STATS_DICT[i + 1] = val;
                    if (val.status === "DOWN") {
                        sendEmailNotification(val.cid);
                    }
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
    }; 

    collectionlist_check();
    $("#smppc_view_obj").on('click', function(e){collection_manage('smppc');});
    // $(document).ready(function() {
    //     collectionlist_check();
    //   });
    setInterval(function () {
        collectionlist_check();
    }, 60000);
    
    $("li.nav-item.smppsubstats-menu").addClass("active");
})(jQuery);
