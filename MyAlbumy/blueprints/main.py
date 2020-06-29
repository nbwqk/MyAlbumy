import os
from flask import Blueprint,request,current_app,render_template
from flask_login import login_required,current_user
from MyAlbumy.decorators import confirm_required,permission_required
from MyAlbumy.utils import rename_image,resize_image,redirect_back,flash_errors
from MyAlbumy.models import Photo
from MyAlbumy.extensions import db

main_bp=Blueprint('main',__name__)

@main_bp.route('/upload',methods=['GET','POST'])
@login_required # 验证登录状态
@confirm_required   # 验证确认状态
@permission_required('UPLOAD')  # 验证权限
def upload():
    if request.method=='POST' and 'file' in request.files:
        f=request.files.get('file')
        filename=rename_image(f.filename)
        f.save(os.path.join(current_app.config['MYALBUMY_UPLOAD_PAHT'],filename))
        filename_s=resize_image(f,filename,current_app.config['MYALBUMY_PHOTO_SIZE']['small'])
        filename_m=resize_image(f,filename,current_app.config['MYALBUMY_PHOTO_SIZE']['medium'])
        photo=Photo(
            filename=filename,
            filename_s=filename_s,
            filename_m=filename_m,
            author=current_user._get_current_object()
        )
        db.session.add(photo)
        db.session.commit()
    return render_template('main/upload.html')
