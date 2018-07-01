from aip import AipFace
from .models import FaceRecord
import os.path
import base64


def create_aip_client():
    app_id = '11211624'
    api_key = 'wo7nEAvyNrK30kWG38rTC1qg'
    secret_key = 'VcHeSeIARmfXI0TahrgtMyszMsljIKnB'

    client = AipFace(app_id, api_key, secret_key)
    return client


def load_image_to_base64(file_path):
    if os.path.exists(file_path):
        file = open(file_path, 'rb')
        img64 = base64.b64encode(file.read()).decode('UTF-8')
        file.close()
        return img64
    else:
        return "DoesNotExist"


def check_occlusion_error(occlusion):
    if float(occlusion.get('left_eye')) > 0.4 \
            or float(occlusion.get('right_eye')) > 0.4 \
            or float(occlusion.get('nose')) > 0.5 \
            or float(occlusion.get('mouth')) > 0.5 \
            or float(occlusion.get('left_cheek')) > 0.6 \
            or float(occlusion.get('left_cheek')) > 0.6 \
            or float(occlusion.get('right_cheek')) > 0.6 \
            or float(occlusion.get('chin_contour')) > 0.4:
        return True
    else:
        return False


def check_orientation_error(yaw, pitch, roll):
    if float(yaw) > 20 or float(yaw) < -20 \
            or float(pitch) > 20 or float(pitch) < -20 \
            or float(roll) > 20 or float(roll) < -20:
        return True
    else:
        return False


def check_blur_error(blur):
    if float(blur) > 0.5:
        return True
    else:
        return False


def check_illumination_error(illumination):
    if float(illumination) < 80:
        return True
    else:
        return False


def check_completeness_error(completeness):
    if float(completeness) < 0.3:
        return True
    else:
        return False


def check_size_error(width, height):
    if width < 80 or height < 80:
        return True
    else:
        return False


def check_liveness_error(face_liveness, thresholds):
    frr = thresholds.get('frr_1e-4')
    if face_liveness < frr:
        return True
    else:
        return False


def detect_face(image, image_type, client):
    options = {}
    options['face_field'] = 'quality'
    options['max_face_num'] = 1
    result = client.detect(image, image_type, options)

    error_code = result.get('error_code')
    if error_code == 0:
        # check normal result
        face_list = result.get('result').get('face_list')
        face_token = face_list[0].get('face_token')
        quality = face_list[0].get('quality')
        angle = face_list[0].get('angle')
        location = face_list[0].get('location')
        width = location.get('width')
        height = location.get('height')
        yaw = angle.get('yaw')
        pitch = angle.get('pitch')
        roll = angle.get('roll')
        occlusion = quality.get('occlusion')
        blur = quality.get('blur')
        illumination = quality.get('illumination')
        completeness = quality.get('completeness')
        if check_blur_error(blur):
            return {'error_code': 101, 'error_msg': "blur error"}
        elif check_illumination_error(illumination):
            return {'error_code': 102, 'error_msg': "illumination error"}
        elif check_completeness_error(completeness):
            return {'error_code': 103, 'error_msg': "completeness error"}
        elif check_occlusion_error(occlusion):
            return {'error_code': 104, 'error_msg': "occlusion error"}
        elif check_orientation_error(yaw, pitch, roll):
            return {'error_code': 105, 'error_msg': "orientation error"}
        elif check_size_error(width, height):
            return {'error_code': 106, 'error_msg': "face too small error"}
        else:
            return {'error_code': 0, 'face_token': face_token}
    else:
        """
        {
            'error_code': code
            'error_msg' : detail string about the error
        }
        """
        return result


def register_face(image, image_type, user_id, user_info, group_id, client):
    options = {}
    options["user_info"] = user_info
    options["quality_control"] = "NORMAL"
    options["liveness_control"] = "LOW"
    result = client.addUser(image, image_type, group_id, user_id, options)

    # face_token = result.get('face_token')
    # face = FaceRecord(token=face_token, user_id=user_id, group_id=group_id, operation='register')
    face = FaceRecord(user_id=user_id, group_id=group_id, operation='register')
    face.save()

    return {'error_code': 0}


def update_face(image, image_type, user_id, user_info, group_id, client):
    options = {}
    options["quality_control"] = "NORMAL"
    options["liveness_control"] = "LOW"
    result = client.addUser(image, image_type, group_id, user_id, user_info, options)

    face_token = result.get('face_token')
    face = FaceRecord(token=face_token, user_id=user_id, user_info=user_info, group_id=group_id, operation='update')
    face.save()

    return {'error_code': 0}


def delete_face(user_id, group_id, face_token, client):
    result = client.faceDelete(user_id, group_id, face_token)
    face = FaceRecord(token=face_token, user_id=user_id, group_id=group_id, operation='deleteFace')
    face.save()

    error_code = result.get('error_code')
    if error_code == 0:
        return {'error_code': 0}
    else:
        return result


def query_user_info(user_id, group_id, client):
    """获取人脸库中某个用户的信息(user_info信息和用户所属的组)。"""
    result = client.getUser(user_id, group_id)
    user_list = result.get('user_list')
    return user_list


def get_face_list(user_id, group_id, client):
    """用于获取一个用户的全部人脸列表 token, ctime。"""
    result = client.faceGetlist(user_id, group_id)
    face_list = result.get('face_list')
    return face_list


def get_group_list(group_id, client):
    """用于查询指定用户组中的用户列表。"""
    result = client.getGroupUsers(group_id)
    user_id_list = result.get('user_id_list')
    return user_id_list


def copy_user_between_group(user_id, src_group_id, dst_group_id, client):
    options = {}
    options["src_group_id"] = src_group_id
    options["dst_group_id"] = dst_group_id
    result = client.userCopy(user_id, options)
    error_code = result.get('error_code')
    if error_code == 0:
        face = FaceRecord(user_id=user_id, group_id=(src_group_id + ' to ' + dst_group_id),
                          operation='copy')
        face.save()
        return {'error_code': 0}
    else:
        return result


def delete_user(group_id, user_id, client):
    result = client.deleteUser(group_id, user_id)
    error_code = result.get('error_code')
    if error_code == 0:
        face = FaceRecord(user_id=user_id, group_id=group_id,
                          operation='deleteUser')
        face.save()
        return {'error_code': 0}
    else:
        return result


def add_group(group_id, client):
    result = client.groupAdd(group_id)
    error_code = result.get('error_code')
    if error_code == 0:
        return {'error_code': 0}
    else:
        return result


def delete_group(group_id, client):
    result = client.groupDelete(group_id)
    error_code = result.get('error_code')
    if error_code == 0:
        return {'error_code': 0}
    else:
        return


def query_group_list(client):
    result = client.getGroupList()
    group_id_list = result.get('group_id_list')
    return group_id_list


def search_face(image, image_type, group_id_list, client):
    options = {}
    # options["quality_control"] = "NORMAL"
    # options["liveness_control"] = "LOW"
    options['group_id_list'] = group_id_list
    # options["user_id"] = "233451" # fill user_id to make search to identify
    # options["max_user_num"] = 1
    result = client.search(image, image_type, options)
    error_code = result.get('error_code')
    if error_code == 0:
        try:
            user_list = result.get('result').get('user_list')[0]
            user_id = user_list.get('user_id')
            score = user_list.get('score')
        except:
            user_id = '0'
            score = 0
        if float(score) > 80:
            return {'error_code': 0,
                    'user_id': user_id,
                    'score': score}
        else:
            return {'error_code': 101,
                    'user_id': user_id,
                    'score': score}
    else:
        return result


def verify_face(image, image_type, client):
    options = {}
    options['face_field'] = 'quality'
    result = client.faceverify(image, image_type)

    face_liveness = result.get('face_liveness')
    thresholds = result.get('thresholds')
    face_list = result.get('result').get('face_list')
    quality = face_list[0].get('quality')
    angle = face_list[0].get('angle')
    location = face_list[0].get('location')
    width = location.get('width')
    height = location.get('height')
    yaw = angle.get('yaw')
    pitch = angle.get('pitch')
    roll = angle.get('roll')
    occlusion = quality.get('occlusion')
    blur = quality.get('blur')
    illumination = quality.get('illumination')
    completeness = quality.get('completeness')

    if check_blur_error(blur):
        return {'error_code': 101, 'error_msg': "blur error"}
    elif check_illumination_error(illumination):
        return {'error_code': 102, 'error_msg': "illumination error"}
    elif check_completeness_error(completeness):
        return {'error_code': 103, 'error_msg': "completeness error"}
    elif check_occlusion_error(occlusion):
        return {'error_code': 104, 'error_msg': "occlusion error"}
    elif check_orientation_error(yaw, pitch, roll):
        return {'error_code': 105, 'error_msg': "orientation error"}
    elif check_size_error(width, height):
        return {'error_code': 106, 'error_msg': "face too small error"}
    elif check_liveness_error(face_liveness, thresholds):
        return {'error_code': 107, 'error_msg': "liveness error"}
    else:
        return {'error_code': 0}

