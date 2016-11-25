# -*- coding: utf-8 -*-

from mako import exceptions
from mako.lookup import TemplateLookup
from multiprocessing import Pool
from shade import exc
from shade import openstack_cloud
import os
import sys
import time
import xlrd
import yaml


class OpenStackAPI(object):
    def __init__(self, cloud):
        self.__cloud = cloud
        self.__conn = self.__get_conn()

    def __get_conn(self):
        conn = openstack_cloud(cloud=self.__cloud)
        return conn

    def __get_param_from_excel(self, path):
        param_list = []
        data = None
        try:
            data = xlrd.open_workbook(path)
        except Exception, e:
            print str(e)

        def check_sheet_available(i):
            if i.cell_value(8, 3) != "" and i.cell_value(12, 1) != "":
                return True

        for i in data.sheets():
            if check_sheet_available(i):
                param_dict = {}
                image = i.cell_value(13, 1)
                flavor = i.cell_value(12, 1)
                net = i.cell_value(8, 1)
                vol_size = i.cell_value(14, 1)
                volume_nums = i.cell_value(14, 3)
                instances_nums = i.cell_value(8, 3)
                stack_name = i.cell_value(9, 1)
                param_dict['image'] = str(image)
                param_dict['flavor'] = str(flavor)
                param_dict['net'] = str(net)
                param_dict['vol_size'] = int(vol_size)
                param_dict['volume_nums'] = int(volume_nums)
                param_dict['instances_nums'] = int(instances_nums)
                param_dict['stack_name'] = str(stack_name)
                param_list.append(param_dict)
        return param_list

    def __generate_heat_template(self, path):
        templates_dir = 'heat/mako_templates'
        templates_cache = 'heat/cache'
        output_templates_dir = 'heat/templates'

        templates_list = []
        params_list = self.__get_param_from_excel(path)

        env = TemplateLookup(directories=[templates_dir],
                             module_directory=templates_cache,
                             output_encoding='utf-8',
                             encoding_errors='replace')
        tpl_list = os.listdir(templates_dir)
        for t in tpl_list:
            try:
                tpl = env.get_template(t)
                for param_dict in params_list:
                    output = tpl.render(**param_dict)
                    template_name = (time.strftime('%y-%m-%d') +
                                     '_' +
                                     param_dict.get('stack_name') +
                                     '_' +
                                     os.path.basename(t))

                    template_path = os.path.join(output_templates_dir,
                                                 template_name)
                    if os.path.exists(output_templates_dir) == False:
                        os.makedirs(output_templates_dir)
                    with open(template_path, 'w') as out:
                        out.write(output)
                    templates_list.append((param_dict.get('stack_name'),
                                           template_path))
            except:
                print (exceptions.text_error_template().render())

        return templates_list

    def generate_heat_template(self, path):
        return self.__generate_heat_template(path)

    def create_stack(
            self, name,
            template_file=None, template_url=None,
            template_object=None, files=None,
            rollback=True,
            wait=False, timeout=3600,
            environment_files=None,
            **parameters):
        print "*****  begin create heat stack {}  *****".format(name)
        self.__conn.create_stack(name=name,
                                 template_file=template_file,
                                 template_url=template_url,
                                 template_object=template_object,
                                 files=files,
                                 rollback=rollback,
                                 wait=wait,
                                 timeout=timeout,
                                 environment_files=environment_files,
                                 **parameters)
        print "*****  finish create heat stack {}  *****".format(name)

    @staticmethod
    def load_config(config_file):
        with open(config_file, 'r') as f:
            return yaml.load(f)


def paralley_create_stack(cloud,
                          name,
                          tempalte_file,
                          wait=True):
    client = OpenStackAPI(cloud=cloud)
    try:
        client.create_stack(name=name,
                            template_file=tempalte_file,
                            wait=wait)
    except exc.OpenStackCloudException as e:
        print "create heat stack {0} failed, error msg: {1}".format(name, e)


if __name__ == '__main__':
    config_data = OpenStackAPI.load_config('clouds.yml')
    if not config_data:
        print "No config data has been loaded"
        sys.exit(1)

    cloud = 'myfavoriteopenstack'
    client = OpenStackAPI(cloud=cloud)
    templates_list = client.generate_heat_template(
                                                config_data.get('excel_name')
                                                )

    pool = Pool(20)
    for name, template_file in templates_list:
        pool.apply_async(paralley_create_stack,
                         args=(cloud,
                               name,
                               template_file,
                               ))
    pool.close()
    pool.join()
