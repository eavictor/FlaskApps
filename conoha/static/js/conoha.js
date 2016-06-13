// initialize tooltip js
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });

    // Token
    $('#get_token').click(function() {
        // get region
        var region = $('input[type="radio"][name="region"]:checked').val();
        // get tenant_id
        var tenant_id = $('#tenant_id').val();
        // get tenant_name
        var tenant_name = $('#tenant_name').val();
        // get api_id
        var api_id = $('#api_id').val();
        // get api_pw
        var api_pw = $('#api_pw').val();
        // send AJAX request
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/conoha/api/token/',
            data: JSON.stringify({
                'region': region,
                'tenant_id': tenant_id,
                'tenant_name': tenant_name,
                'api_id': api_id,
                'api_pw': api_pw
            }),
            success: function(response) {
                $('#token').val(response['token']);
                $('#token_info').css('display', '').empty().append(response['error']);
            },
            error: function() {
                $('#token_info').css('display', '').empty().append('送信失敗');
            }
        });
    });




    // ISO
    function iso_func(action, region, tenant_id, token, server_id, iso_image_url, iso_image_path) {
        // send AJAX request
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/conoha/api/iso/',
            data: JSON.stringify({
                'region': region,
                'tenant_id': tenant_id,
                'token': token,
                'server_id': server_id,
                'iso_image_url': iso_image_url,
                'iso_image_path': iso_image_path,
                'action': action
            }),
            success: function(response) {
                if (action === 'download_iso') {
                    if (response['request']['iso-image']['url'] != null) {
                        $('#download_iso_info').css('display', '').empty().append(response['request']['iso-image']['url']).append(' 送信成功');
                    } else {
                        $('#download_iso_info').css('display', '').empty().append('送信失敗');
                    }
                } else if (action === 'list_iso') {
                    $('#iso_list').css('display', '').empty();
                    $.each(response, function(key, value) {
                        $('#iso_list').append($('<option></option>').attr('value', value).text(key));
                    });
                    $('#list_iso_info').css('display', '').empty().append('リスト取得成功');
                } else if (action === 'mount_iso') {
                    $('#mount_iso_info').css('display', '').empty().append(response['message']);
                } else if (action === 'unmount_iso') {
                    $('#mount_iso_info').css('display', '').empty().append(response['message']);
                }
            },
            complete: function(response) {
                console.log(response);
                if (action === 'list_iso') {
                    if (response.responseText === 'missing token') {
                        $('#list_iso_info').css('display', '').empty().append(response.responseText);
                    }
                }
            },
            error: function() {
                if (action === 'download_iso') {
                    $('#download_iso_info').css('display', '').empty().append('送信失敗');
                } else if (action === 'list_iso') {
                    $('#list_iso_info').css('display', '').empty().append('リスト取得失敗');
                } else if (action === 'mount_iso') {
                    $('#mount_iso_info').css('display', '').empty().append('送信失敗(マウントISO)');
                } else if (action === 'unmount_iso') {
                    $('#mount_iso_info').css('display', '').empty().append('送信失敗(アンマウントISO)');
                }
            }
        });
    }

    // download ISO
    $('#download_iso').click(function() {
        // action
        var action = 'download_iso';
        // get region
        var region = $('input[type="radio"][name="region"]:checked').val();
        // get tenant_id
        var tenant_id = $('#tenant_id').val();
        // get token
        var token = $('#token').val();
        // get server_id
        var server_id = '';
        // get iso_image_url
        var iso_image_url = $('#iso_image_url').val();
        // get iso_image path
        var iso_image_path = '';
        // send AJAX request
        iso_func(action, region, tenant_id, token, server_id, iso_image_url, iso_image_path);
    });

    // list ISO
    $('#list_iso').click(function() {
        // action
        var action = 'list_iso';
        // get region
        var region = $('input[type="radio"][name="region"]:checked').val();
        // get tenant_id
        var tenant_id = $('#tenant_id').val();
        // get token
        var token = $('#token').val();
        // get server_id
        var server_id = '';
        // get iso_image_url
        var iso_image_url = '';
        // get iso_image path
        var iso_image_path = '';
        // send AJAX request
        iso_func(action, region, tenant_id, token, server_id, iso_image_url, iso_image_path);
    });

    // mount ISO
    $('#mount').click(function() {
        // action
        var action = 'mount_iso';
        // get region
        var region = $('input[type="radio"][name="region"]:checked').val();
        // get tenant_id
        var tenant_id = $('#tenant_id').val();
        // get token
        var token = $('#token').val();
        // get server_id
        var server_id = $('#server_list').find('option:selected').val();
        // get iso_image_url
        var iso_image_url = '';
        // get iso_image path
        var iso_image_path = $('#iso_list').find('option:selected').val();
        // send AJAX request
        iso_func(action, region, tenant_id, token, server_id, iso_image_url, iso_image_path);
    });

    // unmount ISO
    $('#unmount').click(function() {
        // action
        var action = 'unmount_iso';
        // get region
        var region = $('input[type="radio"][name="region"]:checked').val();
        // get tenant_id
        var tenant_id = $('#tenant_id').val();
        // get token
        var token = $('#token').val();
        // get server_id
        var server_id = $('#server_list').find('option:selected').val();
        // get iso_image_url
        var iso_image_url = '';
        // get iso_image path
        var iso_image_path = '';
        // send AJAX request
        iso_func(action, region, tenant_id, token, server_id, server_id, iso_image_url, iso_image_path);
    });




    // shutdown / force stop / start the selected server and open vnc console
    function server_func(action, region, tenant_id, token, server_id) {
        // send AJAX request
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/conoha/api/server/',
            data: JSON.stringify({
                'region' : region,
                'tenant_id': tenant_id,
                'token': token,
                'server_id': server_id,
                'action': action
            }),
            success: function(response) {
                console.log(response);
                if (action === 'list_servers') {
                    $('#server_list').css('display', '').empty();
                    $.each(response, function(key, value) {
                        $('#server_list').append($('<option></option>').attr('value', key).text(value));
                    });
                    $('#list_servers_info').css('display', '').empty().append('リスト取得成功');
                }else if (action === 'start_server') {
                    $('#server_command').css('display', '').empty().append(response['code']).append(' ').append(response['message']);
                } else if (action === 'shutdown_server') {
                    $('#server_command').css('display', '').empty().append(response['code']).append(' ').append(response['message']);
                } else if (action === 'stop_server') {
                    $('#server_command').css('display', '').empty().append(response['code']).append(' ').append(response['message']);
                } else if (action === 'open_vnc_console') {
                    if (response['code'] === 200) {
                        $('#vnc_console_info').css('display', '').empty().append(response['vnc_url']);
                        window.open(response['vnc_url'])
                    } else {
                        $('#vnc_console_info').css('display', '').empty().append(response['message']);
                    }
                }
            },
            complete: function(response) {
                if (action === 'list_servers') {
                    if (response.responseText === 'missing token') {
                        $('#list_servers_info').css('display', '').empty().append(response.responseText);
                    }
                }
            },
            error: function() {
                if (action === 'list_servers') {
                    $('#list_server_info').css('display', '').empty().append('リスト取得失敗');
                } else if (action === 'start_server') {
                    $('#server_command').css('display', '').empty().append('送信失敗(起動)')
                } else if (action === 'shutdown_server') {
                    $('#server_command').css('display', '').empty().append('送信失敗(停止)')
                } else if (action === 'stop_server') {
                    $('#server_command').css('display', '').empty().append('送信失敗(強制停止)')
                } else if (action === 'open_vnc_console') {
                    $('#vnc_console_info').css('display', '').empty().append('送信失敗')
                }
            }
        });
    }

    // list servers
    $('#list_servers').click(function() {
        // action
        var action = 'list_servers';
        // get region
        var region = $('input[type="radio"][name="region"]:checked').val();
        // get tenant_id
        var tenant_id = $('#tenant_id').val();
        // get token
        var token = $('#token').val();
        // get server_id
        var server_id = '';
        // send AJAX request
        server_func(action, region, tenant_id, token, server_id);
    });

    // start server
    $('#start_server').click(function() {
        // action
        var action = 'start_server';
        // get region
        var region = $('input[type="radio"][name="region"]:checked').val();
        // get tenant_id
        var tenant_id = $('#tenant_id').val();
        // get token
        var token = $('#token').val();
        // get server_id
        var server_id = $('#server_list').find('option:selected').val();
        // send AJAX request
        server_func(action, region, tenant_id, token, server_id);
    });

    // shutdown server
    $('#shutdown_server').click(function() {
        // action
        var action = 'shutdown_server';
        // get region
        var region = $('input[type="radio"][name="region"]:checked').val();
        // get tenant_id
        var tenant_id = $('#tenant_id').val();
        // get token
        var token = $('#token').val();
        // get server_id
        var server_id = $('#server_list').find('option:selected').val();
        // send AJAX request
        server_func(action, region, tenant_id, token, server_id);
    });

    // stop server
    $('#stop_server').click(function() {
        // action
        var action = 'stop_server';
        // get region
        var region = $('input[type="radio"][name="region"]:checked').val();
        // get tenant_id
        var tenant_id = $('#tenant_id').val();
        // get token
        var token = $('#token').val();
        // get server_id
        var server_id = $('#server_list').find('option:selected').val();
        // send AJAX request
        server_func(action, region, tenant_id, token, server_id);
    });

    // open VNC console
    $('#open_vnc_console').click(function() {
        // action
        var action = 'open_vnc_console';
        // get region
        var region = $('input[type="radio"][name="region"]:checked').val();
        // get tenant_id
        var tenant_id = $('#tenant_id').val();
        // get token
        var token = $('#token').val();
        // get server_id
        var server_id = $('#server_list').find('option:selected').val();
        // send AJAX request
        server_func(action, region, tenant_id, token, server_id);
    });