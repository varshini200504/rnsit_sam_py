from flask import Flask, jsonify, request
from person_dao import Person, Db_operations
import pymysql

persons = Db_operations()

persons.create_table()
app = Flask(__name__)

@app.route('/persons',methods=['POST'])
def persons_create():
    body = request.get_json()
    new_person = Person(body['name'], body['gender'], body['dob'], body['location'])
    print(type(new_person))
    id = persons.insert_row(new_person)
    person = persons.search_row(id)
    person_dict = {'id':person[0], 'name':person[1], 'gender':person[2], 'dob':person[3], 'location': person[4]}
    return jsonify(person_dict)

@app.route('/new_persons/<id>',methods=['GET'])
def persons_read_by_id(id):
    person = persons.search_row(id)
    print(person)
    print(type(person))
    if person == None:
        return jsonify("Person not found")
    person_dict = {'id':person.id, 'name':person.name, 'gender':person.gender, 'location':person.location, 'dob': person.dob}
    return jsonify(person_dict)

@app.route('/persons',methods=['GET'])
def persons_read_all():
    persons_list = persons.list_all_rows()
    persons_dict = []
    for person in persons_list:
        persons_dict.append({'id':person.id, 'name':person.name, 'gender':person.gender, 'location':person.location, 'dob': person.dob})
    return jsonify(persons_dict)

@app.route('/persons/<id>',methods=['PUT'])
def persons_update(id):
    body = request.get_json()
    old_peron_obj = persons.search_row(id)
    if not old_peron_obj:
        return jsonify({'message': 'Person not found'})
    old_peron_obj.name = body['name']
    old_peron_obj.gender = body['gender']
    old_peron_obj.location = body['location']
    old_peron_obj.dob = body['dob']
    id = body['id']
    persons.update_row(old_peron_obj, id)
    person = persons.search_row(id)
    person_dict = {'id':person.id, 'name':person.name, 'gender':person.gender, 'location':person.location, 'dob': person.dob}
    return jsonify(person_dict)

@app.route('/persons/<id>',methods=['DELETE'])
def persons_delete(id):
    old_person_obj = persons.search_row(id)
    if not old_person_obj:
        return jsonify({'message': 'Person not found', 'is_error': 1})
    persons.delete_row(id)
    return jsonify({'message': 'Person is deleted', 'is_error': 0})

app.run(debug=True)