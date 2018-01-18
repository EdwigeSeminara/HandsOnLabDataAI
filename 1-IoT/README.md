<h1> AZURE RED SHIRT DEV TOUR

<h2> Hands On Lab Cognitive Services & AI


1-	IOT

The dataset contains 9568 data points collected from a Combined Cycle Power Plant over 6 years (2006-2011), when the power plant was set to work with full load. 
Features consist of hourly average ambient variables Temperature (T), Ambient Pressure (AP), Relative Humidity (RH), Exhaust Vacuum (V) and the net hourly electrical energy output (EP) of the plant.

We will use Azure Machine Learning Studio to create a model that can detect anomalies in that power plant data.

Then we will simulate new data from that power plant and see what's happenning on a Power BI report.

First of all, check that you have 
* Python 2.7 installed
* A Power BI account (you can have a free one)
* An Azure Account (you can have a free one)

* Go to https://studio.azureml.net/
* Create a free account or sign in
* Click New, Dataset

![image 1](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/1.JPG)

* Add the dataset “folds.csv”

![image 2](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/2.JPG)

* Click New again
* Create a new Experiment

![image 3](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/3.JPG)

* Rename your new experiment
* Add to this experiment your newly added dataset
![image 5](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/5.JPG)

* Click on Visualize

![image 6](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/6.JPG)

* We have 2 useless columns to remove
* Add a Select Column in Dataset

![image 7](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/7.JPG)

* Remove Column 0 and Column 6

![image 8](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/8.JPG)

* Run

![image 9](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/9.JPG)

* Visualize. You have kind of a good dataset.

![image 10](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/10.JPG)