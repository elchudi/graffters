from flask import Flask, request
from flask.ext.restful import reqparse, abort, Api, Resource
from random import randrange

parser = reqparse.RequestParser()
parser.add_argument('base64', type=str)

app = Flask(__name__)
api = Api(app)

markers = {
    'marker1': {'images': ['id_1','id_3']},
    'marker2': {'images': ['id_2']},
}

images = {
    'id_1':'A',
    'id_2':'B',
    'id_3':'C',
}


def abort_if_image_doesnt_exist(image_id):
    if image_id not in images:
        abort(404, message="Image {} doesn't exist".format(image_id))

def abort_if_marker_doesnt_exist(marker_id):
    if marker_id not in markers:
        abort(404, message="Image {} doesn't exist".format(marker_id))

class Image(Resource):
    def get(self, image_id):
        abort_if_image_doesnt_exist(image_id)
        return images[image_id]

    def delete(self, image_id):
        abort_if_image_doesnt_exist(image_id)
        del images[image_id]
        for m in markers:
            if image_id in m['images']:
                m['images'].remove(image_id)
        return '', 204

    def post(self, image_id):
        args = parser.parse_args()
        image_data =  args['base64']
        images[image_id] = image_data
        return image_id, 201

class ImageDelete(Resource):
    def post(self, image_id):
        abort_if_image_doesnt_exist(image_id)
        del images[image_id]
        for m in markers:
            if image_id in m['images']:
                m['images'].remove(image_id)
        return '', 204

class Marker(Resource):
    def get(self, marker_id):
        abort_if_marker_doesnt_exist(marker_id)
        return markers[marker_id]

    def post(self, marker_id):
        args = parser.parse_args()
        image_id = 'id_%d' % (randrange(100000))
        images[image_id] = args['base64']
        if marker_id not in markers.keys():
            markers[marker_id] = {'images':[]}
        markers[marker_id]['images'].append(image_id)
        return image_id, 201

class MarkerDelete(Resource):
    def post(self, marker_id):
        abort_if_marker_doesnt_exist(marker_id)
        for image_id in markers[marker_id]['images']:
            del images[image_id] 
        del markers[marker_id]
        return '', 204

class MarkerList(Resource):
    def get(self):
        return markers.keys()

class ImageList(Resource):
    def get(self):
        return images.keys()

api.add_resource(ImageList, '/images')
api.add_resource(Image, '/images/<string:image_id>')
api.add_resource(ImageDelete, '/images/delete/<string:image_id>')
api.add_resource(MarkerList, '/markers')
api.add_resource(Marker, '/markers/<string:marker_id>')
api.add_resource(MarkerDelete, '/markers/delete/<string:marker_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
