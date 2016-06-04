from flask import render_template, jsonify, request, Response, Blueprint
from . import logic_json, logic_routeros
import json


ads = Blueprint('ads', __name__, template_folder='templates', static_folder='static')


@ads.route('/')
def index():
    return render_template("ads/index.html")


@ads.route('/api/')
def api_page():
    return render_template("ads/api.html")


@ads.route('/api/json/ip_list/', methods=['POST'])
def api_ad_server_list():
    content = request.json
    ip_version = content['ip_version']
    ip_format = content['ip_format']
    return jsonify(logic_json.ad_server_list(ip_version, ip_format))


@ads.route('/api/routeros/ip_list/<string:ip_version>/ad_server_list')
def api_routeros(ip_version):
    return Response(logic_routeros.gen_commands(ip_version), content_type='text/plain')


@ads.route('/web_request', methods=['POST'])
def web_request():
    content = request.json
    output_format = content['output_format']
    ip_version = content['ip_version']
    ip_format = content['ip_format']
    if output_format == 'json_pretty':
        data = logic_json.ad_server_list(ip_version=ip_version, ip_format=ip_format)
        return Response(json.dumps(data, indent=4), 200, content_type='text/plain')
    elif output_format == 'json_compact':
        data = logic_json.ad_server_list(ip_version=ip_version, ip_format=ip_format)
        return Response(json.dumps(data, separators=(',', ':')), 200, content_type='text/plain')
    elif output_format == 'RouterOS':
        data = logic_routeros.gen_commands(ip_version)
        return Response(data, 200, content_type='text/plain')
