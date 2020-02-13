import matplotlib.pyplot as plt

#Making the plot interactive with event handlers displaying annotations
def add_annot(fig,ax,plot1,arrayOfIds,labelsAsGenres):
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):

        
        pos = plot1.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "{}, ({})".format(" ".join([arrayOfIds[n] for n in ind["ind"]]),
                           " ".join([labelsAsGenres[n] for n in ind["ind"]]))
        annot.set_text(text)
        #annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = plot1.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)
    
    


