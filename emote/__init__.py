#!/bin/env python
#   Copyright 2016 Matthew Ralston
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Author: Matt Ralston
# Date: 1/31/16
# Description:

####################
# PACKAGES
####################
import os
#import argparse
import copy
import sys
#import ConfigParser
import logging
import logging.config

#import click
import inquirer

####################
# CONSTANTS
####################

"""
The emotions used here were taken from a variety of 'emotional wheels' available by using Google search for 'emotion wheel' and viewing image results.

Most adjectives shown here were taken from 'humansystems.co' and used under Fair Use of their Copyright.
"""

positive_keywords = [
    "Excited",
    "Interested",
    "Confident",
    "Loving",
    "Accepted"
]

negative_keywords = [
    "Angry",
    "Afraid",
    "Alone",
    "Sad",
    "Embarassed",
    "Dislike",
]


positive = {
    "Loving": [
        # Wheel level 2
        "Joyful",
        "Gratified",
        "Content",
        "Tolerant",
        "Caring",
        "Committed",
        "Accepting",
        "Grateful",
        "Generous",
        # Wheel level 3
        "Free",
        "Fulfilled",
        "Thankful",
        "Pleased",
        "Peaceful",
        "Warm",
        "Benevolent",
        "Amiable",
        "Considerate",
        "Devoted",
        "Faithful",
        "Doting",
        "Respectful",
        "Friendly",
        "Humbled",
        "Beneficient",
        "Willing",
        "Kindhearted",
    ],
    "Excited": [
        # Wheel level 2
        "Amazed",
        "Surprised",
        "Energetic",
        "Aroused",
        "Moved",
        "High",
        "Expectant",
        "Charged",
        # Wheel level 3
        "Astonished",
        "Awed",
        "Delighted",
        "Thrilled",
        "Eager",
        "Enthusiastic",
        "Passionate",
        "Stimulated",
        "Stirred",
        # "Afflame", # nope
        #"Roused", # nah
        "Awakened",
        "Piqued",
        "Fired up",
        "Animated",
     ],
    "Interested": [
        "Constructive",
        # Wheel level 2
        "Sensitive",
        "Intrigued",
        "Allured",
        "Intimate",
        "Attracted",
        "Creative",
        "Curious",
        "Playful",
        # Wheel level 3
        "Responsive",
        "Receptive",
        "Beguiled",
        "Fascinated",
        "Enticed",
        "Drawn",
        "Attentive",
        "Romantic",
        "Infatuated",
        "Captivated",
        "Inspired",
        "Thoughtful",
        "Inquisitive",
        "Feisty",
        "Cheeky"
    ],
    "Confident": [
        # Wheel level 2
        "Constructive",
        "Trusting",
        "Positive",
        "Fearless",
        "Truthful",
        "Optimistic",
        "Bold",
        "Powerful",
        "Proud",
        # Wheel level 3
        "Earnest",
        "Assured",
        "Convinced",
        "Senguine",
        "Sure",
        "Dauntless",
        "Authentic",
        "Honest",
        "Upbeat",
        "Hopeful",
        "Brave",
        "Courageous",
        "Self-reliant",
        "Independent",
        "Magnanimous",
        "Expansive",
        "Self-assured"
    ],
    "Accepted": [
        # Wheel level 2
        "Invited",
        "Attractive",
        "Loved",
        "Honored",
        "Popular",
        "Cooperative",
        "Respected",
        # Wheel level 3
        "Wanted",
        "Needed",
        "Interesting",
        "Beautiful",
        "Favored",
        "Appreciated",
        "Precious",
        "Cherished",
        "Important",
        "Esteemed",
        "Admired",
        "In Demand",
        "Constructive",
        "Helpful",
        "Valued",
        "Validated",
    ]
}

negative = {
    "Afraid": [
        # Wheel level 2
        "Apprehensive",
        "Stressed",
        "Worried",
        "Inadequate",
        "Confused",
        "Threatened",
        "Helpless",
        # WHeel level 3
        "Timid",
        "Nervous",
        "Overwhelmed",
        "Desperate",
        "Anxious",
        "Alarmed",
        "Incompetent",
        "Insecure",
        "Perturbed",
        "Bewildered",
        "Intimidated",
        "Imperiled",
        "Powerless",
        "Out of control"
        # Extras
        "Apathetic",
        "Bored",
        "Discouraged",
    ],
    "Embarassed": [
        # Wheel level 2
        "Disrespected",
        "Worthless",
        "Sheepish",
        "Ashamed",
        "Guilty",
        "Inferior",
        # Wheel level 3
        "Dishonored",
        "Ridiculed",
        "Insignificant",
        "Useless",
        "Remorseful",
        "Repentant",
        "Contrite",
        "Abashed",
        "Mortified",
        "Humiliated",
        "Weak",
        "Small",
        # Extras
        "Discouraged",
        "Vulnerable",
        "Exposed",
        "Friendless",
        "Submissive",
        "Scandalized",
    ],
    "Angry": [
        # Wheel level 2
        "Offended",
        "Indignant",
        "Dismayed",
        "Bitter",
        "Frustrated",
        "Aggressive",
        "Harassed",
        "Rushed",
        # Wheel level 3
        "Insulted",
        "Mocked",
        "Violated",
        "Outraged",
        "Let down",
        "Betrayed",
        "Resentful",
        "Jealous",
        "Annoyed",
        "Infuriated",
        "Hostile",
        "Belligerent",
        "Pressured",
        "Pushed"
    ],
    "Alone": [
        # Wheel level 2
        "Distant",
        "Lonely",
        "Excluded",
        "Fragile",
        "Abandoned",
        "Desolate",
        # Wheel level 3
        "Withdrawn",
        "Detached",
        "Isolated",
        "Forlorn",
        "Deserted",
        "Forsaken",
        "Rejected",
        "Friendless",
        "Bleak",
        "Desolate",
    ],
    "Sad": [
        # Wheel level 2
        "Depressed",
        "Hurt",
        "Bereft",
        "Melancholy",
        "Subdued",
        "Aggrieved",
        "Discouraged"
        # Wheel level 3
        "Morose",
        "Despondent",
        "Deflated",
        "Injured",
        "Discouraged",
        "Inconsolable",
        "Mournful",
        "Sorrow",
        "Gloomy",
        "Somber",
        "Agonized",
        "Wounded",
        "Crestfallen",
        "Broken",
        # Extras
        "Bleak",
        "Desolate",
        "Submissive",
    ],
    "Dislike": [
        # Wheel level 2
        "Dismissive",
        "Disgusted",
        "Suspicious",
        "Appalled",
        "Repelled",
        "Skeptical",
        # Wheel level 3
        "Contemptuous",
        "Disdainful",
        "Revolted",
        "Disturbed",
        "Scandalized",
        "Sickened",
        "Aghast",
        "Loathe",
        "Critical",
        "Disapproving",
    ]
}



####################
# FUNCTIONS
####################
# @click.command()
# @click.option("--emotions", prompt="Choose:", help="Choose a positive emotion")
def prompt_for_elaboration(emotion, emotion_dictionary):
    if type(emotion) is not str:
        raise TypeError("emote.prompt_for_elaboration requires an emotion as a 'str' as its first positional argument")
    elif type(emotion_dictionary) is not dict:
        raise TypeError("emote.prompt_for_elaboration requires an emotion dictionary as a 'dict' as its second positional argument")
    elif emotion not in emotion_dictionary.keys():
        raise ValueError("emote.prompt_for_elaboration requires the emotion str to be a valid member of the emotion dictionary")
    
    return inquirer.Checkbox(
        emotion,
        message="You said you feel {0}... care to elaborate?".format(emotion),
        choices=emotion_dictionary[emotion]
    )



def get_emotions():
    """
    Prompt for initial emotions to elaborate on
    """
    select_initial_emotions = [
        inquirer.Checkbox(
            'positive_emotions',
            message="Select positive emotions:",
            choices=positive_keywords
        ),
        inquirer.Checkbox(
            'negative_emotions',
            message="Select negative emotions:",
            choices=negative_keywords
        ),
    ]
    initial_emotions = inquirer.prompt(select_initial_emotions)
    if not initial_emotions:
        raise ValueError("Didn't have any feels?")
    # Clone the positive/negative emotions for later
    all_positive_adjs = copy.deepcopy(initial_emotions['positive_emotions'])
    all_negative_adjs = copy.deepcopy(initial_emotions['negative_emotions'])
    # Specify top-level list of prompts for 'elaborations'
    elaborations = []
    # Specify top-level list of adjectives
    

    """
    Now, select more specific adjectives
    """
    # positive_emotions = answers['positive_emotions']
    # negative_emotions = answers['negative_emotions']
    #  Store the prompts for each positive initial emotion in 'elaborations'
    if len(initial_emotions['positive_emotions']) > 0:
            
        sys.stderr.write("Great! You've got good vibes: {0}\n\n".format(initial_emotions['positive_emotions']))
        for e in initial_emotions['positive_emotions']:
            adj_q = prompt_for_elaboration(e, positive)
            elaborations.append(adj_q)
    #  Store the prompts for each negative initial emotion in 'elaborations'
    if len(initial_emotions['negative_emotions']) > 0:
        sys.stderr.write("Shiieeee... You've got some Negative energies: {0}\n\n".format(initial_emotions['negative_emotions']))
        for e in initial_emotions['negative_emotions']:
            adj_q = prompt_for_elaboration(e, negative)
            elaborations.append(adj_q)
    """
    Ask the user to elaborate on each initially selected emotion.
    """
    specific_adjs = inquirer.prompt(elaborations)
    for e in (initial_emotions['positive_emotions'] + initial_emotions['negative_emotions']):
        adjs = specific_adjs[e]
        sys.stderr.write("You said you feel '{0}'...more specifically: {1}\n".format(e, ', '.join(adjs)))
        if e in initial_emotions['positive_emotions']:
            all_positive_adjs += adjs
        elif e in initial_emotions['negative_emotions']:
            all_negative_adjs += adjs


    sys.stderr.write("\n\nSummarizing:\n\n")
    sys.stderr.write("You felt a good way today: {0}\n".format(all_positive_adjs))
    sys.stderr.write("You had things on your mind: {0}\n".format(all_negative_adjs))
    return all_positive_adjs, all_negative_adjs


def main():
    positive_emotions, negative_emotions = get_emotions()



def cli():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--required', help="Required argument",required=True)
    # parser.add_argument('--flag', help="This is a flag",action="store_true")
    # parser.add_argument('-v, --verbose', help="Prints warnings to console by default",default=0, action="count")
    # args = parser.parse_args()
    # Main routine
    main()


####################
# OPTIONS AND MAIN
####################

if __name__ == '__main__':
    cli()

