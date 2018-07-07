# -*- coding: UTF-8 -*-
"""
This module defines all tasks for creating, deleting, listing virtual vLANs.

All responses from a task *MUST* be a dictionary, and *MUST* contain the following
keys:

- ``error``  An error message about bad user input,or None
- ``params`` The parameters provided by the user, or an empty dictionary
- ``content`` The resulting output from running a task, or an empty dictionary

Example:

.. code-block:: python

   # If everything works
   {'error' : None,
    'content' : {'vlan' : 24, 'name': 'bob_FrontEnd'}
    'params' : {'vlan-name' : 'FrontEnd'}
   }
   # If bad params are provided
   {'error' : "Valid parameters are foo, bar, baz",
    'content' : {},
    'params' : {'doh': 'Not a valid param'}
   }

"""
from celery import Celery
from vlab_api_common import get_logger
from vlab_inf_common.vmware import vCenter

from vlab_inventory_api.lib import const

app = Celery('inventory', backend='rpc://', broker=const.VLAB_MESSAGE_BROKER)
logger = get_logger(__name__, loglevel=const.VLAB_INVENTORY_LOG_LEVEL)


@app.task(name='inventory.show')
def show(username):
    """Obtain information about all virtual machines a user owns

    :Returns: Dictionary

    :param username: The owner of the virtual machines
    :type username: String
    """
    resp = {'content' : {}, 'error' : None, 'params' : {}}
    try:
        vcenter= vCenter(host=const.INF_VCENTER_SERVER, user=const.INF_VCENTER_USER,
                         password=const.INF_VCENTER_PASSWORD, verify=const.INF_VCENTER_VERIFY_CERT)
        location = '{}/'.format(const.INF_VCENTER_TOP_LVL_DIR, username)
        folder = vcenter.get_vm_folder(location)
    except FileNotFoundError:
        status = 404
        resp['error'] = 'User {} has no folder; try POSTing to create one.'.format(username)
    else:
        # loop over items in folder, and build up response
        pass
    finally:
        vcenter.close()

@app.task(name='inventory.delete')
def delete(username, everything):
    """Destroy a user's inventory

    :Returns: Dictionary

    :param username: The owner of the inventory to delete
    :type username: String

    :param everything: Optionally destroy all the VMs associated with the user
    :type everything: Boolean
    """
    resp = {'content' : {}, 'error' : None, 'params' : {'everything': everything}}
    try:
        vcenter= vCenter(host=const.INF_VCENTER_SERVER, user=const.INF_VCENTER_USER,
                         password=const.INF_VCENTER_PASSWORD, verify=const.INF_VCENTER_VERIFY_CERT)
        location = '{}/'.format(const.INF_VCENTER_TOP_LVL_DIR, username)
        folder = vcenter.get_vm_folder(location)
        nuke_folder(folder, delete_everything=delete_everything)
    except FolderNotEmptyError:
        resp['error'] = 'To delete a non-empty folder, use param "delete-everything=true"'
    except vim.fault.InvalidState as doh:
        # Some VM isn't powered off...
        resp['error'] = '{}'.format(doh)
    except FileNotFoundError:
        resp['error'] = 'User {} has no folder'.format(username)
    except RuntimeError as doh:
        logger.exception(doh)
        resp['error'] = doh
    except Exception as doh:
        logger.excception(doh)
        resp['error'] = '{}'.format(doh)
    finally:
        vcenter.close()
    return resp


@app.task(name='inventory.create')
def create(username):
    """Make a folder for tacking a user's VM inventory

    :Returns: Dictionary

    :param username: The name of the user to create a folder for
    :type username: String
    """
    resp = {'content' : {}, 'error' : None, 'params' : {}}
    try:
        with vCenter(host=const.INF_VCENTER_SERVER, user=const.INF_VCENTER_USER,
                     password=const.INF_VCENTER_PASSWORD, verify=const.INF_VCENTER_VERIFY_CERT) as vcenter:
            location = '{}/'.format(const.INF_VCENTER_TOP_LVL_DIR, username)
            vcenter.create_vm_folder(location)
    except Exception as doh:
        logger.exception(doh)
        resp['error'] = '{}'.format(doh)


def nuke_folder(folder, delete_everything=False, timeout=300):
    """Delete a user's folder

    :Returns: None

    :param folder: **Required** The user's folder to delete
    :type folder: vim.Folder

    :param delete_everything: Optionally delete "all the things" in a single call
    :type delete_everything: Boolean

    :param timeout: How long to wait for the operation to complete
    :type timeout: Integer
    """
    if delete_everything:
        task = folder.UnregisterAndDestroy()
    else:
        task = folder.Destroy()
    for _ in range(timeout):
        if task.info.state == 'success':
            break
        else:
            sleep(1)
    else:
        error = 'Task failed to complete within {} seconds'.format(timeout)
        raise RuntimeError(error)
