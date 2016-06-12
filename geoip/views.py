from flask import render_template, jsonify, request, Response, Blueprint
from . import logic_json
from . import logic_routeros
import json


geoip = Blueprint('geoip', __name__, template_folder='templates', static_folder='static')


@geoip.route('/')
def index():
    return render_template("geoip/index.html")


@geoip.route('/api/')
def api_page():
    return render_template("geoip/api.html")


@geoip.route('/api/json/ip_list/', methods=['POST'])
def api_ip_list():
    content = request.json
    ip_version = content['ip_version']
    ip_format = content['ip_format']
    countries = content['countries']
    return jsonify(logic_json.ip_lists(ip_version=ip_version, ip_format=ip_format, countries=countries))


@geoip.route('/api/json/country/', methods=['POST'])
def api_country():
    content = request.json
    request_ips = content['request_ips']
    return jsonify(logic_json.which_country(request_ips))


@geoip.route('/api/routeros/ip_list/<string:ip_version>/<string:country_list>')
def api_routeros(ip_version, country_list):
    return Response(logic_routeros.gen_commands(ip_version, country_list), content_type='text/plain')


@geoip.route('/web_request', methods=['POST'])
def web_request():
    content = request.json
    output_format = content['output_format']
    ip_version = content['ip_version']
    ip_format = content['ip_format']
    country_list = content['country_list']
    if (output_format is not None) and (ip_version is not None) and (country_list is not None):
        # return pretty json format
        if output_format == 'json_pretty':
            countries = country_list.split(',')
            data = logic_json.ip_lists(ip_version=ip_version, ip_format=ip_format, countries=countries)
            return Response(json.dumps(data, indent=4), 200, content_type='text/plain')
        # return compact json format
        elif output_format == 'json_compact':
            countries = country_list.split(',')
            data = logic_json.ip_lists(ip_version=ip_version, ip_format=ip_format, countries=countries)
            return Response(json.dumps(data, separators=(',', ':')), 200, content_type='text/plain')
        # return RouterOS commands
        elif output_format == 'RouterOS':
            data = logic_routeros.gen_commands(ip_version, country_list)
            return Response(data, 200, content_type='text/plain')
    else:
        errors = {
            'output_format_error': output_format,
            'ip_version_error': ip_version,
            'country_list_error': country_list
        }
        return Response(json.dumps(errors, indent=4), 200, content_type='text/plain')
