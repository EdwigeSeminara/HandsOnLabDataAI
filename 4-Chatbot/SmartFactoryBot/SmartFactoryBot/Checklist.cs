using Microsoft.Bot.Builder.Dialogs;
using Microsoft.Bot.Builder.FormFlow;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Globalization;
using System.Linq;
using System.Threading;
using System.Web;

namespace SmartFactoryBot
{
    [Serializable]
    [Template(TemplateUsage.NotUnderstood,
        "Sorry, I didn't get that.",
        "Please try again",
        "My apologies, I didn't understand \"{0}\".",
        "I don't understand \"{0}\".",
        "Excuse me but I'm a chatbot and don't know \"{0}\".",
        "Try again, I don't get \"{0}\".")]
    public class Checklist
    {
        public string TechnicianId { get; set; }

        private static ConcurrentDictionary<CultureInfo, IForm<Checklist>> _forms = new ConcurrentDictionary<CultureInfo, IForm<Checklist>>();

        public static IForm<Checklist> BuildForm()
        {
            var culture = Thread.CurrentThread.CurrentUICulture;
            IForm<Checklist> form;

            if (!_forms.TryGetValue(culture, out form))
            {
                OnCompletionAsyncDelegate<Checklist> processChecklist = async (context, state) =>
                {
                    await context.PostAsync("We are currently processing your checklist. We will message you the status.");
                };

                var formBuilder = new FormBuilder<Checklist>();
                formBuilder
                        .Message("Hello, my name is Chuck the checkbot !")
                        .Field(nameof(TechnicianId))
                        .Message("Thank you");

                formBuilder.Configuration.DefaultPrompt.ChoiceStyle = ChoiceStyleOptions.Auto;
                form = formBuilder.Build();
                _forms[culture] = form;
            }
            return form;
        }

        
    }
}