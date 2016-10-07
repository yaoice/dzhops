# -*- coding: utf-8 -*-

from shade import openstack_cloud
import sys
import yaml


class OpenStackAPI(object):
    def __init__(self, cloud):
        self.__cloud = cloud
        self.__conn = self.__get_conn()

    def __get_conn(self):
        conn = openstack_cloud(cloud=self.__cloud)
        return conn

    def is_exist_server(self, name_or_id=None):
        return True if self.__conn.get_server(name_or_id) else False

    def is_exist_image(self, name_or_id=None):
        return True if self.__conn.get_image(name_or_id) else False

    def __get_server_id(self, name_or_id):
        return self.__conn.get_server_id(name_or_id)

    def parallel_rebuild_server(self, servers, image_id,
                                admin_pass=None,
                                wait=False):
        for server in servers:
            print "server {0} rebuild " \
                "with image {1} begin.".format(server, image_id)
            server_id = self.__get_server_id(server)
            self.__conn.rebuild_server(server_id,
                                       image_id,
                                       admin_pass,
                                       wait)
            print "server {0} rebuild " \
                "with image {1} end.".format(server,
                                             image_id)

    @staticmethod
    def load_config(config_file):
        with open(config_file, 'r') as f:
            return yaml.load(f)


if __name__ == '__main__':
    config_data = OpenStackAPI.load_config('clouds.yml')
    if not config_data:
        print "No config data has been loaded"
        sys.exit(1)

    client = OpenStackAPI(cloud='myfavoriteopenstack')
    image = config_data['rebuild']['image']
    adminPass = config_data['rebuild']['adminPass']
    server_list = config_data['rebuild']['servers']

    if not client.is_exist_image(image):
        print "image %s doesn't exist" % image
        sys.exit(1)

    for server in server_list:
        if not client.is_exist_server(server):
            print "server %s doesn't exist" % server
            sys.exit(1)

    print('*************rebuild process begin*************')
    client.parallel_rebuild_server(servers=server_list,
                                   image_id=image,
                                   admin_pass=adminPass,
                                   wait=True)
    print('*************rebuild process end*************')
