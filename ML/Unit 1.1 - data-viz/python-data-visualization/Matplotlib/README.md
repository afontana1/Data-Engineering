# Subplotting

## [Arranging multiple Axes in a Figure](https://matplotlib.org/stable/tutorials/intermediate/arranging_axes.html#sphx-glr-tutorials-intermediate-arranging-axes-py)

Often more than one Axes is wanted on a figure at a time, usually organized into a regular grid. Matplotlib has a variety of tools for working with grids of Axes that have evolved over the history of the library. Here we will discuss the tools we think users should use most often, the tools that underpin how Axes are organized, and mention some of the older tools.

[Jupyter Notebook](https://github.com/javedali99/python-data-visualization/blob/main/Matplotlib/arranging_axes.ipynb)



## [Figure subfigures](https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subfigures.html)

Sometimes it is desirable to have a figure with two different layouts in it. This can be achieved with [nested gridspecs](https://matplotlib.org/stable/gallery/subplots_axes_and_figures/gridspec_nested.html), but having a virtual figure with its own artists is helpful, so Matplotlib also has `subfigures`, accessed by calling `matplotlib.figure.Figure.add_subfigure` in a way that is analogous to `matplotlib.figure.Figure.add_subplot`, or `matplotlib.figure.Figure.subfigures` to make an array of subfigures. Note that subfigures can also have their own child subfigures.

[Jupyter Notebook](https://github.com/javedali99/python-data-visualization/blob/main/Matplotlib/subfigures.ipynb)


## [Tutorial on Plot Organization in matplotlib — Your One-stop Guide](https://github.com/maticalderini/Tutorial_pltOrganization)

A brief tutorial on how to organize multiple subplots with different positions and sizes on matplotlib.

[Jupyter Notebook](https://github.com/maticalderini/Tutorial_pltOrganization/blob/master/OrganizationTutorial.ipynb)


## [Creating Subplots in Matplotlib](https://python-course.eu/numerical-programming/creating-subplots-in-matplotlib.php)

```python
import matplotlib.pyplot as plt

python_course_green = "#476042"
fig = plt.figure(figsize=(6, 4))
sub1 = plt.subplot(2, 2, 1)
sub1.set_xticks(())
sub1.set_yticks(())
sub1.text(0.5, 0.5, 'subplot(2,2,1)', ha='center', va='center',
        size=20, alpha=.5)

sub2 = plt.subplot(2, 2, 2)
sub2.set_xticks(())
sub2.set_yticks(())
sub2.text(0.5, 0.5, 'subplot(2,2,2)', ha='center', va='center',
        size=20, alpha=.5)

sub3 = plt.subplot(2, 2, 3)
sub3.set_xticks(())
sub3.set_yticks(())
sub3.text(0.5, 0.5, 'subplot(2,2,3)', ha='center', va='center',
        size=20, alpha=.5)

sub4 = plt.subplot(2, 2, 4, facecolor=python_course_green)
sub4.set_xticks(())
sub4.set_yticks(())
sub4.text(0.5, 0.5, 'subplot(2,2,4)', ha='center', va='center',
        size=20, alpha=.5, color="y")

fig.tight_layout()
plt.show()
```

<p align="center">
  <a href="https://python-course.eu/numerical-programming/creating-subplots-in-matplotlib.php">
         <img src="https://user-images.githubusercontent.com/15319503/165600695-d58abf3e-082f-4732-930f-6ce2ff5c60c5.png" 
              width="450" height="300" alt="subplots-in-Python"/>
      </a>
</p>


```python
import numpy as np
from numpy import e, pi, sin, exp, cos
import matplotlib.pyplot as plt

def f(t):
    return exp(-t) * cos(2*pi*t)

def fp(t):
    return -2*pi * exp(-t) * sin(2*pi*t) - e**(-t)*cos(2*pi*t)

def g(t):
    return sin(t) * cos(1/(t+0.1))

def g(t):
    return sin(t) * cos(1/(t))


python_course_green = "#476042"
fig = plt.figure(figsize=(6, 4))

t = np.arange(-5.0, 1.0, 0.1)

sub1 = fig.add_subplot(221) # instead of plt.subplot(2, 2, 1)
sub1.set_title('The function f') # non OOP: plt.title('The function f')
sub1.plot(t, f(t))


sub2 = fig.add_subplot(222, facecolor="lightgrey")
sub2.set_title('fp, the derivation of f')
sub2.plot(t, fp(t))


t = np.arange(-3.0, 2.0, 0.02)
sub3 = fig.add_subplot(223)
sub3.set_title('The function g')
sub3.plot(t, g(t))

t = np.arange(-0.2, 0.2, 0.001)
sub4 = fig.add_subplot(224, facecolor="lightgrey")
sub4.set_title('A closer look at g')
sub4.set_xticks([-0.2, -0.1, 0, 0.1, 0.2])
sub4.set_yticks([-0.15, -0.1, 0, 0.1, 0.15])
sub4.plot(t, g(t))

plt.plot(t, g(t))

plt.tight_layout()
plt.show()
```

<p align="center">
  <a href="https://python-course.eu/numerical-programming/creating-subplots-in-matplotlib.php">
         <img src="https://python-course.eu/images/numerical-programming/creating-subplots-in-matplotlib_12.webp" 
              width="550" height="400" alt="subplots-in-Python"/>
      </a>
</p>


