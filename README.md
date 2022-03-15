# PGCDiscordBot
This is a first dive into writing a Discord Bot. The motivation for this Bot was to provide the necessary URL links relevant to League of Legends champions, their moveset, and recommended build for ARAM. However, additional functionality will be added to this bot as desirable features are brought forward. 

## How to Use
The following commands are supported by the PGC Discord Bot
* `!lol <champ_name>`
  * The command keyword here to alert the bot is `!lol`. It then parses the provided champ name and outputs the recommended pages for champion moveset and builds for ARAM.
* `!joke`
  * The command keyword here to alert the bot is `!joke`. It then generates a random dad joke from `data\dadjokes.txt`. 
  * TODO: Future goals include adding a rating for the joke to improve joke selection (e.g. weighting)

## LoL Scraping
In this Jupyter Notebook, we use the LoL wiki to parse all of the valid Champions currently in League of Legends. We also go about formatting and mapping the champion names to the relevant URLs for movesets and builds. 

## LoL Fuzzy Matching
In this Jupyter Notebook, we use the Jaro-Winkler distance metric to provide the best match for the user's input to the aforementioned preprocessed champion names. The Jaro-Winkler distance metric was used here due to the higher weight put on the beginning of the string. This same matching algorithm is currently being used in `discordbot.py`.
  * It's also worth noting that `Nunu & Willump` is typically shortened to `Nunu` - there might be an issue with matching if trying to do the whole term. 
