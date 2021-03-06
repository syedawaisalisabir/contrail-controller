#
# Copyright (c) 2016 Juniper Networks, Inc. All rights reserved.
#

import sys

import argparse
from vnc_api.vnc_api import *
from pysandesh.sandesh_base import Sandesh, SandeshSystem
from sandesh_common.vns.constants import HttpPortKubeManager

def parse_args():
    conf_parser = argparse.ArgumentParser(add_help=False)
    conf_parser.add_argument("-c", "--config-file", action='append',
        help="Specify config file", metavar="FILE")
    args, remaining_argv = conf_parser.parse_known_args(sys.argv)

    defaults = {
        'http_server_port': HttpPortKubeManager,
        'worker_id': '0',
        'sandesh_send_rate_limit': SandeshSystem.get_sandesh_send_rate_limit(),
        'collectors': None,
        'logger_class': None,
        'logging_conf': '',
        'log_local': False,
        'log_category': '',
        'use_syslog': False,
        'syslog_facility': Sandesh._DEFAULT_SYSLOG_FACILITY,
        'kube_object_cache': 'True',
    }

    vnc_opts = {
        'rabbit_server': 'localhost',
        'rabbit_port': '5672',
        'rabbit_user': 'guest',
        'rabbit_password': 'guest',
        'rabbit_vhost': None,
        'rabbit_ha_mode': False,
        'rabbit_use_ssl': False,
        'kombu_ssl_version': '',
        'kombu_ssl_keyfile': '',
        'kombu_ssl_certfile': '',
        'kombu_ssl_ca_certs': '',
        'cassandra_user': None,
        'cassandra_password': None,
        'cluster_id': '',
    }
    k8s_opts = {}

    config = ConfigParser.SafeConfigParser()
    if args.config_file:
        config.read(args.config_file)
        if 'VNC' in config.sections():
            vnc_opts.update(dict(config.items("VNC")))
        if 'KUBERNETES' in config.sections():
            k8s_opts.update(dict(config.items("KUBERNETES")))
        if 'DEFAULTS' in config.sections():
            defaults.update(dict(config.items("DEFAULTS")))

    parser = argparse.ArgumentParser(
        parents=[conf_parser],
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    defaults.update(vnc_opts)
    defaults.update(k8s_opts)
    parser.set_defaults(**defaults)
    args = parser.parse_args()

    if type(args.cassandra_server_list) is str:
        args.cassandra_server_list = args.cassandra_server_list.split()
    if type(args.pod_subnets) is str:
        args.pod_subnets = args.pod_subnets.split()
    if type(args.service_subnets) is str:
        args.service_subnets = args.service_subnets.split()
    return args
