# import random so we can use random numbers
import random
import secrets

# Import flask which is a micro web framework written in Python.
from flask import (
    Flask,
    jsonify, render_template, session, Response
)

from matplotlib.figure import Figure

# Function that create the app
import BetaController
import GraphController

# matplot lib gives us the ability to draw charts
import LabData

'''
create_app will be called when we want to start listening on a port for http traffic. It's main purpose is to rerun a flask object with routes (URLS) defined

'''


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    secret = secrets.token_urlsafe(32)
    app.secret_key = secret

    @app.route('/beta/plot.png')
    def plot_png():
        """
       Creates a route for an image. This way the image doesn't need  to be saved.
       In essence this should ask the controller to the same "save" function that matplot
       lib gives

       gets the beta_list from the session
       gets the base_line_list from the session
       gets the stock_name from the session

       calls teh GraphController's draw beta chart with baseline function passing the beta_list, the base_line_list and stockname)
       returns Response Object with a mimetype='image/png' and the output's getValue()
               """
        beta_list = session['beta_list']
        base_line_list = session['base_line_list']
        stockName = session["stock_name"]

        outPut = GraphController.draw_beta_chart_with_baseline(beta_list,base_line_list,stockName)

        return Response(outPut.getvalue(), mimetype='image/png')

    #   Simple route
    @app.route('/')
    def hello_world():
        return jsonify({
            "status": "success",
            "message": "Hello World!"
        })

    @app.route('/hello/<name>')
    def hello(name):
        session['user'] = name
        return render_template('hello_world.html', name=name)

    @app.route('/Beta/Debug')
    def BetaDebug():
        """
        Perhaps a useful debug URL to see what is stored in the session.

        :return:
        """
        beta_list = session['beta_list']
        base_line_list = session['base_line_list']
        stockName = session["stock_name"]
        betaListStr = " ".join (str (e) for e in beta_list)
        baseLineStr = "".join (str (a) for a in base_line_list)
        return "<h1>"+stockName+"</h1><p>"+ baseLineStr +"<p>" + betaListStr

    @app.route('/Beta/<stockName>/<numberOfPeriods>')
    def Beta(stockName="AAPL", numberOfPeriods=10):
        """
        this is the main function
        it calls the BetaController's do_calculations function sending the stock name and hte number of periods that is on the url (casting the number of periods to int)
        that call returns two lists, one is base_beta which is the overall beta and the other is chunked_beta which has our chunked beta calculations
        we "save" these values to the sessions.
        and call the render template to display.

        :param stockName:
        :param numberOfPeriods:
        :return:
        """
        base_betas,chunked_betas = BetaController.do_calculations(stockName, int(numberOfPeriods))
        session["stock_name"] = stockName
        session['beta_list'] = chunked_betas
        session['base_line_list'] = base_betas
        session['numberOfPeriods'] = numberOfPeriods
        return render_template('hello_world.html', stockName=stockName)

    return app  # do not forget to return the app


def create_figure(name):
    """
    just a sample test to create a figure
    :param name:
    :return:
    """
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    axis.set_title("Your name: " + name)
    return fig


APP = create_app()

if __name__ == '__main__':
    # APP.run(host='0.0.0.0', port=5000, debug=True)
    # APP.run(debug=True)

    APP.run(debug=True, port=8081)
