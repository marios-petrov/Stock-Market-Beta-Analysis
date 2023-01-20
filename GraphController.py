
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import BetaController
import matplotlib.pyplot as plt
import io



def draw_beta_chart_with_baseline (beta_list, base_line,  security_name):
    """
    Take the beta_list and base_line and security name and make a chart from it.


    :param beta_list:
    :param base_line:
    :param security_name:
    :return:
    """
    fig = plt.figure()
    if (len (beta_list) > len (base_line)):
        for x in range (len (beta_list)-1):
            base_line.append(base_line[0])
    print(beta_list)

    plt.plot(range(len(beta_list)), beta_list)
    plt.plot(range(len(beta_list)), base_line)
    plt.xlabel("Chunk")
    plt.ylabel("Beta")
    plt.title("AAPL Beta Over Time")

    output = io.BytesIO() # some magic to return a stream of png/jpg format
    FigureCanvas(fig).print_png(output) # some magic to return a stream of png/jpg format 
    return output

if __name__ == '__main__':
    beta_list = BetaController.get_beta ("AAPL", 10)
    base_line_list = BetaController.get_beta ("AAPL", 1)
    draw_beta_chart_with_baseline  (beta_list, base_line_list, 'AAPL')