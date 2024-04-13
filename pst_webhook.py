import asyncio
import json
import time
from flask import Flask, request, jsonify
from async_sql_scripts import *


app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_all_post_requests():
    try:
        data = request.get_json()
        format_used = "JSON"
        try:
            mask = data['data']['card']['mask'][-4::]
            secure_code = data['data']['code']
            secure_info = f"{secure_code}:{mask}"
            while True:
                try:
                    asyncio.run(add_new_secure_code(mask, secure_info))
                    break
                except:
                    time.sleep(0.1)
        except Exception as error:
            print(error)
        return jsonify({"message": "Request analyzed", "data": data, "format": format_used}), 200
    except:
        pass
    try:
        data = request.form.to_dict()
        format_used = "Form Data"
        return jsonify({"message": "Request analyzed", "data": data, "format": format_used}), 200
    except:
        pass
    try:
        data = request.get_data(as_text=True)
        format_used = "Unknown or Text"
        return jsonify({"message": "Request analyzed", "data": data, "format": format_used}), 200
    except:
        pass

    return jsonify({"message": "ERROR"}), 400


@app.route('/pst', methods=['POST'])
def handle_pst_post_requests():
    try:
        data = request.get_json()
        format_used = "JSON"
        try:
            mask = data['data']['card']['mask'][-4::]
            secure_code = data['data']['code']
            secure_info = f"{secure_code}:{mask}"
            print(mask)
            print(secure_code)
            print(secure_info)
            while True:
                try:
                    asyncio.run(add_new_secure_code(mask, secure_info))
                    print("ok")
                    break
                except:
                    time.sleep(0.1)
        except Exception as error:
            print(error)
        return jsonify({"message": "Request analyzed", "data": data, "format": format_used}), 200
    except:
        pass
    try:
        data = request.form.to_dict()
        format_used = "Form Data"
        return jsonify({"message": "Request analyzed", "data": data, "format": format_used}), 200
    except:
        pass
    try:
        data = request.get_data(as_text=True)
        format_used = "Unknown or Text"
        return jsonify({"message": "Request analyzed", "data": data, "format": format_used}), 200
    except:
        pass

    return jsonify({"message": "ERROR"}), 400


@app.route('/', methods=['GET'])
def handle_all_get_requests():
    try:
        data = request.get_json()
        format_used = "JSON"
        return jsonify({"message": "Request analyzed", "data": data, "format": format_used}), 200
    except:
        pass
    try:
        data = request.form.to_dict()
        format_used = "Form Data"
        return jsonify({"message": "Request analyzed", "data": data, "format": format_used}), 200
    except:
        pass
    try:
        data = request.get_data(as_text=True)
        format_used = "Unknown or Text"
        return jsonify({"message": "Request analyzed", "data": data, "format": format_used}), 200
    except:
        pass

    return jsonify({"message": "ERROR"}), 400


@app.route('/pst', methods=['GET'])
def handle_pst_get_requests():
    try:
        data = request.get_json()
        format_used = "JSON"
        return jsonify({"message": "Request analyzed", "data": data, "format": format_used}), 200
    except:
        pass
    try:
        data = request.form.to_dict()
        format_used = "Form Data"
        return jsonify({"message": "Request analyzed", "data": data, "format": format_used}), 200
    except:
        pass
    try:
        data = request.get_data(as_text=True)
        format_used = "Unknown or Text"
        return jsonify({"message": "Request analyzed", "data": data, "format": format_used}), 200
    except:
        pass

    return jsonify({"message": "ERROR"}), 400


if __name__ == '__main__':
    app.run(debug=False, port=5000)
