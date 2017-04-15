from flask import jsonify, request, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
from flask_login import login_required, current_user
from app import app, db
from app.models import User, Server, ServerSchema, DataCenterServer, DataCenter, ModelSchema
import sqlalchemy.exc


limiter = Limiter(
  app,
  key_func=get_remote_address,
)

def serverCount(datacenter_id):
    return DataCenterServer.query.count(DataCenterServer.data_center_id == datacenter_id)

def getIds(param1, array):
    ans = []
    for item in array:
        ans.append(item[param1])
    return ans


def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.authorization
    if not auth:
      if current_user.is_authenticated:
        g.user = current_user
        return f(*args, **kwargs)
      else:
        return needs_authentication()
    if user is None or user.password is not user.verify_password(auth.password):
      return needs_authentication()
    g.user = user
    return f(*args, **kwargs)
  return decorated

def needs_authentication():
  return jsonify({"error": "Could not authenticate user."}), 401

def check_auth(username, password):
  user = User.query.filter_by(email = username).first()
  return user and user.verify_password(password)

def get_user(request):
  if request.authorization:
    return User.query.filter_by(email = request.authorization.username).first()
  elif current_user.is_authenticated:
    return current_user

# MODELS ============================================================

@app.route('/api/datacenters', methods=['GET'])
@requires_auth
def get_datacenters():
  datacenters = DataCenter.query.all()
  return jsonify(ModelSchema().dump(datacenters, many=True).data), 200

@app.route('/api/datacenters/<int:servers>/<name>', methods=['GET'])
@requires_auth
def search_datacenters(servers,name):
  datacenters = DataCenter.query.filter(DataCenter.name == name and serverCount(DataCenter.id) == servers)
  return jsonify(ModelSchema().dump(datacenters).data), 200

@app.route('/api/datacenter/delete/<int:data_center_id>', methods=['DELETE'])
@requires_auth
def delete_data_center(data_center_id):
  data_center_servers = DataCenterServer.query.filter(DataCenterServer.data_center_id == data_center_id)
  server_ids = getIds('server_id',data_center_servers)
  for server_id in server_ids:
      delete_server(server_id)
  data_center = DataCenter.query.filter(DataCenter.id == data_center_id)
  db.session.delete(data_center)
  db.session.commit()
  return  jsonify({}), 204

@app.route('/api/datacenter/servers/<int:data_center_id>', methods=['GET'])
@requires_auth
def get_servers_in_data_center(data_center_id):
    data_center_servers = DataCenterServer.query.filter(DataCenterServer.data_center_id == data_center_id)
    server_ids = getIds('server_id', data_center_servers)
    servers = []
    for server_id in server_ids:
        server = Server.query.filter(Server.id == server_id)
        servers.append(server)
    return jsonify({ModelSchema().dump(servers).data}),200

@app.route('/api/datacenter/update/<int:data_center_id>', methods=['POST'])
@requires_auth
def update_data_center(data_center_id):
    db.session.query(DataCenter).filter(DataCenter.id == data_center_id).update(request.get_json())
    db.session.commit()
    updated_data_center = DataCenter.query.filter(DataCenter.id == data_center_id)
    return  jsonify({ModelSchema().dump(updated_data_center).data}),200


@app.route('/api/datacenter/create', methods=['POST'])
@requires_auth
def create_date_center():
    db.session.add(request.get_json())
    db.session.commit()
    return jsonify({}),200

@app.route('/api/servers', methods=['GET'])
@requires_auth
def get_servers_list():
    servers = Server.query.all()
    return jsonify({ModelSchema().dump(servers).data}),200

@app.route('/api/server/search/<maker>/<name>', methods=['GET'])
@requires_auth
def serach_servers(maker,name):
    servers = Server.query.filter(Server.name == name and Server.maker == maker)
    return jsonify({ModelSchema().dump(servers).data}),200

@app.route('/api/server/update/<int:id>', methods=['POST'])
@requires_auth
def update_server(id):
    db.session.query(Server).filter(Server.id == id).update(request.get_json())
    db.session.commit()
    updated_server = Server.query.filter(Server.id == id)
    return jsonify({ModelSchema().dump(updated_server).data}),200

@app.route('/api/server/create', methods=['POST'])
@requires_auth
def create_server():
    db.session.add(request.get_json())
    db.session.commit()
    return jsonify({}),200


@app.route('/api/server/delete/<int:sever_id>', methods=['DELETE'])
@requires_auth
def delete_server(server_id):
  server = Server.query.filter(Server.id == server_id)
  db.session.delete(server)
  db.session.commit()
  return  jsonify({}), 204

