# coding: utf-8
from datetime import datetime
import os
import re
import sha

from mongoengine import *

from .tasks import *


SOCIAL_CHOICES = (('GH', 'GitHub'), ('F', 'Facebook'), ('G', 'Google'), ('T', 'Twitter'), ('FF', 'FriendFinder'), )

COUNTRIES = 'ad,ae,af,ag,ai,al,am,an,ao,ar,as,at,au,aw,az,ba,bb,bd,be,bf,bg,bh,bi,bj,bm,bn,bo,br,bs,bt,bv,bw,by,bz,ca,catalonia,cd,cf,cg,ch,ci,ck,cl,cm,cn,co,cr,cu,cv,cw,cy,cz,de,dj,dk,dm,do,dz,ec,ee,eg,eh,en,er,es,et,eu,fi,fj,fk,fm,fo,fr,ga,gb,gd,ge,gf,gg,gh,gi,gl,gm,gn,gp,gq,gr,gs,gt,gu,gw,gy,hk,hm,hn,hr,ht,hu,ic,id,ie,il,im,in,io,iq,ir,is,it,je,jm,jo,jp,ke,kg,kh,ki,km,kn,kp,kr,ku,kw,ky,kz,la,lb,lc,li,lk,lr,ls,lt,lu,lv,ly,ma,mc,md,me,mg,mh,mk,ml,mm,mn,mo,mp,mq,mr,ms,mt,mu,mv,mw,mx,my,mz,na,nc,ne,nf,ng,ni,nl,no,np,nr,nu,nz,om,pa,pe,pf,pg,ph,pk,pl,pm,pn,pr,ps,pt,pw,py,qa,re,ro,rs,ru,rw,sa,sb,sc,scotland,sd,se,sg,sh,si,sk,sl,sm,sn,so,somaliland,sr,ss,st,sv,sx,sy,sz,tc,td,tf,tg,th,tj,tk,tl,tm,tn,to,tr,tt,tv,tw,tz,ua,ug,um,us,uy,uz,va,vc,ve,vg,vi,vn,vu,wa,wf,ws,ye,yt,za,zanzibar,zm,zw'.split(',')
COUNTRY_CHOICES = tuple([(c, c) for c in COUNTRIES])

class User(Document):
    email = EmailField(required=True, max_length=1024)
    password = StringField(max_length=1024) # social login
    secret_key = StringField(required=True, max_length=1024)
    admin = BooleanField()

    username = StringField(required=False)
    social = StringField(required=False, choices=SOCIAL_CHOICES, max_length=2)
    country = StringField(required=False, choices=COUNTRY_CHOICES)
    gender = StringField()
    registered_on = DateTimeField(required=True, default=datetime.utcnow)

    @classmethod
    def authenticate(cls, email, password):
        if password:
            pw = User.encrypt_password(password)
            return User.objects(email=email, password=pw)
        return []

    @classmethod
    def encrypt_password(cls, password):
        return sha.sha(password).hexdigest()

    @classmethod
    def generate_secret_key(cls):
        return os.urandom(24).encode('base64').strip()

    @classmethod
    def is_valid_password(cls, password):
        if not password: return False
        if len(password) < 10 or len(password) > 1024: return False
        if re.match('.*\s+', password): return False
        if not re.match('.*[a-z]+', password): return False
        if not re.match('.*[A-Z]+', password): return False
        if not re.match('.*[0-9]+', password): return False
        if not re.match('.*[!@#$%&*()_+-={}|/?;:,.<>\\\[\]]+', password): return False
        return True

    def pre_save(self, encrypt_pass=False):
        created = self.id is None
        if encrypt_pass:
            self.validate_password() # validate only for non-social logins
            self.password = User.encrypt_password(self.password)
        if not self.secret_key:
            self.secret_key = User.generate_secret_key()

    def save(self, encrypt_pass=False, **kwargs):
        self.pre_save(encrypt_pass=encrypt_pass)
        super(User, self).save(**kwargs)

    def get_or_create(encrypt_pass=False, write_concern=None, auto_save=True, *q_objs, **query):
        self.pre_save(encrypt_pass=encrypt_pass)
        return super(User, self).get_or_create(write_concern=write_concern, auto_save=auto_save, *q_objs, **query)

    def validate_password(self): # it must be called before encrypting the password
        if not User.is_valid_password(self.password):
            errors = {}
            print(self.password)
            msg = "Invalid password. It must have at least 10 chars, 1 lower case, 1 upper case, 1 number, 1 symbol."
            errors['password'] = ValidationError(msg, field_name='password')
            raise ValidationError('ValidationError', errors=errors)

    def change_password(self, current_password, new_password):
        errors = {}
        if User.encrypt_password(current_password) != self.password:
            errors['password'] = ValidationError('The current password is wrong', field_name='password')
        if current_password == new_password:
            errors['password'] = ValidationError('New password must not be the same as the old one', field_name='password')
        if errors:
            raise ValidationError('ValidationError', errors=errors)
        self.password = new_password
        self.save(encrypt_pass=True)

    def update_country(self, ip):
        import connect_redis # import to connect to redis
        from .tasks import update_country
        queue = connect_redis.default_queue()
        queue.enqueue(update_country, self.id, ip)

    def add_contact_to_propagation(self, fb_id=None, tags=None, languages=None):
        import connect_redis # import to connect to redis
        from apps.utils.tasks import add_contact_to_propagation
        queue = connect_redis.default_queue()
        queue.enqueue(add_contact_to_propagation, email=self.email, fb_id=fb_id, tags=tags, languages=languages)

    def send_email(self, subject, message):
        send_email(self.email, subject, message)


# Migration
# users = User.objects.filter(secret_key=None)
# for u in users:
#     u.save()
