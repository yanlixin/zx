from flask import Blueprint

blueprint = Blueprint(
    'sys_blueprint',
    __name__,
    url_prefix='/sys',
    template_folder='templates',
    static_folder='static'
)
