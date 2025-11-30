from flask import Blueprint, request, jsonify
from Functons. store import addstore
storeStatus=('open','closed','maintenance')

stores =Blueprint("Theaters",__name__)

#adds a store                                           not tested
@stores.route("/store/add",methods=["POST"]) 
def addStores():
    data=request.get_json()

    if not data :
        return jsonify({"error":"Missing JSON body"}),400
    
    name=data.get("name")
    location=data.get("location")
    status= data.get("status", "open")
    
    try:
        name=name.lower().strip()
        location.lower().strip()
        status.lower().strip()
    except ValueError:
        return jsonify({"error":"not valid input types"}),400
    
    if status not in storeStatus:
        return jsonify({"error":f"cant add this status {status}"}),400
    
    val=addstore(name,location,status)

    if val is None:
        return jsonify({"message":"store Alredy exists"}),202  
    if val:
        return jsonify({"message":"store has been aded."}),201
    else:
        return jsonify({"error":"Failed to add store"}),409