from flask import Blueprint

blueprint = Blueprint(
    'zx_blueprint',
    __name__,
    url_prefix='/zx',
    template_folder='templates',
    static_folder='static'
)
