from flask import Blueprint

blueprint = Blueprint(
    'pm_blueprint',
    __name__,
    url_prefix='/pm',
    template_folder='templates',
    static_folder='static'
)
