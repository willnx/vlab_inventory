# -*- coding: UTF-8 -*-
"""
This module defines the API for tracking your vLab inventory
"""
import ujson
from flask import current_app
from flask_classy import request, Response
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
    DELETE_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                     "description": "Destroy the user's inventory record"
                    }
    POST_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                   "description": "Create a new record so a user can track their inventory of virtual machines"
                  }

    @describe(get=GET_SCHEMA, delete=DELETE_SCHEMA, post=POST_SCHEMA)
    @requires(verify=const.VLAB_VERIFY_TOKEN, version=2)
    def get(self, *args, **kwargs):
        """Get all the virtual machines within a folder"""
        username = kwargs['token']['username']
        resp_data = {'user' : username}
        task = current_app.celery_app.send_task('inventory.show', [username])
        resp_data['content'] = {'task-id': task.id}
        resp = Response(ujson.dumps(resp_data))
        resp.status_code = 202
        resp.headers.add('Link', '<{0}{1}/task/{2}>; rel=status'.format(const.VLAB_URL, self.route_base, task.id))
        return resp

    @requires(verify=const.VLAB_VERIFY_TOKEN, version=2)
    def post(self, *args, **kwargs):
        """Create a user's folder"""
        username = kwargs['token']['username']
        resp_data = {"user" : username}
        txn_id = request.headers.get('X-REQUEST-ID', 'noId')
        task = current_app.celery_app.send_task('inventory.create', [username, txn_id])
        resp_data['content'] = {'task-id': task.id}
        resp = Response(ujson.dumps(resp_data))
        resp.status_code = 202
        resp.headers.add('Link', '<{0}{1}/task/{2}>; rel=status'.format(const.VLAB_URL, self.route_base, task.id))
        return resp

    @requires(verify=const.VLAB_VERIFY_TOKEN, version=2)
    def delete(self, *args, **kwargs):
        """Delete a user's folder"""
        username = kwargs['token']['username']
        resp_data = {'user' : username}
        task = current_app.celery_app.send_task('inventory.delete', [username])
        resp_data['content'] = {'task-id': task.id}
        resp = Response(ujson.dumps(resp_data))
        resp.status_code = 202
        resp.headers.add('Link', '<{0}{1}/task/{2}>; rel=status'.format(const.VLAB_URL, self.route_base, task.id))
        return resp
