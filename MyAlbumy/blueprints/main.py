import os
from flask import Blueprint,request,current_app,render_template,send_from_directory
from flask_login import login_required,current_user
from MyAlbumy.decorators import confirm_required,permission_required
from MyAlbumy.utils import rename_image,resize_image,redirect_back,flash_errors
from MyAlbumy.models import Photo,Comment
from MyAlbumy.extensions import db

main_bp=Blueprint('main',__name__)

@main_bp.route('/uploads/<path:filename>')  #  获取图片的是视图
def get_image(filename):
    return send_from_directory(current_app.config['MYALBUMY_UPLOAD_PATH'],filename)

@main_bp.route('/avatars/<path:filename>')  #  从文件夹获取头像文件的视图
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'],filename)

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

@main_bp.route('/photo/<int:photo_id>')
def show_photo(photo_id):
    photo=Photo.query.get_or_404(photo_id)
    page=request.args.get('page',1,type=int)
    per_page=current_app.config['MYALBUMY_COMMENT_PER_PAGE']
    pagination=Comment.query.with_parent(photo).order_by(Comment.timestamp.asc()).paginate(page,per_page)
    comments=pagination.items

    comment_form=CommentForm()
    description_form=DescriptionForm()
    tag_form=TagForm()

    description_form.description.data=photo.description
    return render_template('main/photo.html',photo=photo,comment_form=comment_form,
                           description_form=description_form,tag_form=tag_form,
                           pagination=pagination,comments=comments)
