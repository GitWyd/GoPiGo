import matplotlib.pyplot as plt
import follow_obstacle

def plot_graph():
    #location_history = [[1,1],[2,2],[5,5]]
    location_history = follow_obstacle.get_location_history()
    print "Location history"
    print location_history
    #obstacle_history = [[1,2],[1,3],[2,4],[4, 4]]
    obstacle_history follow_obstacle.get_obstacle_history()
    print "Obstacle History"
    print obstacle_history
    plt.xlim(0, 300)
    plt.ylim(0, 300)
    plt.xlabel('X-Axis')
    plt.ylabel('Y-Axis')
    ax = plt.axes()

    # Plotting the location along the m-line
    for i in range(1,len(location_history),1):
            prev = location_history[i-1]
            curr = location_history[i]
            print (prev[0], prev[1], curr[0], curr[1])
            ax.annotate("", xy=(curr[0], curr[1]), xytext=(prev[0], prev[1]),
        arrowprops=dict(arrowstyle="->"))

    # Plotting the location along the obstacle
    for i in range(1,len(obstacle_history),1):
            prev = obstacle_history[i-1]
            curr = obstacle_history[i]
            print (prev[0], prev[1], curr[0], curr[1])
            ax.annotate("", xy=(curr[0], curr[1]), xytext=(prev[0], prev[1]),
        arrowprops=dict(arrowstyle="->"))
    plt.show()
