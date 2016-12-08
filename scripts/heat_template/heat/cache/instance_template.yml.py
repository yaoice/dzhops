# -*- encoding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1481082994.588855
_enable_loop = True
_template_filename = 'heat/mako_templates/instance_template.yml'
_template_uri = 'instance_template.yml'
_source_encoding = 'ascii'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        stack_name = context.get('stack_name', UNDEFINED)
        vol_size = context.get('vol_size', UNDEFINED)
        image = context.get('image', UNDEFINED)
        instances_nums = context.get('instances_nums', UNDEFINED)
        volume_nums = context.get('volume_nums', UNDEFINED)
        range = context.get('range', UNDEFINED)
        flavor = context.get('flavor', UNDEFINED)
        net = context.get('net', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'heat_template_version: 2015-04-30\n\ndescription: create instances template for cr-dev.\n\nparameters:\n  image:\n    type: string\n    description: OpenStack deploy image.\n    default: ')
        # SOURCE LINE 9
        __M_writer(unicode(image))
        __M_writer(u'\n    constraints:\n    - custom_constraint: glance.image\n      description: >\n        Name or ID of Image for deploy.\n\n  flavor:\n    type: string\n    description: OpenStack deploy flavor.\n    default: ')
        # SOURCE LINE 18
        __M_writer(unicode(flavor))
        __M_writer(u'\n    constraints:\n    - custom_constraint: nova.flavor\n      description: Flavor name for template.\n\n  net:\n    type: string\n    description: OpenStack deploy network.\n    default: ')
        # SOURCE LINE 26
        __M_writer(unicode(net))
        __M_writer(u'\n    constraints:\n    - custom_constraint: neutron.network\n      description: >\n        Network name for template.\n\n  volume_size:\n    type: number\n    description: Instance volume size.\n    default: ')
        # SOURCE LINE 35
        __M_writer(unicode(vol_size))
        __M_writer(u'\n\nresources:\n')
        # SOURCE LINE 38
        for instance_index in range(instances_nums):
            # SOURCE LINE 39
            __M_writer(u'\n  ')
            # SOURCE LINE 40
            __M_writer(unicode(stack_name))
            __M_writer(unicode(instance_index+1))
            __M_writer(u'_volume_os:\n    type: OS::Cinder::Volume\n    properties:\n      name: ')
            # SOURCE LINE 43
            __M_writer(unicode(stack_name))
            __M_writer(unicode(instance_index+1))
            __M_writer(u'_volume_os\n      size: 40\n      image: { get_param: image }\n\n  ')
            # SOURCE LINE 47
            __M_writer(unicode(stack_name))
            __M_writer(unicode(instance_index+1))
            __M_writer(u':\n    type: OS::Nova::Server\n    properties:\n      name: ')
            # SOURCE LINE 50
            __M_writer(unicode(stack_name))
            __M_writer(unicode(instance_index+1))
            __M_writer(u'\n      flavor: { get_param: flavor }\n      block_device_mapping_v2: [{"device_name": /dev/vda, "volume_id": { get_resource: ')
            # SOURCE LINE 52
            __M_writer(unicode(stack_name))
            __M_writer(unicode(instance_index+1))
            __M_writer(u'_volume_os }, "delete_on_termination": true }]\n      networks:\n      - network: { get_param: net }\n\n')
            # SOURCE LINE 56
            for volume_index in range(volume_nums):
                # SOURCE LINE 57
                __M_writer(u'\n  ')
                # SOURCE LINE 58
                __M_writer(unicode(stack_name))
                __M_writer(unicode(instance_index+1))
                __M_writer(u'_volume')
                __M_writer(unicode(volume_index+1))
                __M_writer(u':\n    type: OS::Cinder::Volume\n    properties:\n      name: ')
                # SOURCE LINE 61
                __M_writer(unicode(stack_name))
                __M_writer(unicode(instance_index+1))
                __M_writer(u'_volume')
                __M_writer(unicode(volume_index+1))
                __M_writer(u'\n      size: { get_param: volume_size }\n\n  ')
                # SOURCE LINE 64
                __M_writer(unicode(stack_name))
                __M_writer(unicode(instance_index+1))
                __M_writer(u'_attach_volume')
                __M_writer(unicode(volume_index+1))
                __M_writer(u':\n    type: OS::Cinder::VolumeAttachment\n    depends_on: [ ')
                # SOURCE LINE 66
                __M_writer(unicode(stack_name))
                __M_writer(unicode(instance_index+1))
                __M_writer(u', ')
                __M_writer(unicode(stack_name))
                __M_writer(unicode(instance_index+1))
                __M_writer(u'_volume')
                __M_writer(unicode(volume_index+1))
                __M_writer(u' ]\n    properties:\n      volume_id: { get_resource: ')
                # SOURCE LINE 68
                __M_writer(unicode(stack_name))
                __M_writer(unicode(instance_index+1))
                __M_writer(u'_volume')
                __M_writer(unicode(volume_index+1))
                __M_writer(u' }\n      instance_uuid: { get_resource: ')
                # SOURCE LINE 69
                __M_writer(unicode(stack_name))
                __M_writer(unicode(instance_index+1))
                __M_writer(u' }\n      mountpoint:\n')
        # SOURCE LINE 73
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


