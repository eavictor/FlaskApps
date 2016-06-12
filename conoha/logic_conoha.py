import requests
import json


class ConoHaToken:
    def __init__(self, region='JP', tenant_id=None, tenant_name=None, api_username=None, api_password=None):
        self.region = region
        self.tenant_id = tenant_id
        self.tenant_name = tenant_name
        self.api_username = api_username
        self.api_password = api_password

    def _get_token_url(self):
        if self.region == 'JP':
            return 'https://identity.tyo1.conoha.io/v2.0/tokens'
        elif self.region == 'SG':
            return 'https://identity.sin1.conoha.io/v2.0/tokens'
        elif self.region == 'US':
            return 'https://identity.sjc1.conoha.io/v2.0/tokens'

    def get_token(self):
        """https://www.conoha.jp/docs/identity-post_tokens.html"""
        # information
        token_url = self._get_token_url()
        request_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        request_body = json.dumps({'auth': {'passwordCredentials': {
                        'username': self.api_username, 'password': self.api_password}, 'tenantId': self.tenant_id}})
        # post request, get token
        http = requests.Session()
        http.headers.update(request_headers)
        response = http.post(token_url, data=request_body)
        status_code = response.status_code
        data = response.content.decode('utf-8')
        if status_code == 200:
            json_data = json.loads(data)
            token = json_data['access']['token']['id']
            return json.dumps({'token': token, 'error': None})
        else:
            json_data = json.loads(data)
            message = json_data['error']['message']
            return json.dumps({'token': None, 'error': message})


class ConoHaServer:
    def __init__(self, region='JP', tenant_id=None, token=None, server_id=None):
        self.region = region
        self.tenant_id = tenant_id
        self.token = token
        self.server_id = server_id

    def _get_server_list_url(self):
        if self.region == 'JP':
            return 'https://compute.tyo1.conoha.io/v2/' + self.tenant_id + '/servers/detail'
        elif self.region == 'SG':
            return 'https://compute.sin1.conoha.io/v2/' + self.tenant_id + '/servers/detail'
        elif self.region == 'US':
            return 'https://compute.sjc1.conoha.io/v2/' + self.tenant_id + '/servers/detail'

    def _get_server_action_url(self):
        if self.region == 'JP':
            return 'https://compute.tyo1.conoha.io/v2/' + self.tenant_id + '/servers/' + self.server_id + '/action'
        elif self.region == 'SG':
            return 'https://compute.sin1.conoha.io/v2/' + self.tenant_id + '/servers/' + self.server_id + '/action'
        elif self.region == 'US':
            return 'https://compute.sjc1.conoha.io/v2/' + self.tenant_id + '/servers/' + self.server_id + '/action'

    def get_server_list(self):
        """https://www.conoha.jp/docs/compute-get_vms_detail.html"""
        # information
        vm_list_url = self._get_server_list_url()
        request_headers = {'X-Auth-Token': self.token, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        # get request, get vm list from ConoHa
        http = requests.Session()
        http.headers.update(request_headers)
        response = http.get(vm_list_url)
        status_code = response.status_code
        response_body = response.content.decode('utf-8')
        if status_code == 200:
            json_data = json.loads(response_body)
            server_dict = {}
            for server in json_data['servers']:
                server_dict[server['id']] = server['metadata']['instance_name_tag']
            return json.dumps(server_dict)
        else:
            return 'missing token'

    def start_server(self):
        """https://www.conoha.jp/docs/compute-power_on_vm.html"""
        # information
        start_url = self._get_server_action_url()
        request_headers = {'X-Auth-Token': self.token, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        request_body = json.dumps({'os-start': None})
        # post request, start server
        http = requests.Session()
        http.headers.update(request_headers)
        response = http.post(start_url, request_body)
        status_code = response.status_code
        if status_code == 202:
            return json.dumps({'code': 202, 'message': 'server start command sent'})
        else:
            response_body = response.content.decode('utf-8')
            json_data = json.loads(response_body)
            return json.dumps({'code': status_code, 'message': json_data['conflictingRequest']['message']})

    def shutdown_server(self):
        """https://www.conoha.jp/docs/compute-stop_cleanly_vm.html"""
        # information
        shutdown_url = self._get_server_action_url()
        request_headers = {'X-Auth-Token': self.token, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        request_body = json.dumps({'os-stop': None})
        # post request, tell ConoHa to shutdown server gracefully
        http = requests.Session()
        http.headers.update(request_headers)
        response = http.post(shutdown_url, data=request_body)
        status_code = response.status_code
        if status_code == 202:
            return json.dumps({'code': 202, 'message': 'server shutdown command sent'})
        else:
            response_body = response.content.decode('utf-8')
            json_data = json.loads(response_body)
            return json.dumps({'code': status_code, 'message': json_data['conflictingRequest']['message']})

    def force_stop_server(self):
        """https://www.conoha.jp/docs/compute-stop_forcibly_vm.html"""
        # information
        stop_url = self._get_server_action_url()
        request_headers = {'X-Auth-Token': self.token, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        request_body = json.dumps({'os-stop': {'force_shutdown': True}})
        # post request, force ConoHa to stop specific server
        http = requests.Session()
        http.headers.update(request_headers)
        response = http.post(stop_url, data=request_body)
        status_code = response.status_code
        if status_code == 202:
            return json.dumps({'code': 202, 'message': 'server force stop command sent'})
        else:
            response_body = response.content.decode('utf-8')
            json_data = json.loads(response_body)
            return json.dumps({'code': status_code, 'message': json_data['conflictingRequest']['message']})

    def get_vnc_url(self):
        """https://www.conoha.jp/docs/compute-vnc_console.html"""
        # information
        vnc_request_url = self._get_server_action_url()
        request_headers = {'X-Auth-Token': self.token, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        request_body = json.dumps({'os-getVNCConsole': {'type': 'novnc'}})
        # post request, get vnc_url from conoha
        http = requests.Session()
        http.headers.update(request_headers)
        response = http.post(vnc_request_url, data=request_body)
        status_code = response.status_code
        if status_code == 200:
            response_body = response.content.decode('utf-8')
            json_data = json.loads(response_body)
            return json.dumps({'code': 200, 'vnc_url': json_data['console']['url']})
        else:
            return json.dumps({'code': status_code, 'message': "cannot get current server's VNC url"})




class ConoHaISO:
    def __init__(
            self, region='JP', tenant_id=None, token=None, server_id=None, iso_image_url=None, iso_image_path=None):
        self.region = region
        self.tenant_id = tenant_id
        self.token = token
        self.server_id = server_id
        self.iso_image_url = iso_image_url
        self.iso_image_path = iso_image_path

    def _get_server_action_url(self):
        if self.region == 'JP':
            return 'https://compute.tyo1.conoha.io/v2/' + self.tenant_id + '/servers/' + self.server_id + '/action'
        elif self.region == 'SG':
            return 'https://compute.sin1.conoha.io/v2/' + self.tenant_id + '/servers/' + self.server_id + '/action'
        elif self.region == 'US':
            return 'https://compute.sjc1.conoha.io/v2/' + self.tenant_id + '/servers/' + self.server_id + '/action'

    def _get_check_url(self):
        if self.region == 'JP':
            return 'https://compute.tyo1.conoha.io/v2/' + self.tenant_id + '/servers/' + self.server_id
        elif self.region == 'SG':
            return 'https://compute.sin1.conoha.io/v2/' + self.tenant_id + '/servers/' + self.server_id
        elif self.region == 'US':
            return 'https://compute.sjc1.conoha.io/v2/' + self.tenant_id + '/servers/' + self.server_id

    def _get_image_url(self):
        if self.region == 'JP':
            return 'https://compute.tyo1.conoha.io/v2/' + self.tenant_id + '/iso-images'
        elif self.region == 'SG':
            return 'https://compute.sin1.conoha.io/v2/' + self.tenant_id + '/iso-images'
        elif self.region == 'US':
            return 'https://compute.sjc1.conoha.io/v2/' + self.tenant_id + '/iso-images'

    def _check_mount_status(self):
        """https://www.conoha.jp/docs/compute-get_flavors_detail_specified.html"""
        check_url = self._get_check_url()
        request_headers = {'X-Auth-Token': self.token, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        http = requests.Session()
        http.headers.update(request_headers)
        response = http.get(check_url)
        status_code = response.status_code
        response_body = response.content.decode('utf-8')
        if status_code == 200:
            json_data = json.loads(response_body)
            properties = json.loads(json_data['server']['metadata']['properties'])
            cdrom_path = properties['cdrom_path']
            return cdrom_path
        else:
            return ''

    def push_iso_url(self):
        """https://www.conoha.jp/docs/compute-iso-download-add.html"""
        # information
        image_download_url = self._get_image_url()
        request_headers = {'X-Auth-Token': self.token, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        request_body = json.dumps({'iso-image': {'url': self.iso_image_url}})
        # post request, push iso image download link to ConoHa
        http = requests.Session()
        http.headers.update(request_headers)
        response = http.post(image_download_url, data=request_body)
        status_code = response.status_code
        response_body = response.content.decode('utf-8')
        if status_code == 201:
            return response_body
        else:
            return 'missing token'

    def get_iso_image_list(self):
        """https://www.conoha.jp/docs/compute-iso-list-show.html"""
        # information
        image_list_url = self._get_image_url()
        request_headers = {'X-Auth-Token': self.token, 'Content-Type': 'application/json',
                           'Accept': 'application/json'}
        # get request, get iso image list from ConoHa
        http = requests.Session()
        http.headers.update(request_headers)
        response = http.get(image_list_url)
        status_code = response.status_code
        response_body = response.content.decode('utf-8')
        if status_code == 200:
            json_data = json.loads(response_body)
            images = json_data['iso-images']
            # image_list contains name and id
            iso_image_dict = {}
            for image in images:
                iso_image_dict[image['name']] = image['path']
            return json.dumps(iso_image_dict)
        else:
            return 'missing token'

    def mount_iso(self):
        """https://www.conoha.jp/docs/compute-insert_iso_image.html"""
        cdrom_path = self._check_mount_status()
        if len(cdrom_path) == 0:
            # information
            mount_url = self._get_server_action_url()
            request_headers = {'X-Auth-Token': self.token,
                               'Content-Type': 'application/json', 'Accept': 'application/json'}
            request_body = json.dumps({'mountImage': self.iso_image_path})
            # post request, tell ConoHa to mount selected ISO on selected server
            http = requests.Session()
            http.headers.update(request_headers)
            response = http.post(mount_url, data=request_body)
            status_code = response.status_code
            response_body = response.content.decode('utf-8')
            if status_code == 204:
                cdrom_path2 = self._check_mount_status()
                if len(cdrom_path2) > 0:  # iso is mounted
                    return json.dumps({'code': 204, 'message': 'iso successfully mounted'})
                else:  # iso not mounted
                    return json.dumps({'code': 204, 'message': 'iso mount failed'})
            elif status_code == 409:
                json_data = json.loads(response_body)
                return json.dumps({'code': 409, 'message': json_data['conflictingRequest']['message']})
            else:
                return json.dumps({'code': status_code, 'message': 'something went wrong'})
        else:
            return json.dumps({'code': 204, 'message': 'iso already mounted'})

    def unmount_iso(self):
        cdrom_path = self._check_mount_status()
        if len(cdrom_path) > 0:
            unmount_url = self._get_server_action_url()
            request_headers = {'X-Auth-Token': self.token,
                               'Content-Type': 'application/json', 'Accept': 'application/json'}
            request_body = json.dumps({'unmountImage': ''})
            # post request, unmount iso
            http = requests.Session()
            http.headers.update(request_headers)
            response = http.post(unmount_url, data=request_body)
            status_code = response.status_code
            response_body = response.content.decode('utf-8')
            if status_code == 204:
                cdrom_path2 = self._check_mount_status()
                if len(cdrom_path2) == 0:
                    return json.dumps({'code': 204, 'message': 'iso successfully unmounted'})
                else:
                    return json.dumps({'code': 204, 'message': 'iso unmount failed'})
            elif status_code == 409:
                json_data = json.loads(response_body)
                return json.dumps({'code': 409, 'message': json_data['conflictingRequest']['message']})
            else:
                return json.dumps({'code': status_code, 'message': 'something went wrong'})
        else:
            return json.dumps({'code': 204, 'message': 'iso already unmounted'})
