from flask import Flask, g, request, jsonify
from database import get_db

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/member', methods=['GET'])
def get_members():
    db = get_db()
    members_cur = db.execute('select id, name, doc, ppt, premium, final, mobile, policy, branch from members')
    members = members_cur.fetchall()
    return_value = []
    
    for member in members:
        member_dict = {}
        member_dict['id'] = member['id']
        member_dict['name'] = member['name']
        member_dict['doc'] = member['doc']
        member_dict['ppt'] = member['ppt']
        member_dict['premium'] = member['premium']
        member_dict['final'] = member['final']
        member_dict['mobile'] = member['mobile']
        member_dict['policy'] = member['policy']
        member_dict['branch'] = member['branch']

        return_value.append(member_dict)
     
    return jsonify({"members": return_value})

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    db = get_db()
    member_cur = db.execute('select id, name, doc, ppt, premium, final, mobile, policy, branch from members where id = ?', [member_id])
    member = member_cur.fetchone()

    return jsonify({"member": {"id": member['id'], "name": member['name'], "doc": member['doc'], "ppt": member['ppt'], "premium": member['premium'], "final": member['final'], "mobile": member['mobile'], "policy": member['policy'], "branch": member['branch']}})

@app.route('/member', methods=['POST'])
def add_members():
    new_member = request.get_json()

    name = new_member['name']
    doc = new_member['doc']
    ppt = new_member['ppt']
    premium = new_member['premium']
    final = new_member['final']
    mobile = new_member['mobile']
    policy = new_member['policy']
    branch = new_member['branch']

    db = get_db()
    db.execute('insert into members (name, doc, ppt, premium, final, mobile, policy, branch) values (?, ?, ?, ?, ?, ?, ?, ?)', [name, doc, ppt, premium, final, mobile, policy, branch])
    db.commit()
    
    member_cur = db.execute('select id, name, doc, ppt, premium, final, mobile, policy, branch from members where doc = ?', [doc])
    member = member_cur.fetchone()

    return jsonify({"member": {"id": member['id'], "name": member['name'], "doc": member['doc'], "ppt": member['ppt'], "premium": member['premium'], "final": member['final'], "mobile": member['mobile'], "policy": member['policy'], "branch": member['branch']}})

@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
    new_member = request.get_json()

    name = new_member['name']
    doc = new_member['doc']
    ppt = new_member['ppt']
    premium = new_member['premium']
    final = new_member['final']
    mobile = new_member['mobile']
    policy = new_member['policy']
    branch = new_member['branch']

    db = get_db()
    db.execute('update members set name = ?, doc = ?, ppt = ?, premium = ?, final = ?, mobile = ?, policy = ?, branch = ? where id = ?', [name, doc, ppt, premium, final, mobile, policy, branch, member_id])
    db.commit()

    member_cur = db.execute('select id, name, doc, ppt, premium, final, mobile, policy, branch from members where doc = ?', [doc])
    member = member_cur.fetchone()

    return jsonify({"member": {"id": member['id'], "name": member['name'], "doc": member['doc'], "ppt": member['ppt'], "premium": member['premium'], "final": member['final'], "mobile": member['mobile'], "policy": member['policy'], "branch": member['branch']}})


@app.route('/member/<int:member_id>', methods=['DELETE'])
def add_member(member_id):
    db = get_db()
    db.execute('delete from members where id = ?', [member_id])
    db.commit()

    return jsonify({'message': 'The member has been deleted'})

if __name__ == '__main__':
    app.run(debug=True)