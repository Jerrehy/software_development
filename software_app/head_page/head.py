from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from software_app.models import CompanyWorker
from software_app.forms import UpdateWorker

head = Blueprint('head', __name__, template_folder="templates")


@head.route('/')
@head.route('/head', methods=['GET'])
def set_profile_page():
    if current_user.is_authenticated:
        that_user = CompanyWorker.get_worker_by_id_with_position(current_user.get_id())
        return render_template('head/head_page.html', that_user=that_user)
    else:
        return render_template('head/head_page.html')


@head.route('/')
@head.route('/new-adders-for-profile', methods=['GET', 'POST'])
@login_required
def update_profile_page():
    worker_update_form = UpdateWorker()
    that_user = CompanyWorker.get_worker_by_id_with_position(current_user.get_id())

    if worker_update_form.submit_update.data:
        if worker_update_form.fio.data:
            fio_update = worker_update_form.fio.data
        else:
            fio_update = that_user.CompanyWorker.fio

        if worker_update_form.phone_number.data:
            phone_number_update = worker_update_form.phone_number.data
        else:
            phone_number_update = that_user.CompanyWorker.phone_number

        if worker_update_form.user_photo.data:
            photo_update = worker_update_form.user_photo.data
        else:
            photo_update = that_user.CompanyWorker.photo

        CompanyWorker.update_company_worker(current_user.get_id(), fio_update, phone_number_update, photo_update)

        return redirect(url_for('head.set_profile_page'))

    return render_template('head/profile_update_page.html', that_user=that_user, worker_update_form=worker_update_form)
