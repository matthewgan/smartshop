from aip import AipFace


def createapiface():

    APP_ID = '11211624'
    API_KEY = 'wo7nEAvyNrK30kWG38rTC1qg'
    SECRET_KEY = 'VcHeSeIARmfXI0TahrgtMyszMsljIKnB'

    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    return client


def detectface(image, imagetype, client):

    options = {}
    options['face_field'] = 'quality'
    res = client.detect(image, imagetype, options)

    errorcode = res.get('error_code')
    if errorcode == 0:
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
        if float(occlusion.get('left_eye')) > 0.4 or float(occlusion.get('right_eye')) > 0.4 or float(
                occlusion.get('nose')) > 0.5 or float(occlusion.get('mouth')) > 0.5 or float(
            occlusion.get('left_cheek')) > 0.6 or float(occlusion.get('left_cheek')) > 0.6 or float(
            occlusion.get('right_cheek')) > 0.6 or float(occlusion.get('chin_contour')) > 0.4:
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
    elif errorcode == 222202:
        print("no face")
        return 104

    return 200


def registerface(image, imagetype, userid, groupid, client):

    options = {}
    options["quality_control"] = "NORMAL"
    options["liveness_control"] = "LOW"
    res = client.addUser(image, imagetype, groupid, userid, options)

    return res


def searchface(image, imagetype, client):

    options= {}
    options["group_id_list"] = "customer"
    res = client.search(image,imagetype,options)
    errorcode = res.get('error_code')
    if errorcode == 0:
        userlist = res.get('result').get('user_list')
        userid = userlist.get('user_id')
        score = userlist.get('score')
        res = {}
        if float(score) > 80:
            res['status'] = 200
            res['userid'] = userid
        else:
            res['status'] = 100
            res['userid'] = userid
            res['score'] =score
    else:
        res['status'] = 101
        res['errorcode'] = errorcode
    return res


def verifyface(image, imagetype, client):

    options = {}
    options['face_fields'] = 'qualities, faceliveness'
    res = client.faceverify(image, imagetype, options)

    return res

    # errorcode = res.get('error_code')
    # if errorcode == 0:
    #     facelist = res.get('result').get('face_list')
    #     quality = facelist[0].get('quality')
    #     occlusion = quality.get('occlusion')
    #     blur = quality.get('blur')
    #     illumination = quality.get('illumination')
    #     completeness = quality.get('completeness')
    #     if float(occlusion.get('left_eye')) > 0.4 or float(occlusion.get('right_eye')) > 0.4 or float(
    #             occlusion.get('nose')) > 0.5 or float(occlusion.get('mouth')) > 0.5 or float(
    #         occlusion.get('left_cheek')) > 0.6 or float(occlusion.get('left_cheek')) > 0.6 or float(
    #         occlusion.get('right_cheek')) > 0.6 or float(occlusion.get('chin_contour')) > 0.4:
    #         print("occlusion error")
    #         return 100
    #     if float(blur) > 0.5:
    #         print("blur error")
    #         return 101
    #     if float(illumination) < 80:
    #         print("illumination error")
    #         return 102
    #     if float(completeness) < 0.3:
    #         print("completeness error")
    #         return 103
    # elif errorcode == 222202:
    #     print("no face")
    #     return 104

    return 200