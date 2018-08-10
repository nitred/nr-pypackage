"""Landing Blueprint."""
from flask import Blueprint, render_template, url_for

landing_handler = Blueprint(name='landing',
                            import_name=__name__,
                            template_folder='templates',
                            static_folder='static')


@landing_handler.route('/', methods=['GET'])
def index():
    """Render landing page."""
    print('>>> landing.index')
    return render_template('navigation_template.html',
                           page_title='{{ package_name }}',
                           page_heading='Landing Page',
                           sub_pages=[
                               {'url': url_for('landing.index'), 'label': "Landing Page"},
                           ])
