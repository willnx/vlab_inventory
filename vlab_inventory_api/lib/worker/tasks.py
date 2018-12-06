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
from vlab_api_common import get_task_logger
from vlab_inf_common.vmware import vCenter

from vlab_inventory_api.lib import const
from vlab_inventory_api.lib.worker import vmware

app = Celery('inventory', backend='rpc://', broker=const.VLAB_MESSAGE_BROKER)


@app.task(name='inventory.show', bind=True)
def show(self, username, txn_id):
    """Obtain information about all virtual machines a user owns

    :Returns: Dictionary

    :param username: The owner of the virtual machines
    :type username: String

    :param txn_id: A unique string supplied by the client to track the call through logs
    :type txn_id: String
    """
    logger = get_task_logger(txn_id=txn_id, task_id=self.request.id, loglevel=const.VLAB_INVENTORY_LOG_LEVEL.upper())
    resp = {'content' : {}, 'error' : None, 'params' : {}}
    logger.info('Task Starting')
    try:
        info = vmware.show_inventory(username)
    except FileNotFoundError:
        status = 404
        resp['error'] = 'User {} has no folder; try POSTing to create one.'.format(username)
    else:
        resp['content'] = info
    logger.info('Task Complete')
    return resp


@app.task(name='inventory.delete', bind=True)
def delete(self, username, txn_id):
    """Destroy a user's inventory

    :Returns: Dictionary

    :param username: The owner of the inventory to delete
    :type username: String

    :param everything: Optionally destroy all the VMs associated with the user
    :type everything: Boolean

    :param txn_id: A unique string supplied by the client to track the call through logs
    :type txn_id: String
    """
    logger = get_task_logger(txn_id=txn_id, task_id=self.request.id, loglevel=const.VLAB_INVENTORY_LOG_LEVEL.upper())
    resp = {'content' : {}, 'error' : None, 'params' : {}}
    logger.info('Task Starting')
    resp['error'] = vmware.delete_inventory(username)
    logger.info('Task Complete')
    return resp


@app.task(name='inventory.create', bind=True)
def create(self, username, txn_id):
    """Make a folder for tacking a user's VM inventory

    :Returns: Dictionary

    :param username: The name of the user to create a folder for
    :type username: String

    :param txn_id: A unique string supplied by the client to track the call through logs
    :type txn_id: String
    """
    logger = get_task_logger(txn_id=txn_id, task_id=self.request.id, loglevel=const.VLAB_INVENTORY_LOG_LEVEL.upper())
    resp = {'content' : {}, 'error' : None, 'params' : {}}
    logger.info('Task Starting')
    vmware.create_inventory(username, logger)
    logger.info('Task Complete')
    return resp
