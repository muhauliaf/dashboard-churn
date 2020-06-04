from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import BytesIO
import base64
import matplotlib

matplotlib.use('Agg')


from helper import *

app = Flask(__name__)

data = load_telco()

@app.route("/")
def index():
	# copy data as raw
	raw = data.copy()

	# generate value for cards
	## churn rate & retaining customers
	table_churn_res = table_churn(raw)
	percent_churn = table_churn_res.loc['Yes', 'percent'].round(2)
	percent_retain = table_churn_res.loc['No', 'percent'].round(2)
	## average lifetime value
	average_cltv = int(raw['cltv'].mean())
	# compile card values as `card_data`
	card_data = dict(
			percent_churn = f'{percent_churn}%',
			percent_retain = f'{percent_retain}%',
			average_cltv = f'{average_cltv:,}'
		)

	# generate plot
	plot_phone_res = plot_phone(raw)
	plot_internet_res = plot_internet(raw)
	# plot_tenure_cltv_res = plot_tenure_cltv(raw)
	plot_tenure_churn_res = plot_tenure_churn(raw)

	# render to html
	return render_template('index.html',
		   card_data = card_data, 
		 plot_phone_res=plot_phone_res,
		 plot_internet_res=plot_internet_res,
		#  plot_tenure_cltv_res=plot_tenure_cltv_res,
		 plot_tenure_churn_res=plot_tenure_churn_res
		)


if __name__ == "__main__": 
    app.run(debug=True)
