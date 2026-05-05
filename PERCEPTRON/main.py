from perceptron import Perceptron
from training import Point




#Plot the training data and the decision boundary
import matplotlib.pyplot as plt
from training import Point
canvas_width = 40
canvas_height = 40
points = [Point(canvas_width, canvas_height) for _ in range(200)]
for point in points:
    color = 'red' if point.label() == 1 else 'blue'
    plt.scatter(point.x, point.y, color=color)
plt.plot([0, canvas_width], [0, canvas_height], color='black')
plt.xlim(0, canvas_width)
plt.ylim(0, canvas_height)
plt.show()


for point in points:
    inputs = [point.x, point.y]
    target = point.label()
    Perceptron.train(inputs, target)

    guess = Perceptron.guess(inputs)
    if guess == target:
        #Plot the point in green if the guess is correct
        plt.scatter(point.x, point.y, color='green')

    
#click mouse to train the perceptron with the clicked point
def onclick(event):
    x = event.xdata
    y = event.ydata
    inputs = [x, y]
    target = 1 if y > x else 0
    Perceptron.train(inputs, target)
    guess = Perceptron.guess(inputs)
    color = 'green' if guess == target else 'red'
    plt.scatter(x, y, color=color)
    plt.draw()