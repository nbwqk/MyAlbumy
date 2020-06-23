from MyAlbumy.extensions import db

# relationship table
roles_permissions=db.Table('roles_permissions',
                           db.Column('role_id',db.Integer,db.ForeignKey('role.id')),
                           db.Column('permission_id',db.Integer,db.ForeignKey('permission.id'))
                           )

class Permission(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),unique=True)
    roles=db.relationship('Role',secondary=roles_permissions,back_populates='permissions')

class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),unique=True)
    users=db.relationship('User',back_populates='role')
    permissions=db.relationship('Permission',secondary=roles_permissions,back_populates='roles')

    @staticmethod
    def init_role():
        roles_permissions_map={
            'Locked':['FOLLOW','COLLECT'],
            'User':['FOLLOW','COLLECT','COMMENT','UPLOAD'],
            'Moderator':['FOLLOW','COLLECT','COMMENT','UPLOAD','MODERATE'],
            'Administrator':['FOLLOW','COLLECT','COMMENT','UPLOAD','MODERATE','ADMINISTER']
        }

        for role_name in roles_permissions_map:
            role=Role.query.filter_by(name=role_name).first()
            if role is None:
                role=Role(name=role_name)
                db.session.add(role)
            role.permissions=[]
            for permission_name in roles_permissions_map[role_name]:
                permission=Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission=Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
            db.session.commit()

