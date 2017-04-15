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







@app.route('/api/server/delete/<int:sever_id>', methods=['DELETE'])
@requires_auth
def delete_server(server_id):
  server = Server.query.filter(Server.id == server_id)
  db.session.delete(server)
  db.session.commit()
  return  jsonify({}), 204

@app.route('/api/models/<int:model_id>', methods=['PUT'])
@requires_auth
def update_model(model_id):
  user = get_user(request)
  try:
    model = user.models.filter(Model.id == model_id).first()

    if 'name' in request.get_json():
      setattr(model, 'name', request.get_json()['name'])

    for field in model.fields:
      update_field = next((f for f in request.get_json()['fields'] if field.id == f['id']), None)

      if update_field:
        setattr(field, 'name', update_field['name']) if 'name' in update_field else None
        setattr(field, 'data_type', update_field['data_type']) if 'data_type' in update_field else None
        setattr(field, 'parent_node', update_field['parent_node']) if 'parent_node' in update_field else None
      else:
        db.session.delete(field)

    for field in request.get_json()['fields']:
      new_field = next((None for f in model.fields if f.id == field['id']), field)

      if new_field:
        new_field = Field(name=field['name'], model=model, data_type=field['data_type'])
        new_field.parent_node = field['parent_node'] if 'parent_node' in field else None
        model.fields.append(new_field)

    db.session.add(model)
    db.session.commit()
    return jsonify(ModelSchema().dump(model).data), 200
  except sqlalchemy.exc.SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({"error": str(e)}), 401

@app.route('/api/models/<int:model_id>', methods=['DELETE'])
@requires_auth
def delete_model(model_id):
  user = get_user(request)
  try:
    model = user.models.filter(Model.id == model_id).first()
    fields = model.fields.all()
    db.session.delete(model)
    [db.session.delete(field) for field in fields]
    db.session.commit()
    return jsonify({}), 204
  except sqlalchemy.exc.SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({"error": str(e)}), 401

# GENERATOR =================================================================

@app.route('/api/generator/string', methods=['GET'])
@requires_auth
def get_random_string():
  return jsonify({ "string": get_random_string() }), 200

@app.route('/api/generator/integer', methods=['GET'])
@requires_auth
def get_random_integer():
  """To do: Allow url parameters to determine high/low for random integer. """
  return jsonify({ "integer": get_random_integer() }), 200

@app.route('/api/generator/float', methods=['GET'])
@requires_auth
def get_random_float():
  """To do: Allow url parameters to determine high/low for random float. """
  return jsonify({ "float": get_random_float() }), 200

@app.route('/api/generator/boolean', methods=['GET'])
@requires_auth
def get_random_boolean():
  return jsonify({ "boolean": get_random_boolean() }), 200

# CUSTOM DATA TYPES [NOT IMPLEMENTED] =======================================

@app.route('/api/custom-data-types', methods=['GET'])
@requires_auth
def get_custom_data_types():
  user = get_user(request)
  cdts = CustomDataType.query.filter_by(user = user).all()
  return jsonify(CustomDataTypeSchema().dump(cdts, many=True).data), 200

@app.route('/api/custom-data-types/<int:custom_data_type_id>', methods=['GET'])
@requires_auth
def get_custom_data_type(custom_data_type_id):
  user = get_user(request)
  cdt = user.custom_data_types.filter(CustomDataType.id == custom_data_type_id)
  return jsonify(CustomDataTypeSchema().dump(cdt).data), 200

@app.route('/api/custom-data-types', methods=['POST'])
@requires_auth
def create_custom_data_type():
  user = get_user(request)
  try:
    cdt = CustomDataType(name=request.get_json()['name'], user=user)
    db.session.add(cdt)
    db.session.commit()
    query = CustomDataType.query.get(cdt.id)
    return jsonify(CustomDataTypeSchema().dump(query).data), 201
  except sqlalchemy.exc.SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({"error": str(e)}), 401

@app.route('/api/custom-data-types/<int:custom_data_type_id>', methods=['PUT'])
@requires_auth
def update_custom_data_type(custom_data_type_id):
  user = get_user(request)
  try:
    cdt = user.custom_data_types.filter(CustomDataType.id == custom_data_type_id).first()
    for key, value in request.get_json().items():
      setattr(cdt, key, value)
    db.session.add(cdt)
    db.session.commit()
    return jsonify(CustomDataTypeSchema().dump(cdt).data, 200)
  except sqlalchemy.exc.SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({"error": str(e)}), 401

@app.route('/api/custom-data-types/<int:custom_data_type_id>', methods=['DELETE'])
@requires_auth
def delete_custom_data_type(custom_data_type_id):
  user = get_user(request)
  try:
    cdt = user.custom_data_types.filter(CustomDataType.id == custom_data_type_id).first()
    db.session.delete(cdt)
    db.session.commit()
    return jsonify({}), 204
  except sqlalchemy.exc.SQLAlchemyError as e:
    db.session.rollback()
return jsonify({"error": str(e)}), 401