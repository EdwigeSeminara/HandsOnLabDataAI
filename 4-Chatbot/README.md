# Part 4 - Chatbot

In this part of the lab you will use Bot Framework to code a bot which will help the user to roll out a checklist.

The goal is to play with Bot Framework and quickly use Azure to deploy your bot to the cloud and invoke it in third-party applications.

The tutorial below will guide you to build a simple bot and deploy it, do not hesitate to use your imagination to enrich it!

## Prerequisites

For this part you will need:
* Visual Studio 2017 up-to-date
* Bot Framework Channel Emulator, downloadable **[here](https://github.com/Microsoft/BotFramework-Emulator/releases/tag/v3.5.35)**
* Microsoft Azure SDK up-to-date

## Retrieve, open and run the solution


To get started, make sure that the initial solution is properly launched in your environment. For it :

1. Open the **HolDataAI.Application.sln** solution
2. Run the project
3. An internet page is launched in your browser, note the port indicated in the url:
![localhosturl](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/4-Chatbot/README_files/localhosturl.PNG)

4. To interact with the bot we need an emulator. Launch Bot Framework Channel Emulator (if you have not installed it, download it **[here](https://github.com/Microsoft/BotFramework-Emulator/releases/tag/v3.5.35)** and install it)

5. In the "Bot Url" field, write the port that you noted in step 3

6. Do not change the other fields

7. In the text box at the bottom of the emulator, enter **hello**

8. Your **hello** appears in the chat area

9. The bot answers by welcoming you and asking for your technician id

10. Enter your technician id. The bot displays the message **Thank you! Checklist verified.** :
![debugresult](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/4-Chatbot/README_files/debugresult.png)

We will complete the code to build the requested scenario.

## Create a bot

Our goal is to code a bot to roll out a checklist, with differente steps.

Add the necessary to extend the functionality of this bot to the scenario below:

### Discover the source code

All of our changes will be made in the Checklist.cs file, open this file. Note the presence of the Checklist class.

You can notice:

* the presence of the property:
```chsarp
public string TechnicianId { get; set; }
```

### Add enums

### Add properties

### Modify the form

## Congratulations you finished this part !

## To continue further

## Documentation