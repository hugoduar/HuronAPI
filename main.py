import crawler
from flask import Flask, render_template, request

web_site = Flask(__name__)

@web_site.route('/')
def index():
	return render_template('index.html')

@web_site.route('/problems/<handler>')
@web_site.route('/problems', defaults={'handler':None})
def problems_page(handler):
  if not handler:
    handler = request.args.get('username')

  if not handler:
    return 'Sorry error something, malformed request.'
  
  return render_template('problems.html', problems=crawler.aggregateProblems(handler))

  
web_site.run(host='0.0.0.0', port=8080)

