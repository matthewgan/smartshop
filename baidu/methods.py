from aip import AipFace


def create_aip_client():
    APP_ID = '11211624'
    API_KEY = 'wo7nEAvyNrK30kWG38rTC1qg'
    SECRET_KEY = 'VcHeSeIARmfXI0TahrgtMyszMsljIKnB'
    # change to local test ids
    #APP_ID = '10737221'
    #API_KEY = 'oXOaeclB9LBTTHl80NZqWI0u'
    #SECRET_KEY = '46ynwqBIDuVkEMleFBQ3GAY1ceD0FURS'

    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    return client


def check_occlusion(occlusion):
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


def detect_face(image, image_type, client):

    options = {}
    options['face_field'] = 'quality'
    res = client.detect(image, image_type, options)

    error_code = res.get('error_code')
    if error_code == 0:
        facelist = res.get('result').get('face_list')
        quality = facelist[0].get('quality')
        angle = facelist[0].get('angle')
        yaw = angle.get('yaw')
        pitch = angle.get('pitch')
        roll = angle.get('roll')
        occlusion = quality.get('occlusion')
        blur = quality.get('blur')
        illumination = quality.get('illumination')
        completeness = quality.get('completeness')
        if check_occlusion(occlusion):
            print("occlusion error")
            return 100
        if float(blur) > 0.5:
            print("blur error")
            return 101
        if float(illumination) < 80:
            print("illumination error")
            return 102
        if float(completeness) < 0.3:
            print("completeness error")
            return 103
        if float(yaw) > 20 or float(yaw) < -20 or float(pitch) > 20 or float(pitch) < -20 or float(roll) > 20 or float(roll) < -20:
            return 105
    elif error_code == 222202:
        print("no face")
        return 104
    return 200


def register_face(image, image_type, userid, group_id, client):

    options = {}
    options["quality_control"] = "NORMAL"
    options["liveness_control"] = "LOW"
    res = client.addUser(image, image_type, group_id, userid, options)

    return res


def search_face(image, image_type, client):

    options= {}
    options['group_id_list'] = 'group1'
    res = client.search(image, image_type, options)
    error_code = res.get('error_code')
    if error_code == 0:
        userlist = res.get('result').get('user_list')[0]
        try:
            userid = userlist.get('user_id')
            score = userlist.get('score')
        except:
            userid = 'unkown'
            score = 0
        if float(score) > 80:
            res['status'] = 200
            res['userid'] = userid
        else:
            res['status'] = 100
            res['userid'] = userid
            res['score'] = score
    else:
        res['status'] = 101
        res['errorcode'] = error_code
    return res


def verify_face(image, image_type, client):

    options = {}
    options['face_field'] = 'qualities'
    res = client.faceverify(image, image_type, options)
    print(res)
    error_code = res.get('error_code')
    if error_code == 0:
        facelist = res.get('result').get('face_list')
        quality = facelist[0].get('quality')
        occlusion = quality.get('occlusion')
        blur = quality.get('blur')
        illumination = quality.get('illumination')
        completeness = quality.get('completeness')
        if check_occlusion(occlusion):
            print("occlusion error")
            return 100
        if float(blur) > 0.5:
            print("blur error")
            return 101
        if float(illumination) < 80:
            print("illumination error")
            return 102
        if float(completeness) < 0.3:
            print("completeness error")
            return 103
    elif error_code == 222202:
        print("no face")
        return 104
    return 200
