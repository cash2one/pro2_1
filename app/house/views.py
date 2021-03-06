from flask import render_template,url_for,redirect,request,flash
from . import house
from app import db
from app.models import House,Owner,User
import json
from .forms import OwnerForm
from datetime import datetime,date
@house.route('/house_message/',methods=['POST','GET'])
def house_message():
    queryall=House.query.all()
    houseid=request.args.get('houseid')
    ownername=request.args.get('ownername')
    if (houseid != '' and houseid is not None) or (ownername is not None and ownername != ''):
        if houseid == '' or houseid is  None:
            querys = House.query.filter_by(owner_ownername=ownername)
        elif ownername == '' or ownername is None:
            querys = House.query.filter_by(houseid=houseid)
        else:
            querys = House.query.filter_by(houseid=houseid,owner_ownername=ownername)
    else:
        querys = House.query.all()
    return render_template('house/house_message.html',querys=querys,queryall=queryall)

@house.route('/house_message/house_add',methods=['POST','GET'])
def house_add():
    owner_querys=Owner.query.all()
    return render_template('house/add_house.html',owner_querys=owner_querys)

@house.route('/house_message/add/post',methods=['POST','GET'])
def house_add_post():
    q_house_exit = House.query.filter_by(houseid=request.form.get('add_houseid')).first()
    if q_house_exit is not None:
        flash("该房产已存在")
        return redirect(url_for('house.house_add'))
    else:
        house=House(houseid=request.form.get('add_houseid'),owner_ownername=request.form.get('add_ownername'),
                    housetype=request.form.get('add_housetype'),housestatus=request.form.get('add_housestatus'),
                    housespace=request.form.get('add_housespace'),housecommunity=request.form.get('add_housecommunity'),
                    houseaddress=request.form.get('add_houseaddress'),houseremark=request.form.get('add_houseremark'))
        if house.owner_ownername !="" and house.owner_ownername is not None:
            q_owner = Owner.query.filter_by(ownername=house.owner_ownername).first()
            #判断业主是否已有房产，同时，业主为空的不能算
            if q_owner is not None and q_owner !='':
               flash("一个业主只能拥有一套房产")
               return redirect(url_for('house.house_add'))
            q_owner.ownerstatus=house.housestatus
            db.session.add(q_owner)
            db.session.commit()
        if request.form.get('add_houseyears') !='' and request.form.get('add_houseyears') is not None:
            house.houseyears = request.form.get('add_houseyears')
        db.session.add(house)
        db.session.commit()
    return redirect(url_for('house.house_message'))


@house.route('/house_message/delete/<string:house_id>',methods=['POST','GET'])
def house_delete(house_id):
    res = {
        "status": 1,
        "message": "success"
    }
    house = House.query.filter_by(houseid=house_id).first()
    q_owner = Owner.query.filter_by(house_houseid=house.houseid).first()
    if q_owner !='' and q_owner is not None:
        db.session.delete(q_owner)
    db.session.delete(house)
    db.session.commit()
    return json.dumps(res)

@house.route('/house_message/detail/<string:houseid>',methods=['POST','GET'])
def house_detail(houseid):
    query=House.query.filter_by(houseid=houseid).first_or_404()
    query_owner=Owner.query.all()
    return render_template('house/house_detail.html',query=query,query_owner=query_owner)

@house.route('/house_message/detail/post/',methods=['POST','GET'])
def house_detail_post():
    a=request.form.get('detail_houseid')
    house = House.query.filter_by(houseid=a).first()
    house.owner_ownername=request.form.get('detail_ownername')
    house.housetype=request.form.get('detail_housetype')
    house.housestatus=request.form.get('detail_housestatus')
    house.housespace=request.form.get('detail_housespace')
    house.houseyears=request.form.get('detail_houseyears')
    house.housecommunity=request.form.get('detail_housecommunity')
    house.houseaddress=request.form.get('detail_houseaddress')
    house.houseremark=request.form.get('detail_houseremark')
    if house.owner_ownername != "" and house.owner_ownername is not None:
        q_owner = Owner.query.filter_by(ownername=house.owner_ownername).first()
        q_owner.ownerstatus = house.housestatus
        db.session.add(q_owner)
        db.session.commit()
    db.session.add(house)
    db.session.commit()
    return redirect(url_for('house.house_message'))

#####################################################################

@house.route('/house_owner/',methods=['POST','GET'])
def house_owner():
    owner_querys=Owner.query.all()
    houseid = request.args.get('houseid')
    ownername = request.args.get('ownername')
    #owner_querys=Owner.query.all()
    if (houseid != '' and houseid is not None) or (ownername is not None and ownername != ''):
        if houseid == '' or houseid is None:
            querys = Owner.query.filter_by(ownername=ownername)
        elif ownername == '' or ownername is None:
            querys = Owner.query.filter_by(house_houseid=houseid)
        else:
            querys = Owner.query.filter_by(house_houseid=houseid, ownername=ownername)
    else:
        querys = Owner.query.all()
    return render_template('house/house_owner.html',querys=querys,owner_querys=owner_querys)

@house.route('/house_owner/owner_add',methods=['POST','GET'])
def owner_add():
    house_query=House.query.all()
    #qu = House.query.all()
    return render_template('house/add_owner.html',house_query=house_query)


@house.route('/house_owner/add/post', methods=['POST', 'GET'])
def owner_add_post():
    q_house_owner = Owner.query.filter_by(house_houseid=request.form.get('owner_houseid')).first()
    if q_house_owner is not None :
        flash("该房子已有业主")
        return redirect(url_for('house.owner_add'))
    else:
        owner=Owner(ownername=request.form.get('owner_ownername'),house_houseid=request.form.get('owner_houseid'),
                    ownerphone=request.form.get('owner_ownerphone'),owneridcard=request.form.get('owner_owneridcard'),
                    owneryears=request.form.get('owner_owneryears'),ownerstatus=request.form.get('owner_ownerstatus'),ownerdate=datetime.strptime((request.form.get('owner_ownerdate')).strip(), "%Y-%m-%d"))
        q_user = User.query.filter_by(house_houseid = owner.house_houseid).first()
        if  q_user is None:
            user = User(house_houseid=owner.house_houseid, username=owner.house_houseid, password='111111')
            db.session.add(user)
            db.session.commit()
        q_house = House.query.filter_by(houseid=owner.house_houseid).first()
        if q_house is not None and q_house !='':
            q_house.owner_ownername=owner.ownername
            q_house.housestatus=owner.ownerstatus
            db.session.add(q_house)
            db.session.commit()
        db.session.add(owner)
        db.session.commit()
    return redirect(url_for('house.house_owner'))

@house.route('/house_owner/delete/<string:house_id>',methods=['POST','GET'])
def owner_delete(house_id):
    res = {
        "status": 1,
        "message": "success"
    }
    owner = Owner.query.filter_by(house_houseid=house_id).first()
    q_house= House.query.filter_by(owner_ownername=owner.ownername).first()
    if q_house is not None and q_house !='':
        q_house.owner_ownername = ''
        q_house.housestatus = '闲置'
        db.session.add(owner)
        db.session.commit()
    user= User.query.fitler_by(house_houseid=house_id).first()
    if user is not None:
        db.session.delete(user)
    db.session.delete(owner)
    db.session.commit()
    return json.dumps(res)

@house.route('/house_owner/detail/<string:house_id>',methods=['POST','GET'])
def owner_detail(house_id):
    query=Owner.query.filter_by(house_houseid=house_id).first()
    query_house = House.query.all()
    return render_template('house/owner_detail.html',query=query,query_house=query_house)
@house.route('/house_owner/detail/post/',methods=['POST','GET'])
def owner_detail_post():
    a=request.form.get('detail_ownername')
    owner = Owner.query.filter_by(ownername=a).first()
    owner.house_houseid=request.form.get('detail_houseid')
    owner.ownerphone=request.form.get('detail_ownerphone')
    owner.owneridcard=request.form.get('detail_owneridcard')
    owner.ownerstatus=request.form.get('detail_ownerstatus')
    owner.owneryears=request.form.get('detail_owneryears')
    owner.ownerdate=datetime.strptime((request.form.get('detail_ownerdate')).strip(), "%Y-%m-%d")
    q_house = House.query.filter_by(houseid=owner.house_houseid).first()
    q_house.owner_ownername = owner.ownername
    q_house.housestatus = owner.ownerstatus
    q_user = User.query.filter_by(house_houseid=owner.house_houseid).first()
    if q_user is None:
        user = User(house_houseid=owner.house_houseid, username=owner.house_houseid, password='111111')
        db.session.add(user)
        db.session.commit()
    db.session.add(q_house)
    db.session.add(owner)
    db.session.commit()
    return redirect(url_for('house.house_owner'))
