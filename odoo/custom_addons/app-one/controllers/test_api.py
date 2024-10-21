from odoo import http
from odoo.http import Response

class TestApi(http.Controller):
    @http.route("/api/test", methods=["GET"], type="http", auth="none", csrf=False)
    def test_endpoint(self):
        return Response("Request received successfully 2!", status=200)
