# -*- coding: UTF-8 -*-
from flask import Flask
from celery import Celery

from vlab_inventory_api.lib import const
from vlab_inventory_api.lib.views import InventoryView, HealthView

app = Flask(__name__)
app.celery_app = Celery('inventory', backend='rpc://', broker=const.VLAB_MESSAGE_BROKER)
app.celery_app.conf.broker_heartbeat = 0 #https://github.com/celery/celery/issues/4895

HealthView.register(app)
InventoryView.register(app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
