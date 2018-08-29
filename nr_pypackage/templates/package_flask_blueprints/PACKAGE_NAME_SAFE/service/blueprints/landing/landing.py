"""Landing Blueprint."""
from flask import Blueprint, render_template, url_for
{% if blueprints['auth']['include'] %}
from flask_login import login_required
{% endif %}

landing_handler = Blueprint(name='landing',
                            import_name=__name__,
                            template_folder='templates',
                            static_folder='static')


@landing_handler.route('/', methods=['GET'])
{% if blueprints['auth']['include'] %}
@login_required
{% endif %}
def index():
    """Render landing page."""
    print('>>> landing.index')
    return render_template('navigation_template.html',
                           page_title='{{ package_name }}',
                           page_heading='Landing Page',
                           {% if blueprints['auth']['include'] %}
                           url_for_logout=url_for('auth.logout'),
                           url_for_back=url_for('landing.index'),
                           {% endif %}
                           sub_pages=[
                               {'url': url_for('landing.index'), 'label': "Landing Page"},
                           ])
