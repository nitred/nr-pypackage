"""{{ current_table_name_lower }} Blueprint."""
from copy import deepcopy
from pprint import pformat, pprint

from flask import (Blueprint, Markup, flash, redirect, render_template,
                   request, session, url_for)
{% if blueprints['auth']['include'] %}
from flask_login import login_required
{% endif %}


from . import utils, handle_list, handle_register, handle_update, handle_deregister


{{ current_table_name_lower }}_handler = Blueprint(
    name='{{ current_table_name_lower }}',
    import_name=__name__,
    template_folder='templates',
    static_folder='static'
)


@{{ current_table_name_lower }}_handler.route('/', methods=['GET'])
{% if blueprints['auth']['include'] %}
@login_required
{% endif %}
def index():
    """Render {{ current_table_name_lower }} page."""
    print('>>> {{ current_table_name_lower }}.index')
    return render_template('navigation_template.html',
                           page_title='Manage {{ current_table_name }}s',
                           page_heading='Manage {{ current_table_name }}s',
                           {% if blueprints['auth']['include'] %}
                           url_for_logout=url_for('auth.logout'),
                           {% endif %}
                           url_for_back=url_for('landing.index'),
                           sub_pages=[
                               {'url': url_for('{{ current_table_name_lower }}.list'), 'label': "list {{ current_table_name_lower }}"},
                               {'url': url_for('{{ current_table_name_lower }}.register'), 'label': "register {{ current_table_name_lower }}"},
                               {'url': url_for('{{ current_table_name_lower }}.update'), 'label': "update {{ current_table_name_lower }}"},
                               {'url': url_for('{{ current_table_name_lower }}.deregister'), 'label': "deregister {{ current_table_name_lower }}"},
                           ])


@{{ current_table_name_lower }}_handler.route('/list', methods=['GET', 'POST'])
{% if blueprints['auth']['include'] %}
@login_required
{% endif %}
def list():
    """list {{ current_table_name_lower }}."""
    print('>>> {{ current_table_name_lower }}.list')
    session_form_data = utils.generate_session_form_data_from_request(request)
    if not session_form_data.submitted:
        df_html = ''
    else:
        df_html = handle_list.get_list_of_{{ current_table_name_lower }}s_as_div()
    return render_template('{{ current_table_name_lower }}/list.html',
                           page_title='{{ current_table_name }}',
                           page_heading='{{ current_table_name }} - List',
                           {% if blueprints['auth']['include'] %}
                           url_for_logout=url_for('auth.logout'),
                           {% endif %}
                           url_for_back=url_for('{{ current_table_name_lower }}.index'),
                           url_for_endpoint=url_for('{{ current_table_name_lower }}.list'),
                           df_html=Markup(df_html),
                           **session_form_data.__dict__)


@{{ current_table_name_lower }}_handler.route('/register', methods=['GET', 'POST'])
{% if blueprints['auth']['include'] %}
@login_required
{% endif %}
def register():
    """register {{ current_table_name_lower }}."""
    print('>>> {{ current_table_name_lower }}.register')
    session_form_data = utils.generate_session_form_data_from_request(request)
    if not session_form_data.submitted:
        df_html = handle_list.get_list_of_{{ current_table_name_lower }}s_as_div()
    else:
        handle_register.register_{{ current_table_name_lower }}(session_form_data)
        df_html = handle_list.get_list_of_{{ current_table_name_lower }}s_as_div()
    return render_template('{{ current_table_name_lower }}/register.html',
                           page_title='{{ current_table_name }}',
                           page_heading='{{ current_table_name }} - Register',
                           {% if blueprints['auth']['include'] %}
                           url_for_logout=url_for('auth.logout'),
                           {% endif %}
                           url_for_back=url_for('{{ current_table_name_lower }}.index'),
                           url_for_endpoint=url_for('{{ current_table_name_lower }}.register'),
                           df_html=Markup(df_html),
                           **session_form_data.__dict__)


@{{ current_table_name_lower }}_handler.route('/update', methods=['GET', 'POST'])
{% if blueprints['auth']['include'] %}
@login_required
{% endif %}
def update():
    """update {{ current_table_name_lower }}."""
    print('>>> {{ current_table_name_lower }}.update')
    session_form_data = utils.generate_session_form_data_from_request(request)
    if not session_form_data or not session_form_data.submitted:
        df_html = handle_list.get_list_of_{{ current_table_name_lower }}s_as_div()
    else:
        handle_update.update_{{ current_table_name_lower }}(session_form_data)
        df_html = handle_list.get_list_of_{{ current_table_name_lower }}s_as_div()
    return render_template('{{ current_table_name_lower }}/update.html',
                           page_title='{{ current_table_name }}',
                           page_heading='{{ current_table_name }} - Update',
                           {% if blueprints['auth']['include'] %}
                           url_for_logout=url_for('auth.logout'),
                           {% endif %}
                           url_for_back=url_for('{{ current_table_name_lower }}.index'),
                           url_for_endpoint=url_for('{{ current_table_name_lower }}.update'),
                           df_html=Markup(df_html),
                           **session_form_data.__dict__)


@{{ current_table_name_lower }}_handler.route('/deregister', methods=['GET', 'POST'])
{% if blueprints['auth']['include'] %}
@login_required
{% endif %}
def deregister():
    """deregister {{ current_table_name_lower }}."""
    print('>>> {{ current_table_name_lower }}.deregister')
    session_form_data = utils.generate_session_form_data_from_request(request)
    if not session_form_data or not session_form_data.submitted:
        df_html = handle_list.get_list_of_{{ current_table_name_lower }}s_as_div()
    else:
        handle_deregister.deregister_{{ current_table_name_lower }}(session_form_data)
        df_html = handle_list.get_list_of_{{ current_table_name_lower }}s_as_div()
    return render_template('{{ current_table_name_lower }}/deregister.html',
                           page_title='{{ current_table_name }}',
                           page_heading='{{ current_table_name }} - Deregister',
                           {% if blueprints['auth']['include'] %}
                           url_for_logout=url_for('auth.logout'),
                           {% endif %}
                           url_for_back=url_for('{{ current_table_name_lower }}.index'),
                           url_for_endpoint=url_for('{{ current_table_name_lower }}.deregister'),
                           df_html=Markup(df_html),
                           **session_form_data.__dict__)
