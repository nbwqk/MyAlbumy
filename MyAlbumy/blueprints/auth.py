from flask import Blueprint,redirect,url_for,flash,render_template
from MyAlbumy.settings import Operations
from MyAlbumy.emails import send_confirm_email
from MyAlbumy.forms.auth import RegisterForm
from flask_login import current_user,login_required
from MyAlbumy.extensions import db
from MyAlbumy.utils import generate_token,validate_token,redirect_back

auth_bp=Blueprint('auth',__name__)

@auth_bp.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form=RegisterForm()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data.lower()
        username=form.username.data
        password=form.password.data
        user=User(name=name,email=email,username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        token=generate_token(user=user,operation='confirm')
        send_confirm_email(user=user,token=token)
        flash('Confirm email sent,check your inbox.','info')
        return redirect(url_for('.login'))
    return render_template('auth/register.html',form=form)

@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if validate_token(user=current_user,token=token,operation=Operations.CONFIRM):
        flash('Account confirmed.','success')
        return redirect(url_for('main.index'))
    else:
        flash('Invalid or expired token.','danger')
        return redirect(url_for('.resend_confirm_email'))

@auth_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    token=generate_token(user=current_user,operation=Operations.CONFIRM)
    send_confirm_email(user=current_user,token=token)
    flash('New email sent,check your inbox.','info')
    return redirect(url_for('main.index'))
