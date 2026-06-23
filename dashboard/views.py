from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
from django.http import HttpResponse
from django.shortcuts import render

from .models import PM

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_memory_color(percent):
    if percent >= 90:
        return '#dc3545'
    elif percent >= 70:
        return '#ffc107'
    else:
        return '#6ea8fe'


def pm_list(request):
    nodes = []
    pm_nodes = PM.objects.all().order_by('pm_order_number')
    for node in pm_nodes:
        try:
            r = requests.get(f'https://{node.pm_ip_address}:8006/api2/json/nodes/{node.pm_name}/qemu/', headers={
                'Authorization': f'PVEAPIToken={node.pm_token}'}, verify=False)
            r_lxc = requests.get(f'https://{node.pm_ip_address}:8006/api2/json/nodes/{node.pm_name}/lxc/', headers={
                'Authorization': f'PVEAPIToken={node.pm_token}'}, verify=False)

            r_status = requests.get(f'https://{node.pm_ip_address}:8006/api2/json/nodes/{node.pm_name}/status/',
                                    headers={
                                        'Authorization': f'PVEAPIToken={node.pm_token}'}, verify=False)

            r_version = requests.get(f'https://{node.pm_ip_address}:8006/api2/json/nodes/{node.pm_name}/version/',
                                     headers={
                                         'Authorization': f'PVEAPIToken={node.pm_token}'}, verify=False)

            status_data = r_status.json()['data']
            version_data = r_version.json()['data']
            status_data['memory']['persent'] = round(
                status_data['memory']['used'] / status_data['memory']['total'] * 100)

            status_data['memory']['color'] = get_memory_color(status_data['memory']['persent'])

            nodes.append({
                'node_name': node.pm_name,
                'node_ip_address': node.pm_ip_address,
                'node_status': status_data,
                'node_version': version_data,
                'vm_list': sorted(r.json()['data'], key=lambda k: k['vmid']),
                'lxc_list': sorted(r_lxc.json()['data'], key=lambda k: k['vmid'])
            })
        except:
            pass
    return render(request, "dashboard/pm_list.html", {'nodes': nodes})


def health_check(request):
    pm_list = PM.objects.all()
    print(pm_list)
    return HttpResponse("Health status is OK!", status=200)