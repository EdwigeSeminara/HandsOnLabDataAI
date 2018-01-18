# AZURE RED SHIRT DEV TOUR

## Hands On Lab Cognitive Services & AI

1-	IOT

The dataset contains 9568 data points collected from a Combined Cycle Power Plant over 6 years (2006-2011), when the power plant was set to work with full load. 
Features consist of hourly average ambient variables Temperature (T), Ambient Pressure (AP), Relative Humidity (RH), Exhaust Vacuum (V) and the net hourly electrical energy output (EP) of the plant.

We will use Azure Machine Learning Studio to create a model that can detect anomalies in that power plant data.

Then we will simulate new data from that power plant and see what's happenning on a Power BI report.

First of all, check that you have 
* Python 2.7 installed
* A Power BI account (you can have a free one)
* An Azure Account (you can have a free one)

## Ready ?

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
* But we have some missing values. Our algorithm will ignore the entire line and predict nothing here…
* Add a Clean Missing Data with 0 for the replacement value

![image 11](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/11.JPG)
![image 12](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/12.JPG)

* To train then test our algorithm we need to split our data
* Add a Split Data

![image 13](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/13.JPG)
![image 14](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/14.JPG)

* We want to detect anomalies on future data using the dataset we have.
* We are going to use an algorithm called One-Class Support Vector Machine (https://docs.microsoft.com/en-us/azure/machine-learning/studio-module-reference/one-class-support-vector-machine) which enables unsupervised training on a dataset with few anomalies.
* Add it to the flow

![image 15](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/15.JPG)

* Add a Train Anomaly Detection Model
* Add a Score Model

![image 16](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/16.JPG)

* Run it
* Check your output
* We have the Scored Labels Column which is useless
* Add a Select Column in Dataset and remove the Scored Labels column
* We would like the column Scored Probabilities to be more “expressive”
* Add a Normalize Data with a LogNormal transformation method on the Scored Probabilities column

![image 18](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/18.JPG)

* Run it again and check your output

### We have a model which is able to detect anomaly risk in a dataset
### We now need to use this model outside of Azure ML

* Click on Set Up Web Service, Predictive Web Service

![image 20](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/20.JPG)

* Run the predictive experiment

![image 21](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/21.JPG)

* Check the input and the output. None of them is valid.
* Put the Web Service Input AFTER the transformation
* Add a Select Column in Dataset and keep only the Scored Probabilities column at the end. This is the only thing we want.
* Add a Normalize Data just as before.
* We now should rename the output column to make it easier to use.
* Add an Execute Python Script and paste the following code

``` python
import pandas as pd 

def azureml_main(frame): 
	l = frame.columns.tolist() 
	l[0] = "Proba" 
	frame.columns = l 
	return frame,
```

![image 23](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/23.JPG)

* Run it. You should have a perfect output.
