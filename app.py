from flask import Flask, render_template, request, redirect, url_for, json, jsonify
import datetime
import requests
import logging
import json
from pprint import pprint
from flask import jsonify
from flask import Markup
 
# Create app
app = Flask(__name__)
 
 
@app.route('/getSchedule', methods=['GET'])
def index():
	data = json.load(open('task.json'))
	pprint(data)
	totalDuration = data["totalDuration"]
	interval = float(totalDuration)
	margin_left = 0
	width = 0
	margin_top = 0
	task_name = None
	bar_list = []
	prev_val = []
	class_num = 0
	count = 0
	for k in data:
		if k != "totalDuration" and k != "numTasks":
			task_name = k
			duration = data[k]
			print("**** " + str(duration))
			start, end = duration
			margin_left = (start / float(interval)) * 100
			width = ((end - start) / float(interval)) * 100
			# if len(prev_val) > 0 and prev_val[1] < end:
			# 	margin_left -= ((end- prev_val[1]) / float(interval)) * 100
			# else:
			# 	margin_left = 0
			bar = "<span style='width:{}%;margin-left:{}%;margin-top:{}pt;height:30pt' class='bar-{}'>{}</span>".format(width, margin_left, margin_top, count % 3, task_name)
			print(task_name)
			print("width " + str(width))
			print("margin_left " + str(margin_left))
			print("margin_top " + str(margin_top))
			margin_top += 0
			prev_val = duration
			bar_list.append(Markup(bar))
			count += 1

	# print(data["totalDuration"])
	# test="<p>Hi</p>"
	# test = "<span style='width:200pt;margin-left:30pt;margin-top:30pt;height:30pt'class='bar-4'>Task123</span>"
	# test2 = "<span style='width:200pt;margin-left:30pt;margin-top:30pt;height:30pt'class='bar-4'>Task234</span>"
	# l = [Markup(test), Markup(test2)]
	# data = jsonify(data)
	print(bar_list)
	# return render_template('index.html', data=Markup(test))
	return render_template('index.html', data=bar_list)


@app.route('/', methods=['GET'])
def loadSchedule():
    return render_template('index2.html')
 
 
 
# @app.route('/stuff/<message>', methods=['GET'])
# def url_param_example():
#     return render_template('template/startbootstrap-stylish-portfolio-gh-pages/index.html')
 
 
# @app.route('/temp', methods=['GET'])
# def template_example():
#     return render_template('a_temp.html', adj='Awesome',
#                            things=['Flask', 'Python'],
#                            date=datetime.datetime.now().strftime('%m/%d/%Y'))
 
 
# @app.route('/child', methods=['GET'])
# def template_child():
#     return render_template('extends.html')
 
 
# @app.route('/submit', methods=['GET', 'POST'])
# def submit_page():
#     if request.method == 'POST':
#         msg = '{} was POST-ed'.format(request.form['submit'])
#     else:
#         msg = request.args.get('submit')
#     return redirect((url_for('log', msg=msg, mode='debug')))
 
 
# @app.route('/log/<msg>/<mode>')
# def log(msg, mode):
#     app.logger.debug(msg)
#     return('LEVEL:{}\nLogged: {}'.format(mode, msg))
 
 
# @app.route('/json', methods=['GET', 'POST'])
# def json_endpoint():
#     if request.method == 'POST':
#         extracted = json.loads(request.form['data'])
#         return 'key: {}\nlength: {}'.format(extracted.keys(), len(extracted))
#     else:
#         obj = {'data': [True, ['a list', 'of strings'], {'null': None}]}
#         return jsonify(obj)
 
# @app.route('/board', methods=['GET', 'POST'])
# def message_board():
#     if request.method == 'POST':
#         username = request.form['usr']
#         message = request.form['msg']
#         with open("mb.txt", 'a') as f:
#             f.write("{} says: {} \t [{}]\n".format(username, message, datetime.datetime.now().strftime('%m/%d/%Y')))
#     with open("mb.txt", 'r') as f:
#         return f.read()
 
# def test_request_data():
#     data = {'submit': 'some post data'}
#     params = {'submit': 'some get params'}
#     url = 'http://127.0.0.1:5000/submit'
#     requests.get(url, params=params)
#     requests.post(url, data=data)

# def test_message_board(message="hello", usr="sharry"):
#     data = {'usr' : usr, 'msg' : msg}
#     url = 'http://127.0.0.1:5000/board'
#     requests.post(url, data=data)

 
# def test_json():
#     data = {'some numbers': [1, 2.5]}
#     url = 'http://127.0.0.1:5000/json'
#     r = requests.get(url)
#     r.text
#     r.json()
#     r = requests.post(url, data={'data': json.dumps(data)})
#     print(r.text)
 
 
def main():
    app.debug = True
    log_handler = logging.FileHandler('my_flask.log')
    log_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(log_handler)
    app.run()
 
if __name__ == '__main__':
    main()