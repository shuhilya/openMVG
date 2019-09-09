from __future__ import print_function
import json
import codecs

WIDTH = 4032
HEIGHT = 3024

def load_json(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data

def dump_json(path, json_data):
    with open(path, 'wb') as f:
        json.dump(json_data, codecs.getwriter('utf-8')(f), indent=4, ensure_ascii=False)

def change_camera_params_in_json(src_path, dst_path, key=None, debug=True):
    """
    key = "MATLAB" or "ARKIT"
    """
    def get_camera_params(key, k):
        params = {
            "width": int(WIDTH / k),
            "height": int(HEIGHT / k)
        }
        if key == "MATLAB":
            params["focal_length"] = 3192.4 / k
            params["principal_point"] = [2033.8 / k, 1703.9 / k]
            params["disto_k3"] = [0.0218, -0.0222, 0.0]
            params["disto_t2"] = [0.0062, 0.0135]
        elif key == "ARKIT":
            params["focal_length"] = 3123.74000244 / k
            params["principal_point"] = [1974.82813110 / k, 1524.24611206 / k]
            params["disto_k3"] = [0.0, 0.0, 0.0]
            params["disto_t2"] = [0.0, 0.0]
        else:
            exit("Unknown key in get_camera_params(): key must be \"MATLAB\", \"ARKIT\" or None")
        return params

    def insert_dist_coeff(json_data, key, debug=True):
        ptr_wrapper_data = json_data["intrinsics"][0]["value"]["ptr_wrapper"]["data"]
        resize_k = WIDTH / ptr_wrapper_data["width"]
        new_params = get_camera_params(key, resize_k)
        if debug:
            for key in ptr_wrapper_data.keys():
                print(key + ":", ptr_wrapper_data[key], "-->", new_params[key])
            print("disto_t2:", [0.0, 0.0], "-->", new_params["disto_t2"])
        json_data["intrinsics"][0]["value"]["ptr_wrapper"]["data"] = new_params

    if key is None:
        return
    json_data = load_json(src_path)
    insert_dist_coeff(json_data, key, debug)
    dump_json(dst_path, json_data)


if __name__ == "__main__":
    change_camera_params_in_json("sfm_data_full.json", "sfm_data_test.json", "ARKIT",debug=True)
