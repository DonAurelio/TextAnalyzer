# -*- encoding: utf-8 -*-
import json
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from tools.textparsers import stanford_parser

class ParserView(TemplateView):
	template_name = 'textparser/index.html'

	def post(self,request,*args,**kwargs):
		text = request.POST.get('text',None)
		model = request.POST.get('radio-modelo',None)
		mode = request.POST.get('radio-modo',None)
		test_file_name = request.POST.get('radio-test',None) 

		# Options given by the user throut the template
		print "Data:", text, model, mode, test_file_name

		# Text Processing
		print stanford_parser(text)

		# Template Rendetization
		template = loader.get_template('textparser/includes/result_analisys.html')
		context = {}
		html = template.render(context)

		# Text validations, if the text field is empty, we return and error or
		# False status
		if len(text) == 0:
			respuesta = {'status':False,'html':html}
		else:
			respuesta = {'status':True,'html':html}

		data = json.dumps(respuesta)
		return HttpResponse(data,content_type='application/json')
		
