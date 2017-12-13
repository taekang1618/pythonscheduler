from flask import Flask, render_template,\
  request, redirect, url_for, json, jsonify
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
	data = json.load(open('burger.json'))
	total_duration = data["totalDuration"]
	interval = float(total_duration)
	margin_left = 0
	width = 0
	margin_top = 0
	task_name = None
	bar_list = []
	time = Markup("<div class='test' style='animation-duration:" +
	              str(total_duration) + "s'></div>")
	prev_val = []
	class_num = 0
	count = 0
	sorted_tasks = sorted(data["tasks"], key=lambda k: k["timestamp"][0])
	for k in sorted_tasks:
		task_name = k["name"]
		duration = k["duration"]
		start, end = k["timestamp"]
		margin_left = (start / float(interval)) * 100
		width = ((end - start) / float(interval)) * 100
		bar = "<span style='position:relative;width:{}%;margin-left:{}%;margin-top:{}pt;margin-botton:0pt;height:30pt;font-size:8pt' class='bar-{}'>{}</span>".format(width, margin_left, margin_top, count % 3, "")
		margin_top += 0
		prev_val = duration
		bar_list.append(Markup(bar))
		count += 1
	t_list = []
	time_list = []
	for t in data["tasks"]:
		t_list.append(t["name"])
		time_list.append(t["timestamp"])
	return render_template('index.html', data=bar_list, timer = time, 
		                    duration=total_duration, raw_data = data["tasks"],
							t_list = t_list, time_list = time_list)


@app.route('/', methods=['GET'])
def loadSchedule():
    return render_template('index2.html')


def main():
    app.debug = True
    log_handler = logging.FileHandler('my_flask.log')
    log_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(log_handler)
    app.run()


if __name__ == '__main__':
    main()
