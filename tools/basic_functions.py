from matplotlib import pyplot as plt

def plotfigure(figsize,xlabel,ylabel,title,x,y=[],style="k-",graph="plot"):
    plt.figure(figsize=figsize)
    plt.grid(True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if len(y) == 0:
        plt.plot(x,style)
    else:
        if graph=="plot":
            plt.plot(x,y,style)
        if graph== "semilogx":
            plt.semilogx(x,y,style)
        if graph== "semilogy":
            plt.semilogy(x,y,style)
        if graph== "loglog":
            plt.loglog(x,y,style)
    plt.tight_layout()
    plt.show()
    plt.close()