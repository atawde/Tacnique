import sqlite3
import gradio as gr
from openai import OpenAI, OpenAIError
import os
from IPython.display import display, Markdown, Latex, HTML, JSON
import datetime

messages = [
	{'role' : 'system', 'content' : 'You are assistant who acts as middleperson between user and database. \
		There is a sqlite database which has two tables Employees (id, name, department, salary, hire_date) and \
		Dapartments (id, name, manager) \
	 '}
]

css = """
	.chatHistory {background-color: #E2EAF4 color: black}
	.promptBox {background-color: #E7DDFF, color: black !important}
	.gradio-container {background: #494545}
"""


def runQuery(qry: str):

	print(qry)		# To check at command window if SQL is formed properly
	try:
		conn = sqlite3.connect('tacnique.db')
		cursor = conn.execute(qry)
	except:
 		return 'No records found matching query criterion'

	qryResult = ''
	if cursor.fetchone()[0] > 0:
		for row in cursor:
			my_string = ' | '.join(map(str, row))
			qryResult += my_string+'\n'
	else:
		return 'No records found matching query criterion'

	conn.close()

	return qryResult

def gptResponse(prompt: str):

	messages.append({'role' : 'assistant', 'content' : 'Write a sql query to satisfy the below request from user. \
														Do not include word "sql" at the start of response and backticks at the end \
		                                                when SQL can not be constructed then respond ```not a valid query``` \
		                                                '})

	messages.append({'role' : 'user', 'content' : prompt})
	resp = get_completion(messages)
 
	if resp.find('valid') > 0 and resp.find('query') > 0:
		messages.append({'role' : 'user', 'content' : 'Valid SQL could not be constrcuted based on your request'})
	else:
		messages.append({'role' : 'user', 'content' : runQuery(resp)})
#	messages.append({'role' : 'assistant', 'content' : resp})
	displayMessage = ''

	for item in messages:
		if item['role'] == 'user':
			displayMessage += item['content'] + '\n'

	return displayMessage

def main():

#	OpenAI.api_key  = 'my api key'   <unless it is set in your env variable>

	now = datetime.datetime.now()
	day = now.strftime("%A")
	date = now.strftime("%d")
	month = now.strftime("%B")

	th = 'th'
	if day == 1:
		th = 'st'
	elif day == 2:
		th = 'nd'
	elif day == 3:
		th = 'rd'

	greeting = '<center>!!! Hi, how can I help you today ? </center>'
	greeting += '<center>Today is '+day+' the '+str(date)+th+' of '+month+' </center>'

	with gr.Blocks(css=css) as demo:
		gr.Markdown(greeting)
		output = gr.Textbox(label='Conversation', elem_classes='chatHistory')
		prompt = gr.Textbox(label='Please enter your query', elem_classes='promptBox')
		qryBtn = gr.Button('Chat', elem_classes='promptBox')
		qryBtn.click(fn=gptResponse, inputs=prompt, outputs=output, api_name='ask')

	demo.launch()

	resp = get_completion(messages)
	messages.append({'role' : 'assistant', 'content' : resp})


def get_completion(messages, model="gpt-3.5-turbo", temperature=0):
    
    client = OpenAI()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        return f"Error: {e}"

if __name__== "__main__":
   main()
