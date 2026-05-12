from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests

from django.shortcuts import render
from .models import PM

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def pm_list(request):
    nodes = []
    pm_nodes = PM.objects.all()
    for node in pm_nodes:
        try:
            r = requests.get(f'https://{node.pm_ip_address}:8006/api2/json/nodes/{node.pm_name}/qemu/', headers={
                'Authorization': f'PVEAPIToken={node.pm_token}'}, verify=False)
            r_lxc = requests.get(f'https://{node.pm_ip_address}:8006/api2/json/nodes/{node.pm_name}/lxc/', headers={
                'Authorization': f'PVEAPIToken={node.pm_token}'}, verify=False)

            r_status = requests.get(f'https://{node.pm_ip_address}:8006/api2/json/nodes/{node.pm_name}/status/', headers={
                'Authorization': f'PVEAPIToken={node.pm_token}'}, verify=False)

            r_version = requests.get(f'https://{node.pm_ip_address}:8006/api2/json/nodes/{node.pm_name}/version/',
                                    headers={
                                        'Authorization': f'PVEAPIToken={node.pm_token}'}, verify=False)

            nodes.append({
                'node_name': node.pm_name,
                'node_ip_address': node.pm_ip_address,
                'node_status': r_status.json()['data'],
                'node_version': r_version.json()['data'],
                'vm_list': r.json()['data'],
                'lxc_list': r_lxc.json()['data']
            })
        except:
            pass
    return render(request, "dashboard/pm_list.html", {'nodes': nodes})
