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

#### We first need to train a model, we will use Azure Machine Learning Studio for that 

* Go to https://studio.azureml.net/
* Create a free account or sign in
* Click New, Dataset

![image 1](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/1.JPG)

* Add the dataset “folds.csv” as a Generic CSV File with a header (.csv)
* Click New again
* Create a new Experiment by clicking Blank Experiment

![image 3](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/3.JPG)

* Rename your new experiment
* Add to this experiment your newly added dataset by clicking on the left pane under Saved Datasets/My Datasets
* Right Click on the bottom of the card then click Visualize

![image 6](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/6.JPG)

* We have 2 useless columns to remove
* Search on the left pane and add a Select Column in Dataset

![image 7](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/7.JPG)

* Remove Column 0 and Column 6 by using the Column Selector in the right pane.

![image 8](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/8.JPG)

* Run your experiment

![image 9](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/9.JPG)

* Visualize. You have kind of a good dataset.
* But we have some missing values. Our algorithm will ignore the entire line and predict nothing here…
* Add a Clean Missing Data with 0 for the replacement value.

![image 11](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/11.JPG)
![image 12](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/12.JPG)

* To train then test our algorithm we need to split our data
* Add a Split Data and attribute 80% of the rows for training.

![image 13](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/13.JPG)
![image 14](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/14.JPG)

* We want to detect anomalies on future data using the dataset we have.
* We are going to use an algorithm called One-Class Support Vector Machine (https://docs.microsoft.com/en-us/azure/machine-learning/studio-module-reference/one-class-support-vector-machine) which enables unsupervised learning on a dataset with few anomalies.
* Add it to the flow and make parameters as follow :
	* Create Trainer Mode : Single parameter
	* ƞ : 0.1
	* ɛ : 0.05

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

* Click on Set Up Web Service/Predictive Web Service

![image 21](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/21.JPG)

* Run the predictive experiment
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

![image 24](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/24.JPG)

* Run it. You should have a perfect output.

![image 25](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/25.JPG)

* Click on Deploy Web Service

![image 26](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/26.JPG)

### You now have access to this model throw an API which takes 5 floats as input and output one float : a 0-1 probability

* In the opened window click on the link Excel 2013 or later

![image 27](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/27.JPG)

* Open the file
* Click on Activate Modifications
* You are now able to test your model throw Excel
* On the right pane in Excel, click on HOL[predictive experiment]
* Check the Schema first

![image 29](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/29.JPG)

* Click on use sample data

![image 30](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/30.JPG)

* Select the entire created table as input and F1 as output

![image 31](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/31.JPG)

* Click predict
* You can modify values and click predict again to test your model

![image 32](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/32.JPG)
![image 33](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/33.JPG)
![image 34](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/34.JPG)

### We want to use it on streaming data to determine in real time if there are anomalies in our plant.

#### we will use Azure resources to make that streaming flow

* Go to https://portal.azure.com and sign in using your account or create a free one.
* Create a new Resource Group

![image 35](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/35.JPG)

* Click on Add on the top to add new resources
* Add a Storage Account, an Azure Stream Analytics and an Event Hubs just as follow, in that order

![image 36](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/36.JPG)
![image 37](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/37.JPG)
![image 38](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/38.JPG)

* Go back to your Resource Group
* Open the newly created Event Hubs and click on add an Event Hub, call it datatostream
* Go back to your Resource Group
* Open your newly created Storage Account and open Blob Objects
* Add a new Container

![image 39](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/39.JPG)

* Go back to your Resource Group
* Open your Stream Analytics
* Click on input and add an input from your Event Hub
* Go back to your Stream Analytics
* Click on output and add an output to your Blob Storage to archive outputs

![image 40](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/40.JPG)
![image 41](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/41.JPG)

* Also add an output to your PowerBi Account to visualize your data in real time

![image 42](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/42.JPG)
![image 43](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/43.JPG)

* Go back to your Stream Analytics
* Click on Functions
* Add a new function connected to your predictive API

![image 44](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/44.JPG)

* You can find your key there

![image 45](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/1-IoT/images/45.JPG)

* And the URL by clicking on REQUEST/RESPONSE and by copying the POST URL
* Go back to your Stream Analytics
* Click on Request
* Add the following request

``` sql
WITH anomaly AS ( 
	SELECT cast(T as float) as T, 
	cast(V as float) as V, 
	cast(AP as float) as AP, 
	cast(RH as float) as RH, 
	cast(PE as float) as PE, 
	cast(anomaly(T, V, AP, RH, PE) as float) as result from holBlobIn 
	) 

Select System.Timestamp as date, 'Paris' as location, T, V, AP, RH, PE, (result * 100) as result 
Into holBlobOut 
From anomaly 

Select System.Timestamp as date, 'Paris' as location, T, V, AP, RH, PE, (result * 100) as result 
Into holPbiOut 
From anomaly
```
* Now save it
* And launch your streaming task
* Nothing is now happening because our Event Hub does not receive anything
* Open any Python IDE
* Copy the following code

``` python
import json
import random
from datetime import datetime
from azure.servicebus import ServiceBusService

def rd(mu, sigma):
    return abs(round(random.normalvariate(mu, sigma), 2))

def main():
    sbs = ServiceBusService(service_namespace='holEvents',
                            shared_access_key_name='RootManageSharedAccessKey',
                            shared_access_key_value='ugV/8wxg/Z0ZoTWBZWRUP5j2cgaEDiJC26ZLuoshotY=')
    turn = 0
    while turn >= 0:
        t = rd(19.6, 67.6)
        ap = rd(1002.6, 101.1)
        rh = rd(54, 13.6)
        v = rd(83.5, 99.1)
        pe = rd(445.6, 61.1)

        now = datetime.now().strftime("%M")

        if turn == 0:
            time = now
        else:
            if now != time:

                data = {"T":str(t), "V":str(v), "AP":str(ap), "RH":str(rh), "PE":str(pe)}

                body = str.encode(json.dumps(data))
                print(body)
                sbs.send_event('datatostream', body)

                time = now

        turn += 1

if __name__ == '__main__':
    main()
```

* And launch it

#### It will send continuously values similar to what the plant is supposed to send but with some errors because it’s not exactly the same.

* Let it turns and go to Power BI