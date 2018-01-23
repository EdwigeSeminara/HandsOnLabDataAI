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
5. In the "**Bot Url**" field, write the port that you noted in step 3
6. Do not change the other fields
7. In the text box at the bottom of the emulator, enter **hello**
8. Your **hello** appears in the chat area
9. The bot answers by welcoming you and asking for your technician id
10. Enter your technician id. The bot displays the message **Thank you! Checklist verified.** :
![debugresult](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/4-Chatbot/README_files/debugresult.png)

We will complete the code to build the requested scenario.

## Create a bot

Our goal is to code a bot to roll out a checklist, with differente steps.

Add all required items to extend the functionality of this bot to the scenario below:
1. Specify the machine id
2. Specify the machine type
3. Enter the state of the 3 main checkpoints of the machine (ok / ko)
4. Ask the user for another remark
5. Ask if the problem is solved
6. Thank the user for his intervention

### Explore the source code

All of our changes will be made in the Checklist.cs file, open this file. Note the presence of the Checklist class.

You can notice:

* the presence of the property:
```csharp
public string TechnicianId { get; set; }
```
* the form builder : 
```csharp
public string TechnicianId { get; set; }
```

What you need to understand:

* each question asked by the bot will be defined by a property similar to the TechnicianId property
* in the case of a multiple-choice question, choices offered to the user are defined by an enum
* the "loop" of the form is simply defined in a chained way

Now let's go!

### Add enums

In the file named **Checklist.cs** (**outside** the Checklist class) :
* Add an enum to handle the machine type:
```csharp
        public enum MachineTypeOptions
        {
            [Display(Name = "Type 1")]
            Type1,
            [Display(Name = "Type 2")]
            Type2,
            [Display(Name = "Type 3")]
            Type3,
            [Display(Name = "Type 4")]
            Type4
        };
```

* Add an enum to define the checkpoint verification:
```csharp
        public enum CheckpointVerificationOptions
        {
            OK,
            KO
        };
```

* Add an enum to specitify other remarks about the machine health:
```csharp
        public enum OtherRemarksOptions
        {
            Yes,
            No
        };
```

Now let's add the properties!

### Add properties

In the **Checklist.cs** file (**inside** the Checklist class) :

* Add a property for the machine id:
```csharp
	[Prompt("Enter the serial number of the machine")]
        [Pattern(@"[0-9]")]
        public string MachineId { get; set; }
```

* Add a property to handle the machine type:
```csharp
       [Prompt("Please specify the machine type {||}")]
       public MachineTypeOptions? MachineType;
```

* Add a property to specifiy the first checkpoint health:
```csharp
       [Prompt("Please check the first checkpoint of the machine and enter your result {||}")]
       public CheckpointVerificationOptions? FirstCheckpoint;
```

* Add a property to ask the second checkpoint health:
```csharp        
	[Prompt("Please check the second checkpoint of the machine and enter your result {||}")]
        public CheckpointVerificationOptions? SecondCheckpoint;
```

* Add a property to check the third checkpoint health:
```csharp
        [Prompt("Please check the third checkpoint of the machine and enter your result {||}")]
        public CheckpointVerificationOptions? ThirdCheckpoint;
```

* Add a property to enable the user to enter additional remarks about the machine health:
```csharp
        [Optional]
        [Prompt("Do you see something wrong on the machine which can help for the future ? {||}")]
        [Template(TemplateUsage.NoPreference, "Skip this step")]
        public OtherRemarksOptions? OtherRemarks;
```

* Decore the technician id property this way:
```csharp
	[Prompt("Enter your technican id")]
        [Pattern(@"[0-9]")]
        public string TechnicianId { get; set; }
```

What you must remember :

* the **Prompt** attribute defines the sentence used by the bot to query the user
* the **Optional** attribute makes a question optional and gives the ability to skip the current step
* the **Pattern** attribute defines the expected response format
* the **Template** attribute lets you specify the template used for a property

Let's change the form now to get to our scenario!

### Modify the form

In the Checklist class, go to the BuildForm method, after the line **.Field(nameof(TechnicianId))**:

* Ask the machine id:
```csharp
.Field(nameof(MachineId))
```

* Ask the machine type:
```csharp
.Field(nameof(MachineType))
```

* Ask to check the first checkpoint:
```csharp
.Field(nameof(FirstCheckpoint),
    validate: async (state, value) =>
    {
        return CheckpointVerificationProcess(state, value);
    })
```

* Ask to check the second checkpoint:
```csharp
.Field(nameof(SecondCheckpoint),
    validate: async (state, value) =>
    {
        return CheckpointVerificationProcess(state, value);
    })
```

* Ask to check the third checkpoint:
```csharp
.Field(nameof(ThirdCheckpoint),
    validate: async (state, value) =>
    {
        return CheckpointVerificationProcess(state, value);
    })
```

* Ask the user to specify other remarks about machine health if necessary:
```csharp
.Field(nameof(OtherRemarks))
```

* Ask if the problem is solved:
```csharp
.Confirm(async (state) =>
    {
        var customMessage = "Problem solved, is it ok?";
        return new PromptAttribute(customMessage);
    })
```

* Add this code to handle the choice **"Skip this step"** otherwise it will not be recognized by the bot:
```csharp
var formBuilder = new FormBuilder<Checklist>();
var noPreferenceTerms = formBuilder.Configuration.NoPreference.ToList();
noPreferenceTerms.Add("Skip this step");
formBuilder.Configuration.NoPreference = noPreferenceTerms.ToArray();
```

* And finally, add this method outside the Buildform method:
```csharp
protected static ValidateResult CheckpointVerificationProcess(Checklist state, object value)
{
    string response = "Thanks for your check.";
    var result = new ValidateResult { IsValid = true, Value = value };

    if (value != null)
    {
        if (!string.IsNullOrEmpty(value.ToString()))
        {
            if (value.ToString() == CheckpointVerificationOptions.KO.ToString())
            {
                result.IsValid = false;
                result.Feedback = string.Concat(response, " Please fix the problem by running procedure for first checkpoint and perform a check again");
            }
            else
            {
                result.Feedback = string.Concat(response, " next step...");
            }
        }
    }

    return result;
}
```

* Thank the user for his intervention:
```csharp
.Message("Thank you");
```

Compile, run and test the bot with the emulator!

Here is the result you should get:

![result_1](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/4-Chatbot/README_files/result_1.png)

![result_2](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/4-Chatbot/README_files/result_2.png)

![result_3](https://github.com/EdwigeSeminara/HandsOnLabDataAI/blob/master/4-Chatbot/README_files/result_3.png)

## Congratulations you finished this part !

## To go further

After completing this part you can go further and perform this points:
* Add Cortana skills
* Deploy your bot to the cloud
* Register your bot with Bot Service
* Use it in a cross-platform app thanks to DirectLine 3.0

Feel free to customize it by yourself !

## Documentation
* **[Bot Service documenation](https://docs.microsoft.com/en-us/bot-framework/)**
* **[Bot Builder for .NET](https://docs.microsoft.com/en-us/bot-framework/dotnet/bot-builder-dotnet-quickstart)**
* **[Bot Framework source code](https://github.com/Microsoft/BotFramework-Emulator)**
* **[Register a bot with Bot Service](https://docs.microsoft.com/en-us/Bot-Framework/bot-service-quickstart-registration)**
* **[Connect a bot to Direct Line](https://docs.microsoft.com/en-us/bot-framework/bot-service-channel-connect-directline)**