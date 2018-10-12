"""Landing Blueprint."""
from nr_common.configreader import read_config
from flask import Blueprint, render_template, url_for, current_app, flash, redirect
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
                               {% for table_name, table_details in blueprints['database']['tables'].items() %}
                               {'url': url_for('{{ table_details.table_name_lower }}.index'), 'label': "Manage {{ table_details.table_name }}s"},
                               {% endfor %}
                               {'url': url_for('landing.update_config'), 'label': "update config"},
                           ])


@landing_handler.route('/update_config', methods=['GET'])
{% if blueprints['auth']['include'] %}
@login_required
{% endif %}
def update_config():
    """Update app config."""
    config_filename = current_app.config['app_config']['config_filename']
    new_config = read_config(config_filename)
    new_config['config_filename'] = config_filename
    current_app.config['app_config'] = new_config
    flash("Updated config from: {}.".format(config_filename))

    return redirect(url_for('landing.index'))
