from flask import Flask
from flask_restplus import Resource, Api, fields
import datetime
import requests
import json
import pdb

app = Flask(__name__)
api = Api(app, version='1.0', title='Schedule Service API',
          description='A simple service where task are scheduled.')

ns = api.namespace('schedules', description='Feed ')

schedule = api.model('Schedule', {
    'scheduleId': fields.Integer(readonly=True, description='The task unique identifier'),
    'frequency': fields.String(readonly=True, description='Value is always daily.'),
    'time': fields.String(required=True, description='Time in 24-hour format without timezone. eg. 14:00'),
    'command': fields.String(required=True, description='Command to run and will depend on the os platform used.')
})


class ScheduleData:
    def __init__(self):
        self.count = 0
        self.schedules = []

    def add_schedule(self, schedule):
        self.count += 1
        schedule['scheduleId'] = self.count
        schedule['frequency'] = "Daily"
        self.schedules.append(schedule)

    def get_schedule(self, scheduleId):
        for schedule in self.schedules:
            if int(schedule['scheduleId']) == int(scheduleId):
                return schedule


scheduledata = ScheduleData()
scheduledata.add_schedule({'time': "14:00", 'command': "echo 'task 1'"})
scheduledata.add_schedule({'time': "10:00", 'command': "echo 'task 2'"})
scheduledata.add_schedule({'time': "18:00", 'command': "echo 'task 3'"})


@ns.route('/')
class ScheduleList(Resource):
    '''Shows a list of all schedules'''
    @ns.doc('list_schedules')
    @ns.marshal_list_with(schedule)
    def get(self):
        '''List all schedules'''
        return scheduledata.schedules

    @ns.doc('create_schedule')
    @ns.expect(schedule)
    # @ns.marshal_with(schedule, code=201)
    def post(self):
        '''Create a new schedule'''
        scheduledata.add_schedule(api.payload)
        return scheduledata.schedules, 201


@ns.route('/run/<int:schedule_id>')
class ScheduleRun(Resource):

    def post(self, schedule_id):
        '''Run a schedule'''
        schedule = scheduledata.get_schedule(schedule_id)
        command = json.dumps({'command': schedule['command']})
        queue_url = 'http://localhost:5002/todos/'
        requests.post(queue_url, json=command)

        return scheduledata.schedules, 201


# def check_schedule():
#     while True:
#         time_now = datetime.datetime.now().time().replace(second=0, microsecond=0)
#         for schedule in scheduledata.schedules:
#             schedule_time = datetime.datetime.strptime(
#                 schedule['time'], "%H:%M").time()
#             if time_now == schedule_time:
#                 queue_url = 'http://localhost:5001/todos'
#                 data = {'command': schedule['command']}
#                 request.post(queue_url, data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')
