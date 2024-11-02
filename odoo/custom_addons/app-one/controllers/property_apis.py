# from cgi import parse_qs
from urllib.parse import parse_qs

from odoo import http
import json
from odoo.http import request, Response


class PropertyApi(http.Controller):

    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        print(vals)
        if not vals.get('name'):
            return request.make_json_response({
                "message": "Name is Required",
            }, status=400)
        res = request.env['property'].sudo().create(vals)
        if res:
            print(res)
            return Response("Property Created Successfully", status=200)

        return Response("An error occur while creating property", status=403)

    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            print(property_id)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            if not property_id:
                raise Exception()
            property_id.write(vals)
            print(property_id.garden_area)
            return request.make_json_response({
                "message": "Property Has Been Updated Successfully!",
                "id": property_id.id,
                "name": property_id.name,
            }, status=200)

        except Exception as error:
            return request.make_json_response({
                "message": "---Error occured while updating record ---",
            }, status=400)


    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                raise Exception()
            property_id.unlink()
            return request.make_json_response({
                "message": "Property Has Been Deleted Successfully!",
            }, status=200)

        except Exception as error:
            return request.make_json_response({
<<<<<<< HEAD
                "message": "---Error occured while Deleting record ---",
=======
                "message": "---Error occured while Deleting record  ---",
>>>>>>> ef18c291270151c001a3a52b3d6551fe0b3b67e7
            }, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self,property_id):
        try:
            property = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property:
                return request.make_json_response({
                    "error":"ID Doesn't Exist! "
                }, status=400)
            return request.make_json_response({
                'id': property.id,
                'name': property.name,
                'description': property.description,
                'postcode': property.postcode,
                'date_availability': property.date_availability,
                'expected_selling_date': property.expected_selling_date,
                'expected_price': property.expected_price,
                'selling_price': property.selling_price,
                'bedrooms': property.bedrooms,
                'living_area': property.living_area,
                'facades': property.facades,
                'garage': property.garage,
                'garden': property.garden,
                'garden_area': property.garden_area,
                'garden_orientation': property.garden_orientation,
                'state': property.state
            })
        except Exception as error:
            return request.make_json_response({
                "error": "Error occured while searching!"
            },status=404)


    @http.route("/v1/property", methods=["GET"], type="http", auth="none", csrf=False)
    def get_properties(self):
        # Search for all properties
        params = parse_qs(request.httprequest.query_string.decode('utf-8'))
        # properties = request.env['property'].sudo().search([])
        if params:
            properties = request.env['property'].sudo().search([('state', '=', params.get('state')[0])])
        else:
            properties = request.env['property'].sudo().search([])

        # Prepare the property data in a list of dictionaries
        property_data = []
        for property in properties:
            property_data.append({
                'id': property.id,
                'name': property.name,
                'description': property.description,
                'postcode': property.postcode,
                # 'date_availability': property.date_availability,
                # 'expected_selling_date': property.expected_selling_date,
                'expected_price': property.expected_price,
                'selling_price': property.selling_price,
                'bedrooms': property.bedrooms,
                'living_area': property.living_area,
                'facades': property.facades,
                'garage': property.garage,
                'garden': property.garden,
                'garden_area': property.garden_area,
                'garden_orientation': property.garden_orientation,
                'state': property.state
            })

        # Return the data as a JSON response
        return Response(json.dumps(property_data), content_type='application/json', status=200)
