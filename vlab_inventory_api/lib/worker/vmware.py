# -*- coding: UTF-8 -*-
"""Business logic for backend worker tasks"""
import time
import random
import os.path
from celery.utils.log import get_task_logger
from vlab_inf_common.vmware import vCenter, vim, virtual_machine, consume_task

from vlab_inventory_api.lib import const


logger = get_task_logger(__name__)
logger.setLevel(const.VLAB_INVENTORY_LOG_LEVEL.upper())


def show_inventory(username):
    """Return some basic information about all VMs a user owns

    :Returns: Dictionary

    :param username: The name of the user to create a folder for
    :type username: String
    """
    with vCenter(host=const.INF_VCENTER_SERVER, user=const.INF_VCENTER_USER,\
                 password=const.INF_VCENTER_PASSWORD) as vcenter:
        folder = vcenter.get_by_name(name=username, vimtype=vim.Folder)
        vms = {}
        for entity in folder.childEntity:
            info = virtual_machine.get_info(vcenter, entity)
            vms[entity.name] = info
    return vms


def create_inventory(username):
    """Create a folder in vCenter for storing user's VMs

    :Returns: None

    :param username: The name of the user to create a folder for
    :type username: String
    """
    location = '{}/{}'.format(const.INF_VCENTER_TOP_LVL_DIR, username)
    with vCenter(host=const.INF_VCENTER_SERVER, user=const.INF_VCENTER_USER,
                 password=const.INF_VCENTER_PASSWORD) as vcenter:
        vcenter.create_vm_folder(location)


def delete_inventory(username):
    """Destroy a user's inventory

    :Returns: Dictionary

    :param username: The owner of the inventory to delete
    :type username: String

    :param everything: Optionally destroy all the VMs associated with the user
    :type everything: Boolean
    """
    error = None
    vcenter = vCenter(host=const.INF_VCENTER_SERVER, user=const.INF_VCENTER_USER,
                     password=const.INF_VCENTER_PASSWORD)
    try:
        folder = vcenter.get_by_name(name=username, vimtype=vim.Folder)
        nuke_folder(folder)
    except vim.fault.InvalidState as doh:
        # Some VM isn't powered off...
        error = '{}'.format(doh.msg)
    except FileNotFoundError:
        error = 'User {} has no folder'.format(username)
    except RuntimeError as doh:
        error = '{}'.format(doh)
        logger.error(error)
    finally:
        vcenter.close()
    return error


def nuke_folder(folder, timeout=300):
    """Delete a user's folder

    :Returns: None

    :param folder: **Required** The user's folder to delete
    :type folder: vim.Folder

    :param timeout: How long to wait for the operation to complete
    :type timeout: Integer
    """
    task = folder.Destroy()
    consume_task(task, timeout=timeout)
