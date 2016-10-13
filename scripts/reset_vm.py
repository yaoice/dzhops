# -*- coding: utf-8 -*-

from multiprocessing import Pool
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

    def __get_server(self, name_or_id=None, filters=None, detailed=False):
        return self.__conn.get_server(name_or_id=name_or_id,
                                      filters=filters,
                                      detailed=detailed)

    def __get_volume(self, name_or_id, filters=None):
        return self.__conn.get_volume(name_or_id=name_or_id,
                                      filters=filters)

    def __get_volumes_by_server(self, server_name_or_id, cache=True):
        server = self.__get_server(server_name_or_id)
        attached_volumes = self.__conn.get_volumes(server, cache=cache)
        deleted_volumes = []
        if attached_volumes:
            for volume in attached_volumes:
                deleted_volume = volume['attachments'][0]['volume_id']
                deleted_volumes.append(deleted_volume)
        return deleted_volumes

    def rebuild_server(self, server, image_id,
                       admin_pass=None,
                       wait=False):
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

    def detach_and_delete_volumes(self, server_name,
                                  wait=True,
                                  timeout=180):
            server = self.__get_server(server_name)
            deleted_volumes = self.__get_volumes_by_server(server_name)
            if deleted_volumes:
                for delete_volume in deleted_volumes:
                    volume = self.__get_volume(delete_volume)
                    print "server {0} detach " \
                        "volume {1} begin.".format(server_name, delete_volume)
                    self.__conn.detach_volume(server=server,
                                              volume=volume,
                                              wait=wait,
                                              timeout=timeout)
                    print "server {0} detach " \
                        "volume {1} end.".format(server_name, delete_volume)

                    print "delete " \
                        "volume {} begin.".format(delete_volume)
                    self.__conn.delete_volume(name_or_id=delete_volume,
                                              wait=wait,
                                              timeout=timeout)
                    print "delete " \
                        "volume {} end.".format(delete_volume)
            else:
                print "server %s has no attached volumes." % (server_name)

    def create_and_attach_volumes(self, server_name,
                                  volume_nums, volume_size,
                                  wait=True, timeout=180):
            server = self.__get_server(server_name)
            for _ in range(volume_nums):
                volume = self.__conn.create_volume(size=volume_size,
                                                   wait=wait,
                                                   timeout=timeout)
                print "create volume {} .".format(volume['id'])
                print "server {0} attach " \
                    "volume {1} begin.".format(server_name, volume['id'])
                self.__conn.attach_volume(server=server,
                                          volume=volume,
                                          device=None,
                                          wait=wait,
                                          timeout=timeout)
                print "server {0} attach " \
                    "volume {1} end.".format(server_name, volume['id'])

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
    client2 = OpenStackAPI(cloud='myfavoriteopenstack')
    image = config_data['rebuild']['image']
    adminPass = config_data['rebuild']['adminPass']
    server_list = config_data['rebuild']['servers']
    volume_nums = config_data['rebuild']['volume']['nums']
    volume_size = config_data['rebuild']['volume']['size']

    if not client.is_exist_image(image):
        print "image %s doesn't exist" % image
        sys.exit(1)

    for server in server_list:
        if not client.is_exist_server(server):
            print "server %s doesn't exist" % server
            sys.exit(1)

    import copy_reg
    import types

    def _reduce_method(meth):
        return (getattr, (meth.__self__, meth.__func__.__name__))

    copy_reg.pickle(types.MethodType, _reduce_method)

    def test(client):
        client.detach_and_delete_volumes(server=server_list[0])
    pool = Pool()
    pool.map(test, [client])
    pool.close()
    pool.join()

#     print('*************detach and delete volume process begin*************')
#     client.detach_and_delete_volumes(server_name=server_list[0])
#     client2.detach_and_delete_volumes(server_name=server_list[1])
#     print('*************detach and delete volume process end*************\n')
# 
#     print('*************rebuild process begin*************')
#     client.rebuild_server(server=server_list[0],
#                           image_id=image,
#                           admin_pass=adminPass,
#                           wait=True)
#     client2.rebuild_server(server=server_list[1],
#                            image_id=image,
#                            admin_pass=adminPass,
#                            wait=True)
#     print('*************rebuild process end*************\n')
# 
#     print('*************create and attach volume process begin*************')
#     client.create_and_attach_volumes(server_name=server_list[0],
#                                      volume_nums=volume_nums,
#                                      volume_size=volume_size)
#     client2.create_and_attach_volumes(server_name=server_list[1],
#                                       volume_nums=volume_nums,
#                                       volume_size=volume_size)
#     print('*************create and attach volume process end*************')
