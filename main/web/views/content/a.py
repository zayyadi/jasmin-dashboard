args = {
    "user": [
        {"item": "bind_count", "types": ["SMPP"], "value": ["0"]},
        {"item": "unbind_count", "types": ["SMPP"], "value": ["0"]},
        {
            "item": "bound_connections_count",
            "types": ["SMPP"],
            "value": [
                '{"bind_receiver": 0',
                '"bind_transceiver": 0',
                '"bind_transmitter": 0}',
            ],
        },
        {"item": "submit_sm_request_count", "types": ["SMPP"], "value": ["0"]},
        {"item": "last_activity_at", "types": ["SMPP"], "value": ["ND"]},
        {"item": "qos_last_submit_sm_at", "types": ["SMPP"], "value": ["ND"]},
        {"item": "submit_sm_count", "types": ["SMPP"], "value": ["0"]},
        {"item": "deliver_sm_count", "types": ["SMPP"], "value": ["0"]},
        {"item": "data_sm_count", "types": ["SMPP"], "value": ["0"]},
        {"item": "elink_count", "types": ["SMPP"], "value": ["0"]},
        {"item": "throttling_error_count", "types": ["SMPP"], "value": ["0"]},
        {"item": "other_submit_error_count", "types": ["SMPP"], "value": ["0"]},
        {"item": "connects_count", "types": ["HTTP"], "value": ["0"]},
        {"item": "last_activity_at", "types": ["HTTP"], "value": ["ND"]},
        {"item": "submit_sm_request_count", "types": ["HTTP"], "value": ["0"]},
        {"item": "balance_request_count", "types": ["HTTP"], "value": ["0"]},
        {"item": "rate_request_count", "types": ["HTTP"], "value": ["0"]},
    ],
    "status": 200,
    "message": "ok",
}

args = {
    "users": [
        {
            "uid": "huawei_id",
            "smpp_bound_conn": "0",
            "smpp_la": "ND",
            "http_req_counter": "0",
            "http_la": "ND",
            "status": "UNBOUND",
        },
        {
            "uid": "test",
            "smpp_bound_conn": "0",
            "smpp_la": "ND",
            "http_req_counter": "0",
            "http_la": "ND",
            "status": "UNBOUND",
        },
        {
            "uid": "new",
            "smpp_bound_conn": "0",
            "smpp_la": "ND",
            "http_req_counter": "0",
            "http_la": "ND",
            "status": "UNBOUND",
        },
    ],
    "status": 200,
    "message": "ok",
}
