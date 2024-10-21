from odoo import http
import json
from odoo.http import request, Response


class PropertyApi(http.Controller):

    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        print(vals)
        res = request.env['property'].sudo().create(vals)
        print(res)

        return Response("Property Created Successfully", status=200)
