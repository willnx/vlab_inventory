# -*- coding: UTF-8 -*-
"""
This module defines the API for tracking your vLab inventory
"""
from flask_classy import request
from vlab_inf_common.views import TaskView
from vlab_inf_common.vmware import vCenter, vim
from vlab_api_common import describe, get_logger, requires


from vlab_inventory_api.lib import const


logger = get_logger(__name__, loglevel=const.VLAB_INVENTORY_LOG_LEVEL)


class InventoryView(TaskView):
    """API end point for working with user folders"""
    route_base = '/api/1/inf/inventory'
    GET_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                  "description": "Return all the virtual machines a user owns"
                 }
    DELETE_ARGS_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
    	                  "type": "object",
                          "description": "Destroy the user's inventory record"
                          "properties": {
                             "everything": {
                                "type": "boolean",
                                "description": "Delete all virtual machines, along with the user's record"
                             }
                          }
                         }
    POST_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                   "description": "Create a new record so a user can track their inventory of virtual machines"
                 }

    @describe(get=GET_SCHEMA, delete_args=DELETE_ARGS_SCHEMA, post=POST_SCHEMA)
    @requires(verify=False)
    def get(self):
        """Get all the virtual machines within a folder"""
        username = kwargs['token']['username']
        resp = {'user' : username}
        task = current_app.celery_app.send_task('inventory.show', [username])
        resp['content'] = {'task-id': task.id}
        return ujson.dumps(resp), 200

    @requires(verify=False)
    def post(self, *args, **kwargs):
        """Create a user's folder"""
        username = kwargs['token']['username']
        resp = {"user" : username}
        task = current_app.celerey_app.send_task('inventory.create', [username])
        resp['content'] = {'task-id': task.id}
        return ujson.dumps(resp), 200

    @requires(verify=False)
    def delete(self, *args, **kwargs):
        """Delete a user's folder"""
        username = kwargs['token']['username']
        resp = {'user' : username}
        delete_everything = request.args.get('delete-everything', False)
        task = current_app.celery_app.send_task('inventory.delete', [username, delete_everything])
        resp['content'] = {'task-id': task.id}
        return ujson.dumps(resp), 200
