import time

from kubernetes import client, config
from kubernetes.client.api import core_v1_api
from kubernetes.client.api.apps_v1_api import AppsV1Api

config.load_kube_config()

v1 = client.CoreV1Api()
core_v1 = core_v1_api.CoreV1Api()
apps_v1 = AppsV1Api()


def get_request_url(uuid: str, base_url="http://192.168.49.2"):
    request_url = None
    ret = v1.list_service_for_all_namespaces()
    for i in ret.items:
        selector = i.spec.selector
        if selector is not None:
            namespace = i.metadata.namespace
            port = i.spec.ports[0].node_port
            if namespace == uuid:
                request_url = f"{base_url}:{port}"
    return request_url


def create_app(namespace_name: str, github_link: str, target_file: str, app_name="application", replicas: int = 1):
    cd_path = github_link.split("/")[-1].replace(".git", "")
    arg_string = f"git clone {github_link} && cd {cd_path} && pip install -r requirements.txt && python {target_file}"
    manifest_namespace = {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata":
            {
                "name": f"{namespace_name}"
            }
    }
    core_v1.create_namespace(body=manifest_namespace)
    manifest_service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata":
            {
                "name": f"{app_name}",
                "namespace": f"{namespace_name}"
            },
        "spec":
            {
                "type": "NodePort",
                "selector":
                    {
                        "app": f"{app_name}"
                    },
                "ports": [
                    {
                        "protocol": "TCP",
                        "port": 8080,
                        "targetPort": 8080
                    }
                ]
            }
    }
    core_v1.create_namespaced_service(namespace_name, body=manifest_service)
    manifest_deploy = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata":
            {
                "name": f"{app_name}",
                "namespace": f"{namespace_name}",
                "labels":
                    {
                        "app": f"{app_name}",
                    }
            },
        "spec":
            {
                "replicas": replicas,
                "selector":
                    {
                        "matchLabels":
                            {
                                "app": f"{app_name}"
                            }
                    },
                "template":
                    {
                        "metadata":
                            {
                                "labels":
                                    {
                                        "app": f"{app_name}"
                                    }
                            },
                        "spec":
                            {
                                "containers": [
                                    {
                                        "name": "app",
                                        "image": "python:3.8.13-bullseye",
                                        "ports": [
                                            {
                                                "containerPort": 8080
                                            },
                                        ],
                                        "command": ["/bin/sh", "-c"],
                                        "args": [arg_string]
                                    }
                                ]
                            }
                    }
            }
    }
    apps_v1.create_namespaced_deployment(namespace_name, body=manifest_deploy)

    time.sleep(2)
    return get_request_url(namespace_name)


def delete_app(namespace_name):
    core_v1.delete_namespace(namespace_name)


