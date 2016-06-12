from flask import render_template, request, Blueprint, Response
from .logic_conoha import ConoHaToken, ConoHaISO, ConoHaServer


conoha = Blueprint('conoha', __name__, template_folder='templates', static_folder='static')


@conoha.route('/', methods=['GET', 'POST'])
def index():
        return render_template('conoha/index.html')


@conoha.route('/api/token/', methods=['POST'])
def get_token():
    content = request.json
    region = content['region']
    tenant_id = content['tenant_id']
    tenant_name = content['tenant_name']
    api_username = content['api_username']
    api_password = content['api_password']
    conoha_token = ConoHaToken(
        region=region, tenant_id=tenant_id,
        tenant_name=tenant_name, api_username=api_username, api_password=api_password
    )
    token = conoha_token.get_token()
    return Response(token, 200, content_type='application/json')


@conoha.route('/api/iso/', methods=['POST'])
def iso():
    content = request.json
    print(content)
    region = content['region']
    token = content['token']
    server_id = content['server_id']
    tenant_id = content['tenant_id']
    iso_image_url = content['iso_image_url']
    iso_image_path = content['iso_image_path']
    action = content['action']
    conoha_iso = ConoHaISO(
        region=region, token=token, server_id=server_id,
        tenant_id=tenant_id, iso_image_url=iso_image_url, iso_image_path=iso_image_path)
    if action == 'download_iso':
        iso_download_result = conoha_iso.push_iso_url()
        return Response(response=iso_download_result, status=200, content_type='application/json')
    elif action == 'list_iso':
        iso_list = conoha_iso.get_iso_image_list()
        print(iso_list)
        return Response(response=iso_list, status=200, content_type='application/json')
    elif action == 'mount_iso':
        mount_iso_result = conoha_iso.mount_iso()
        return Response(response=mount_iso_result, status=200, content_type='application/json')
    elif action == 'unmount_iso':
        unmount_iso_result = conoha_iso.unmount_iso()
        return Response(response=unmount_iso_result, status=200, content_type='application/json')


@conoha.route('/api/server/', methods=['POST'])
def server():
    content = request.json
    print(content)
    region = content['region']
    tenant_id = content['tenant_id']
    token = content['token']
    server_id = content['server_id']
    action = content['action']
    conoha_server = ConoHaServer(region=region, tenant_id=tenant_id, token=token, server_id=server_id)
    if action == 'list_servers':
        server_list = conoha_server.get_server_list()
        print(server_list)
        return Response(response=server_list, status=200, content_type='application/json')
    elif action == 'start_server':
        start_server_result = conoha_server.start_server()
        return Response(response=start_server_result, status=200, content_type='application/json')
    elif action == 'shutdown_server':
        shutdown_server_result = conoha_server.shutdown_server()
        return Response(response=shutdown_server_result, status=200, content_type='application/json')
    elif action == 'stop_server':
        stop_server_result = conoha_server.force_stop_server()
        return Response(response=stop_server_result, status=200, content_type='application/json')
    elif action == 'open_vnc_console':
        vnc_url = conoha_server.get_vnc_url()
        return Response(response=vnc_url, status=200, content_type='application/json')
