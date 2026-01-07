from flask import Flask, render_template, request, session, redirect
import random
import json
import os
import time
import difflib

app = Flask(__name__)
app.secret_key = "super-secret-key-change-this"

ADMIN_PASSWORD = "GenzLovesRomanticizingEverything"  

DATA_DIR = "data"
PENDING_FILE = os.path.join(DATA_DIR, "pending_words.json")
APPROVED_FILE = os.path.join(DATA_DIR, "approved_words.json")

os.makedirs(DATA_DIR, exist_ok=True)

if not os.path.exists(PENDING_FILE):
    with open(PENDING_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(APPROVED_FILE):
    with open(APPROVED_FILE, "w") as f:
        json.dump({}, f)

def find_similar_words(query, words):
    return difflib.get_close_matches(
        query.lower(),
        words,
        n=5,        # number of suggestions
        cutoff=0.6  # similarity threshold
    )

def load_dictionary():
    dictionary = {
        "sus": {
            "short": "Suspicious or shady",
            "explanation": "Used to describe someone or something acting suspiciously.",
            "example": "He said he didn’t take the cookie, but that’s kinda sus."
        },
        "yeet": {
            "short": "To throw or move quickly",
            "explanation": "Used when tossing something or expressing excitement.",
            "example": "He yeeted the ball across the yard!"
        },
        "cap": {
            "short": "Lie or false statement",
            "explanation": "Used to call out someone who is lying.",
            "example": "He said he won the game, but that’s cap."
        },
        "stan": {
            "short": "Super fan",
            "explanation": "To strongly support someone or something.",
            "example": "I totally stan that new singer!"
        },
        "vibe": {
            "short": "Mood or feeling",
            "explanation": "Refers to the overall feeling of a person, place, or thing.",
            "example": "This cafe has a chill vibe."
        },
        "simp": {
            "short": "Overly affectionate person",
            "explanation": "Someone who goes overboard to impress another person.",
            "example": "He bought her flowers every day, what a simp!"
        },
        "flex": {
            "short": "Show off",
            "explanation": "To brag about something in a flashy way.",
            "example": "He’s always trying to flex his new shoes."
        },
        "no cap": {
            "short": "No lie / seriously",
            "explanation": "Used to emphasize truthfulness.",
            "example": "That concert was amazing, no cap!"
        },
        "lit": {
           "short": "Exciting or amazing",
            "explanation": "Describes something that’s fun, energetic, or excellent.",
            "example": "The party last night was lit!"
        },
        "salty": {
            "short": "Bitter or annoyed",
            "explanation": "Being upset or irritated about something small.",
            "example": "She’s salty because she lost the game."
        },
        "lowkey": {
            "short": "Secretly or quietly",
            "explanation": "Something you don’t want to announce loudly.",
            "example": "I’m lowkey excited for the exam."
        },
        "highkey": {
            "short": "Clearly or openly",
            "explanation": "Something that is obvious or not hidden.",
            "example": "I highkey love this song!"
        },
        "mood": {
            "short": "Relatable feeling",
            "explanation": "Used to express something you relate to.",
            "example": "Sleeping all day is a mood."
        },
        "tea": {
            "short": "Gossip",
            "explanation": "Information, rumors, or juicy news.",
            "example": "Spill the tea about what happened yesterday!"
        },
        "slaps": {
            "short": "Really good",
            "explanation": "Usually for music, meaning it’s excellent.",
            "example": "This new song slaps!"
        },
        "shook": {
            "short": "Surprised or shocked",
            "explanation": "Feeling amazed or startled by something.",
            "example": "I was shook after watching that movie."
        },
        "fam": {
            "short": "Close friends",
            "explanation": "Refers to your trusted circle of friends.",
            "example": "What’s up, fam?"
        },
        "bop": {
            "short": "Catchy song",
            "explanation": "A song that’s fun and easy to listen to.",
            "example": "This new track is a bop!"
        },
        "drip": {
            "short": "Stylish or trendy",
            "explanation": "Refers to someone’s fashion sense or outfit.",
            "example": "Check out his drip!"
        },
        "snatched": {
            "short": "Looking great",
            "explanation": "Usually about appearance or style.",
            "example": "Her outfit is snatched."
        },
        "receipts": {
            "short": "Proof or evidence",
            "explanation": "Used to back up claims, especially in gossip.",
            "example": "I got receipts for what she said!"
        },
        "cheugy": {
            "short": "Outdated or trying too hard",
            "explanation": "Something that isn’t trendy anymore.",
            "example": "That outfit is kinda cheugy."
        },
        "meme": {
            "short": "Funny internet content",
            "explanation": "A humorous picture, video, or text shared online.",
            "example": "I can’t stop laughing at this meme!"
        },
        "snack": {
            "short": "Attractive person",
            "explanation": "Someone who looks good or appealing.",
            "example": "He’s a whole snack!"
        },
        "woke": {
            "short": "Socially aware",
            "explanation": "Being conscious of social issues.",
            "example": "She’s really woke about environmental issues."
        },
        "extra": {
            "short": "Over the top",
            "explanation": "Doing too much in an unnecessary way.",
            "example": "He’s so extra with his party decorations."
        },
        "bet": {
            "short": "Agreement or affirmation",
            "explanation": "Used like 'okay' or 'you got it'.",
            "example": "Can you pick me up at 8? Bet."
        },
        "cheese": {
            "short": "Smile",
            "explanation": "To grin widely, usually for a photo.",
            "example": "Say cheese!"
        },
        "fit": {
            "short": "Outfit",
            "explanation": "Refers to someone’s clothing or style.",
            "example": "That fit is fire!"
        },
        "sksksk": {
            "short": "Excited expression",
            "explanation": "Used to express excitement or laughter.",
            "example": "Sksksk I can’t believe it!"
        },
        "finna": {
            "short": "Going to",
            "explanation": "Short for 'fixing to', meaning about to do something.",
            "example": "I’m finna leave soon."
        },
        "cringe": {
            "short": "Embarrassing or awkward",
            "explanation": "Something that causes secondhand embarrassment.",
            "example": "That dance move was so cringe."
        },
        "glow up": {
            "short": "Transformation for the better",
            "explanation": "Improving appearance or style over time.",
            "example": "She had a major glow up this year."
        },
        "ok boomer": {
            "short": "Dismissive phrase",
            "explanation": "Used to dismiss outdated opinions.",
            "example": "He said homework is pointless—ok boomer."
        },
        "okurrr": {
            "short": "Expression of excitement",
            "explanation": "Popularized by Cardi B, used to affirm something.",
            "example": "We’re going to the concert, okurrr!"
        },
        "goat": {
            "short": "Greatest of all time",
            "explanation": "Used to describe someone excellent at something.",
            "example": "She’s the GOAT at chess."
        },
        "deadass": {
            "short": "Seriously / for real",
            "explanation": "Used to emphasize truth.",
            "example": "I’m deadass tired right now."
        },
        "pog": {
            "short": "Exciting or awesome",
            "explanation": "Used in gaming communities for hype moments.",
            "example": "That play was pog!"
        },
        "rip": {
            "short": "Rest in peace / sad",
            "explanation": "Used when something bad happens or someone dies.",
            "example": "RIP my phone, it fell in water."
        },
        "ratio": {
            "short": "Social media metric",
            "explanation": "When a post gets more replies than likes, often negative.",
            "example": "Your tweet got ratioed."
        },
        "bussin": {
            "short": "Really good",
            "explanation": "Usually refers to food or something impressive.",
            "example": "This pizza is bussin!"
        },
        "main character": {
            "short": "Center of attention",
            "explanation": "Feeling like the protagonist of your own life.",
            "example": "She’s living her best main character life."
        },
        "quiet quitting": {
            "short": "Doing the bare minimum at work",
            "explanation": "Not overextending yourself professionally.",
            "example": "He’s quiet quitting, only finishing assigned tasks."
        },
        "boujee": {
            "short": "Fancy or high-class",
            "explanation": "Used for someone who acts upscale or pretentious.",
            "example": "She’s so boujee, always at the nicest cafes."
        },
        "cancel culture": {
            "short": "Public shaming",
            "explanation": "The practice of socially boycotting someone after a mistake or controversial action.",
            "example": "The influencer faced cancel culture after their tweet."
        },
        "capper": {
            "short": "Someone who lies",
            "explanation": "A person who exaggerates or isn’t truthful.",
            "example": "He said he got 100% on the test, what a capper."
        },
        "clap back": {
            "short": "Sharp response",
            "explanation": "A witty or fierce reply, usually to criticism.",
            "example": "She clapped back at the rude comment perfectly."
        },
        "cuffed": {
            "short": "In a relationship",
            "explanation": "Being romantically attached to someone.",
            "example": "He’s cuffed now, so he’s off the market."
        },
        "dime": {
            "short": "Perfect 10 / attractive person",
            "explanation": "Refers to someone who is extremely attractive.",
            "example": "She’s a dime, no doubt."
        },
        "drama llama": {
            "short": "Overly dramatic person",
            "explanation": "Someone who exaggerates problems or emotions.",
            "example": "Stop being a drama llama, it’s not that serious."
        },
        "fam jam": {
            "short": "Family gathering",
            "explanation": "Used for a fun get-together with family or close friends.",
            "example": "We had a little fam jam over the weekend."
        },
        "finsta": {
            "short": "Fake Instagram",
            "explanation": "A secondary Instagram account for private posts.",
            "example": "I only post funny memes on my finsta."
        },
        "fit check": {
            "short": "Outfit inspection",
            "explanation": "Showing off what you’re wearing.",
            "example": "Let me do a quick fit check before we leave."
        },
        "gaslight": {
            "short": "Manipulate someone",
            "explanation": "Make someone doubt their own reality or sanity.",
            "example": "He tried to gaslight her into thinking she was wrong."
        },
        "ghosting": {
            "short": "Sudden disappearance",
            "explanation": "Cutting off communication with someone without explanation.",
            "example": "He ghosted after our second date."
        },
        "hits different": {
            "short": "Feels unique or intense",
            "explanation": "Something that impacts you emotionally in a distinct way.",
            "example": "This song hits different at night."
        },
        "humblebrag": {
            "short": "Brag disguised as modesty",
            "explanation": "Pretending to be modest while boasting.",
            "example": "She humblebragged about her new car."
        },
        "iconic": {
            "short": "Memorable or legendary",
            "explanation": "Something widely recognized as impressive or important.",
            "example": "That scene from the movie is iconic."
        },
        "ig": {
            "short": "Instagram",
            "explanation": "Short for Instagram.",
            "example": "Check out my new post on IG."
        },
        "influencer": {
            "short": "Social media personality",
            "explanation": "Someone who promotes products or ideas online.",
            "example": "She’s a popular fashion influencer."
        },
        "karen": {
            "short": "Entitled woman",
            "explanation": "Stereotype for someone acting demanding or privileged.",
            "example": "The lady at the store was acting like a total Karen."
        },
        "keeping it 100": {
            "short": "Being honest",
            "explanation": "Keeping things real or truthful.",
            "example": "I’m keeping it 100, that movie was terrible."
        },
        "lurk": {
            "short": "Watch without participating",
            "explanation": "Observing online activity silently.",
            "example": "I just lurk on Twitter sometimes."
        },
        "main account": {
            "short": "Primary social media account",
            "explanation": "The main profile someone posts publicly from.",
            "example": "I keep my selfies on my main account."
        },
        "mood af": {
            "short": "Relatable feeling, intensified",
            "explanation": "Used to emphasize how relatable something is.",
            "example": "Sleeping all day? Mood af."
        },
        "no chill": {
            "short": "Overreacting",
            "explanation": "Someone who cannot relax or calm down.",
            "example": "He’s so extra, no chill at all."
        },
        "on fleek": {
            "short": "Perfectly done",
            "explanation": "Used to describe appearance, especially eyebrows or outfits.",
            "example": "Her makeup is on fleek today."
        },
        "period": {
            "short": "End of discussion",
            "explanation": "Used to emphasize a point with no debate.",
            "example": "That’s the best movie ever, period."
        },
        "pov": {
            "short": "Point of view",
            "explanation": "Refers to perspective in a video or meme.",
            "example": "POV: You just finished finals."
        },
        "queen": {
            "short": "Amazing person",
            "explanation": "Used to praise someone, usually a woman.",
            "example": "You handled that so well, queen!"
        },
        "savage": {
            "short": "Bold or ruthless",
            "explanation": "Someone or something being impressively daring or fierce.",
            "example": "That comeback was savage."
        },
        "ship": {
            "short": "Support a relationship",
            "explanation": "Rooting for two people to be together romantically.",
            "example": "I totally ship them!"
        },
        "stan culture": {
            "short": "Fandom obsession",
            "explanation": "When fans aggressively support someone or something.",
            "example": "Stan culture can be intense on Twitter."
        },
        "stan twitter": {
            "short": "Community of obsessive fans",
            "explanation": "Part of Twitter dedicated to fandoms.",
            "example": "Stan Twitter went crazy over the new trailer."
        },
        "tbh": {
            "short": "To be honest",
            "explanation": "Used to express sincerity.",
            "example": "TBH, I didn’t like the movie."
        },
        "vibe check": {
            "short": "Test mood or energy",
            "explanation": "Assessing someone’s energy or behavior.",
            "example": "Vibe check: Are we ready for the party?"
        },
        "weird flex": {
            "short": "Unusual brag",
            "explanation": "Boasting about something strange or unexpected.",
            "example": "He owns 10 staplers—what a weird flex."
        },
        "wholesome": {
            "short": "Heartwarming or positive",
            "explanation": "Something that makes you feel good emotionally.",
            "example": "This video of puppies is wholesome."
        },
        "wypipo": {
            "short": "White people (playful)",
            "explanation": "Slang referring to white people, usually jokingly.",
            "example": "Wypipo love pumpkin spice lattes."
        },
        "yass": {
            "short": "Excited affirmation",
            "explanation": "Enthusiastic way of saying 'yes'.",
            "example": "Yass! That’s amazing news!"
        },
        "yikes": {
            "short": "Reaction to awkwardness",
            "explanation": "Used when something is shocking or cringy.",
            "example": "He tried to rap in class—yikes."
        },
        "zip it": {
            "short": "Be quiet",
            "explanation": "Telling someone to stop talking.",
            "example": "Zip it! I’m trying to concentrate."
        },
        "aesthetic": {
            "short": "Visually pleasing",
            "explanation": "Describes something that looks stylish, pretty, or artistically appealing.",
            "example": "Her desk setup is very aesthetic."
        },
        "ate": {
            "short": "Did amazingly well",
            "explanation": "Used to praise someone for an outstanding performance.",
            "example": "She ate that presentation."
        },
        "mid": {
            "short": "Average or unimpressive",
            "explanation": "Used when something is disappointing or not as good as expected.",
            "example": "That movie was mid."
        },
        "npc": {
            "short": "Unoriginal person",
            "explanation": "Refers to someone acting predictable or lacking individuality.",
            "example": "He just follows trends, total NPC."
        },
        "rizz": {
            "short": "Charm or flirting skill",
            "explanation": "The ability to attract others through charm or confidence.",
            "example": "He’s got insane rizz."
        },
        "caught in 4k": {
            "short": "Caught with proof",
            "explanation": "Someone is exposed with clear evidence.",
            "example": "He denied it but got caught in 4k."
        },
        "delulu": {
            "short": "Delusional thinking",
            "explanation": "Playfully describing unrealistic expectations or beliefs.",
            "example": "Thinking he’ll reply is delulu."
        },
        "corecore": {
            "short": "Chaotic internet aesthetic",
            "explanation": "Absurd, ironic remix of internet culture and trends.",
            "example": "That video is pure corecore."
        },
        "soft launch": {
            "short": "Subtle reveal",
            "explanation": "Hinting at something without fully announcing it.",
            "example": "She soft launched her relationship."
        },
        "hard launch": {
            "short": "Public announcement",
            "explanation": "Officially revealing something publicly.",
            "example": "They hard launched their relationship."
        },
        "touch grass": {
            "short": "Disconnect from internet",
            "explanation": "Telling someone to step away from online life.",
            "example": "You need to touch grass."
        },
        "side eye": {
            "short": "Judgmental look",
            "explanation": "A look expressing doubt or disapproval.",
            "example": "That comment got a side eye."
        },
        "it’s giving": {
            "short": "Expressing a vibe",
            "explanation": "Describes the feeling or impression something gives.",
            "example": "It’s giving confidence."
        },
        "girl dinner": {
            "short": "Low-effort meal",
            "explanation": "A casual or snack-based dinner.",
            "example": "Crackers and fruit—girl dinner."
        },
        "boy math": {
            "short": "Illogical reasoning",
            "explanation": "Joking way to describe flawed logic.",
            "example": "That explanation is boy math."
        },
        "girl math": {
            "short": "Spending logic",
            "explanation": "Playful justification for spending money.",
            "example": "It was on sale, girl math."
        },
        "unalive": {
            "short": "Euphemism for death",
            "explanation": "Used online to avoid sensitive language filters.",
            "example": "The character got unalive."
        },
        "chronically online": {
            "short": "Always online",
            "explanation": "Someone overly influenced by internet culture.",
            "example": "That take is chronically online."
        },
        "slay": {
            "short": "Perform excellently",
            "explanation": "Expresses confidence, success, or approval.",
            "example": "You slayed that look."
        },
        "based": {
            "short": "Confident and honest",
            "explanation": "Expressing an opinion without caring about approval.",
            "example": "That opinion was based."
        },
        "rent free": {
            "short": "Mentally stuck",
            "explanation": "When something occupies your thoughts constantly.",
            "example": "That song lives rent free in my head."
        },
        "say less": {
            "short": "Understood",
            "explanation": "Means no further explanation is needed.",
            "example": "You want food? Say less."
        },
        "ick": {
            "short": "Instant turn-off",
            "explanation": "A minor thing that ruins attraction.",
            "example": "That behavior gave me the ick."
        },
        "red flag": {
            "short": "Warning sign",
            "explanation": "Indicates possible danger or unhealthy behavior.",
            "example": "That’s a red flag."
        },
        "green flag": {
            "short": "Positive sign",
            "explanation": "Indicates good or healthy behavior.",
            "example": "Emotional maturity is a green flag."
        },
        "situationship": {
            "short": "Undefined relationship",
            "explanation": "Romantic involvement without commitment or clarity.",
            "example": "We’re in a situationship."
        },
        "pop off": {
            "short": "React strongly or succeed",
            "explanation": "To gain attention or respond energetically.",
            "example": "That post really popped off."
        },
        "fell off": {
            "short": "Lost popularity",
            "explanation": "No longer relevant or admired.",
            "example": "That app fell off."
        },
        "built different": {
            "short": "Uniquely strong",
            "explanation": "Someone exceptional or resilient.",
            "example": "She’s built different."
        },
        "that ain’t it": {
            "short": "Not good / not acceptable",
            "explanation": "Used when something is disappointing, cringey, or just not the right choice.",
            "example": "He said pineapple belongs on every food? Yeah… that ain’t it."
        },
        "coded": {
            "short": "Has a deeper meaning",
            "explanation": "Used when something subtly represents an identity, trait, or vibe without saying it directly.",
            "example": "Her outfit today is very main-character coded."
        },
        "dumpster fire": {
            "short": "A complete disaster",
            "explanation": "Used to describe a chaotic or horribly managed situation.",
            "example": "The group project turned into a total dumpster fire."
        },
        "slept on": {
            "short": "Underrated",
            "explanation": "Used when something or someone deserves more attention or praise.",
            "example": "This small artist is so slept on."
        },
        "main slayer": {
            "short": "The best / standout person",
            "explanation": "Refers to someone who consistently impresses or dominates in a situation.",
            "example": "She came to the party as the main slayer again."
        },
        "press": {
            "short": "Annoyed or upset",
            "explanation": "Meaning someone is bothered or affected by something.",
            "example": "Why you so press about his comment?"
        },
        "doing numbers": {
            "short": "Getting a lot of attention",
            "explanation": "Used when a post, video, or content gains high engagement.",
            "example": "Your reel is doing numbers right now!"
        },
        "understood the assignment": {
            "short": "Did something perfectly",
            "explanation": "Said when someone performs extremely well or fits the vibe perfectly.",
            "example": "She showed up in the perfect outfit — she understood the assignment."
        },
        "moments": {
            "short": "Iconic, memorable situations",
            "explanation": "Used to describe funny, emotional, or unforgettable snippets of life.",
            "example": "Our vacation had so many moments."
        },
        "face card": {
            "short": "Attractive face",
            "explanation": "A playful way to say someone looks good.",
            "example": "Her face card stays valid."
        },
        "face card never declines": {
            "short": "Always attractive",
            "explanation": "Used to hype someone up whose looks never disappoint.",
            "example": "He walked in and wow… his face card never declines."
        },
        "micro-ick": {
            "short": "Small but annoying habit",
            "explanation": "A tiny behavior that suddenly turns someone off.",
            "example": "He says ‘hehe’ after every text… micro-ick."
        },
        "deep cut": {
            "short": "Obscure reference",
            "explanation": "Used when someone mentions something niche that not everyone will get.",
            "example": "Quoting that old meme is such a deep cut."
        },
        "soft girl": {
            "short": "Gentle, aesthetic vibe",
            "explanation": "A feminine aesthetic focused on softness, pastels, kindness, and calm energy.",
            "example": "Her soft girl era is so cute."
        },
        "clean girl": {
            "short": "Minimal, polished aesthetic",
            "explanation": "Refers to a neat, natural, skincare-focused, minimalist lifestyle or look.",
            "example": "Slicked bun, gold hoops, dewy skin — clean girl vibes."
        },
        "free me": {
            "short": "I want to escape",
            "explanation": "Used humorously when someone feels stuck, bored, or overwhelmed.",
            "example": "This lecture is two hours long… free me."
        },
        "hard watch": {
            "short": "Painful to watch",
            "explanation": "Used for videos, behavior, or content that is cringe or awkward.",
            "example": "That interview was a hard watch."
        },
        "soft block": {
            "short": "Block then unblock",
            "explanation": "A subtle way to make someone stop following you without alerting them much.",
            "example": "I had to soft block him — he kept lurking."
        },
        "hard block": {
            "short": "Full, permanent block",
            "explanation": "Completely blocking someone so they cannot contact or see you anymore.",
            "example": "He was toxic so I gave him the hard block."
        },
        "mutuals": {
            "short": "People who follow each other.",
            "explanation": "Used online to describe someone you follow and who also follows you back.",
            "example": "We’re mutuals now, so I can finally DM her."
        },
        "oomf": {
            "short": "One of my followers.",
            "explanation": "Refers to someone in your follower list without naming them.",
            "example": "Oomf needs to stop subtweeting."
        },
        "oomfie": {
            "short": "Cute/silly version of 'oomf'.",
            "explanation": "A playful way of referring to one of your followers.",
            "example": "Oomfie posted the funniest meme today."
        },
        "pilled": {
            "short": "Influenced by an idea.",
            "explanation": "Describes someone who strongly believes in or adopts a certain ideology or trend.",
            "example": "He’s totally gym-pilled now."
        },
        "low vibration": {
            "short": "Negative or draining energy.",
            "explanation": "Describes people or situations that feel unmotivating or toxic.",
            "example": "I’m avoiding low-vibration conversations today."
        },
        "high vibration": {
            "short": "Positive and uplifting energy.",
            "explanation": "Used for things that feel inspiring, healing, or joyful.",
            "example": "Her presence is so high vibration."
        },
        "they ate": {
            "short": "They did amazing.",
            "explanation": "Said when someone performs extremely well.",
            "example": "She ate that performance up."
        },
        "no thoughts just vibes": {
            "short": "Living without stress.",
            "explanation": "Means relaxing, not overthinking, and going with the flow.",
            "example": "Me on vacation: no thoughts, just vibes."
        },
        "hard disagree": {
            "short": "Strong disagreement.",
            "explanation": "Used online to show firm disagreement without being rude.",
            "example": "Pineapple on pizza is elite — hard disagree."
        },
        "soft disagree": {
            "short": "Gentle disagreement.",
            "explanation": "Used when you want to disagree politely.",
            "example": "Soft disagree, I think the first option was better."
        },
        "final boss": {
            "short": "Ultimate challenge/person.",
            "explanation": "Describes someone who is the strongest or most intimidating version of something.",
            "example": "That teacher is the final boss of exams."
        },
        "boss music": {
            "short": "Powerful dramatic moment.",
            "explanation": "Used when something feels intense or epic, like a video-game boss fight.",
            "example": "The sky got dark — cue the boss music."
        },
        "down horrendous": {
            "short": "Extremely desperate or embarrassed.",
            "explanation": "Often used when someone is acting overly obsessed with someone or doing something pitiful.",
            "example": "He liked all her pics from 2018… down horrendous."
        },
        "the audacity": {
            "short": "How dare they.",
            "explanation": "Used when someone does something bold or disrespectful.",
            "example": "He ate my fries — the audacity!"
        },
        "audacity of it all": {
            "short": "Extreme boldness.",
            "explanation": "A dramatic way of expressing disbelief at someone’s actions.",
            "example": "She blamed me for her mistakes — the audacity of it all."
        },
        "main character syndrome": {
            "short": "Acting overly self-centered.",
            "explanation": "Describes someone who behaves like the world revolves around them.",
            "example": "He narrated his whole day out loud… main character syndrome."
        },
        "internet archaeologist": {
            "short": "Someone who digs into old posts.",
            "explanation": "A person who finds and resurfaces old internet content or drama.",
            "example": "Internet archaeologists found her tweets from 2014."
        },
        "lore drop": {
            "short": "Revealing background info.",
            "explanation": "Used when someone suddenly shares deep personal backstory.",
            "example": "He told us about his childhood — major lore drop."
        },
        "deep in the lore": {
            "short": "Knowing all background details.",
            "explanation": "Means someone is very informed about a topic or drama.",
            "example": "She’s deep in the lore of that fandom."
        },
        "retcon": {
            "short": "Rewrite past events.",
            "explanation": "Changing the previously established story or facts, usually in media or fandom.",
            "example": "They retconned her backstory in season 2."
        },
        "rebrand": {
            "short": "Change your image.",
            "explanation": "Used when a person changes their style, vibe, or social persona.",
            "example": "New haircut, new wardrobe — she’s rebranding."
        },
        "irl": {
            "short": "In real life",
            "explanation": "Used to describe something happening offline and not on the internet.",
            "example": "We talk all day online but never met irl."
        },
        "sponsored behavior": {
            "short": "Acting like an ad",
            "explanation": "Used when someone behaves in a way that feels like they’re promoting something.",
            "example": "Drinking water every five minutes? Sponsored behavior."
        },
        "algorithm bait": {
            "short": "Content made for engagement",
            "explanation": "A post purposely crafted to get likes, comments, or views.",
            "example": "This dramatic caption is pure algorithm bait."
        },
        "chronically tired": {
            "short": "Always tired",
            "explanation": "A dramatic way to say someone is constantly exhausted.",
            "example": "I slept 10 hours but I'm still chronically tired."
        },
        "never beating the allegations": {
            "short": "Suspicious reputation",
            "explanation": "Said when someone keeps acting in a way that matches a rumor about them.",
            "example": "You say you don't like drama but you're never beating the allegations."
        },
        "big brain": {
            "short": "Smart moment",
            "explanation": "Used sarcastically or genuinely for clever behavior.",
            "example": "You brought snacks? Big brain move."
        },
        "small brain": {
            "short": "Dumb moment",
            "explanation": "Used when someone does something silly or clueless.",
            "example": "Forgot your own birthday? Small brain energy."
        },
        "out of pocket": {
            "short": "Wild behavior",
            "explanation": "Used when someone says/does something rude, bold, or unexpected.",
            "example": "That joke was out of pocket omg."
        },
        "call is coming from inside the house": {
            "short": "Problem is internal",
            "explanation": "Used when the issue is caused by the person complaining.",
            "example": "She said people are dramatic but she’s the one starting fights. Call is coming from inside the house."
        },
        "doing too much": {
            "short": "Overreacting",
            "explanation": "When someone behaves dramatically or puts unnecessary effort.",
            "example": "He wrote a 3-page text? He’s doing too much."
        },
        "doing nothing": {
            "short": "Lazy behavior",
            "explanation": "Used when someone is being unproductive or avoiding everything.",
            "example": "My weekend plans? Doing nothing."
        },
        "dry texting": {
            "short": "Boring messages",
            "explanation": "Texting with short, uninterested replies.",
            "example": "Why are you dry texting me? Say more than 'ok'."
        },
        "left on read": {
            "short": "Seen but ignored",
            "explanation": "When someone reads your message but doesn’t reply.",
            "example": "She left me on read for two hours."
        },
        "love that for you": {
            "short": "Happy for you",
            "explanation": "A supportive or sarcastic phrase depending on tone.",
            "example": "You got free food? Love that for you!"
        },
        "not me": {
            "short": "Exposing yourself",
            "explanation": "Used when playfully admitting something embarrassing.",
            "example": "Not me eating snacks at 3am."
        },
        "not very": {
            "short": "Doesn’t match the idea",
            "explanation": "Used when someone's behavior contradicts the image they claim.",
            "example": "You say you’re organized but your room is not very."
        },
        "screaming crying throwing up": {
            "short": "Overdramatic reaction",
            "explanation": "Exaggerated way to show extreme excitement or shock.",
            "example": "She liked my post??? Screaming crying throwing up."
        },
        "this is sick": {
            "short": "Amazing",
            "explanation": "Used to describe something extremely cool or impressive.",
            "example": "Your edit? This is sick."
        },
        "we listen and we don’t judge": {
            "short": "Supportive phrase",
            "explanation": "A humorous but comforting way to show non-judgment.",
            "example": "You ate 12 cookies? It’s okay, we listen and we don’t judge."
        },
        "gas": {
            "short": "Amazing",
            "explanation": "Something very good, exciting, or high-quality.",
            "example": "This song is gas."
        },
        "fire": {
            "short": "Super cool",
            "explanation": "Used for something excellent or impressive.",
            "example": "Your outfit is fire."
        },
        "copy paste personality": {
            "short": "No originality",
            "explanation": "Used when someone copies trends instead of being themselves.",
            "example": "Everyone has that water bottle… copy paste personality."
        },
        "plot armor": {
            "short": "Protected by luck",
            "explanation": "Used when someone repeatedly escapes consequences.",
            "example": "He didn’t study but still passed? Plot armor."
        },
        "side quest": {
            "short": "Random detour",
            "explanation": "Doing something unnecessary but fun.",
            "example": "I went out to buy milk and ended up at a café. Side quest."
        },
        "emotional support water bottle": {
            "short": "Always-carried bottle",
            "explanation": "A reusable bottle someone takes everywhere for comfort.",
            "example": "I can't leave without my emotional support water bottle."
        },
        "emotional damage": {
            "short": "Mentally hurt",
            "explanation": "A dramatic phrase for hurt feelings.",
            "example": "You embarrassed me in front of everyone… emotional damage."
        },
        "expired": {
            "short": "Outdated",
            "explanation": "Used when something is no longer trendy or relevant.",
            "example": "That meme is expired."
        },
        "expired take": {
            "short": "Old opinion",
            "explanation": "A viewpoint that was once relevant but isn't anymore.",
            "example": "Saying TikTok is for kids is such an expired take."
        },
        "loud wrong": {
            "short": "Confidently wrong",
            "explanation": "When someone is extremely wrong but speaks with confidence.",
            "example": "He argued for 10 minutes but was loud wrong."
        },
        "quiet wrong": {
            "short": "Subtly wrong",
            "explanation": "When someone is wrong but not aggressively.",
            "example": "She whispered the wrong answer. Quiet wrong."
        },
        "correct but annoying": {
            "short": "Correct but irritating",
            "explanation": "Used when someone is technically right but their comment feels irritating or unnecessary.",
            "example": "Ugh, you're correct but annoying for pointing that out."
        },
        "background character": {
            "short": "Someone unimportant",
            "explanation": "Describes someone acting like they have no main role in social situations.",
            "example": "He just stood in the corner like a background character."
        },
        "front row behavior": {
            "short": "Attention-seeking actions",
            "explanation": "Refers to someone acting overly eager or enthusiastic, like a student who sits in the front row.",
            "example": "Her correcting the teacher is real front row behavior."
        },
        "internet broke": {
            "short": "Huge viral moment",
            "explanation": "Used when a post or event becomes so big it feels like the internet stopped functioning.",
            "example": "Her outfit reveal literally broke the internet."
        },
        "algorithm fed": {
            "short": "The algorithm gave good recommendations",
            "explanation": "When the social media algorithm shows content that feels perfect for the user.",
            "example": "My feed is so good today, the algorithm really fed."
        },
        "soft reset": {
            "short": "Small life refresh",
            "explanation": "A light lifestyle change to feel refreshed, like cleaning, haircut, or reorganizing.",
            "example": "I’m doing a soft reset this weekend—cleaning my room and journaling."
        },
        "hard reset": {
            "short": "Full life restart",
            "explanation": "A major change to restart everything—new habits, environment, or lifestyle.",
            "example": "After that breakup, she went for a hard reset."
        },
        "delivered": {
            "short": "Performed amazingly",
            "explanation": "Used when someone meets or exceeds expectations.",
            "example": "She delivered with that performance!"
        },
        "crying in the club": {
            "short": "Overdramatic sadness",
            "explanation": "Used humorously to describe something unnecessarily emotional.",
            "example": "When I saw my grades… crying in the club."
        },
        "this aged poorly": {
            "short": "Didn’t hold up over time",
            "explanation": "Used when a past prediction or statement now looks very wrong.",
            "example": "He said crypto can’t lose value—this aged poorly."
        },
        "brand risk": {
            "short": "Something risky for reputation",
            "explanation": "Used when someone or something might damage a brand’s image.",
            "example": "Hiring him as an ambassador is a brand risk."
        },
        "chronicles": {
            "short": "A dramatic retelling",
            "explanation": "Used when someone narrates everyday events like they're epic stories.",
            "example": "Here she goes with the 7am commute chronicles."
        },
        "coded behaviour": {
            "short": "Hidden meaning actions",
            "explanation": "When someone's actions subtly reveal personality or intentions.",
            "example": "Drinking iced coffee in winter is coded behaviour."
        },
        "real one": {
            "short": "True loyal friend",
            "explanation": "Someone trustworthy, supportive, or genuine.",
            "example": "You brought me food? You're a real one."
        },
        "fake deep": {
            "short": "Pretending to be deep",
            "explanation": "Used for statements that sound philosophical but mean nothing.",
            "example": "‘Pain is just a concept’—okay, fake deep."
        },
        "peak": {
            "short": "Highest point",
            "explanation": "Used when something is the best moment or version.",
            "example": "This album is peak her."
        },
        "breadcrumbs": {
            "short": "Minimal attention",
            "explanation": "When someone gives tiny signs of interest to keep another person attached.",
            "example": "He’s not committed, he’s just giving breadcrumbs."
        },
        "main pop girl": {
            "short": "Top-tier female star",
            "explanation": "Refers to leading female artists dominating pop culture.",
            "example": "Dua Lipa is becoming the main pop girl."
        },
        "beige flag": {
            "short": "Mildly odd trait",
            "explanation": "A quirk that’s not a dealbreaker but makes you pause.",
            "example": "He collects hotel soaps—beige flag."
        },
        "villain era": {
            "short": "Selfish confidence phase",
            "explanation": "A period where someone prioritizes themselves unapologetically.",
            "example": "She stopped saying yes to everything—villain era."
        },
        "feral": {
            "short": "Uncontrollably chaotic",
            "explanation": "Used when someone acts wild or overly excited.",
            "example": "I went feral at the concert."
        },
        "unhinged": {
            "short": "Chaotic or irrational",
            "explanation": "When someone’s actions or jokes are wildly chaotic.",
            "example": "His tweets at 3am are unhinged."
        },
        "not the vibe": {
            "short": "Doesn’t feel right",
            "explanation": "Used when something feels off or undesirable.",
            "example": "That outfit with those shoes… not the vibe."
        },
        "core memory": {
            "short": "Unforgettable moment",
            "explanation": "A moment that will be remembered forever.",
            "example": "Childhood summers at my grandma’s were core memories."
        },
        "this you?": {
            "short": "Calling out hypocrisy",
            "explanation": "Used to point out someone's own contradictory behavior.",
            "example": "You said you hate drama? This you? *sends screenshot*"
        },
        "who asked": {
            "short": "No one wanted this info",
            "explanation": "A sarcastic reply when someone says something unnecessary.",
            "example": "‘I drink water differently’—okay but who asked?"
        },
        "low effort": {
            "short": "Minimal thought or work",
            "explanation": "Used when something looks rushed or not well done.",
            "example": "This thumbnail is so low effort."
        },
        "maximalist": {
            "short": "Loves excess",
            "explanation": "Someone who enjoys bold, decorative, or extravagant aesthetics.",
            "example": "Your room is so maximalist—colors everywhere!"
        },
        "minimalist": {
            "short": "Loves simplicity",
            "explanation": "Someone who prefers clean, simple, uncluttered styles.",
            "example": "Her wardrobe is so minimalist—just basics."
        },
        "inside voice": {
            "short": "Speak softly",
            "explanation": "A humorous way to tell someone to lower their volume.",
            "example": "Use your inside voice, you're yelling."
        },
        "outside voice": {
            "short": "Speaking loudly or boldly",
            "explanation": "Used when someone expresses something loud or dramatic.",
            "example": "That opinion was your outside voice!"
        },
        "media trained": {
            "short": "Speaks diplomatically",
            "explanation": "Describes someone who answers like a celebrity avoiding controversy.",
            "example": "Her response was so polite—she’s media trained."
        },
        "yapping": {
            "short": "Talking too much",
            "explanation": "Used when someone talks excessively or unnecessarily.",
            "example": "He’s been yapping for 20 minutes."
        },
        "yap session": {
            "short": "Long chat",
            "explanation": "A humorous way to describe a long conversation.",
            "example": "We had a whole yap session last night."
        },
        "brain empty": {
            "short": "No thoughts rn",
            "explanation": "Feeling mentally blank or tired.",
            "example": "After that exam, brain empty."
        },
        "full send": {
            "short": "Go all-in",
            "explanation": "Used when someone commits to something with full energy.",
            "example": "We’re doing it today—full send!"
        },
        "sending me": {
            "short": "Making me laugh hard",
            "explanation": "Used when something is extremely funny.",
            "example": "That meme is sending me."
        },
        "felt that": {
            "short": "Strongly relatable",
            "explanation": "A stronger version of ‘felt’.",
            "example": "‘I’m tired of everything’—felt that."
        },
        "soft era": {
            "short": "Gentle lifestyle phase",
            "explanation": "A period focusing on calmness, softness, and self-kindness.",
            "example": "I’m in my soft era—journaling and skincare daily."
        },
        "healing era": {
            "short": "Emotional recovery phase",
            "explanation": "Used when someone is actively working on personal healing.",
            "example": "She cut off toxic people—healing era."
        },
        "flop": {
            "short": "Failure or underperformance",
            "explanation": "Used when something doesn’t meet expectations.",
            "example": "That movie was a flop."
        },
        "bare minimum": {
            "short": "Doing the least possible",
            "explanation": "Refers to effort that is technically enough but unimpressive.",
            "example": "He washed one dish—bare minimum."
        },
        "side chick": {
            "short": "Secret romantic partner",
            "explanation": "Someone involved with a person who is already committed to another partner.",
            "example": "She didn’t know she was the side chick."
        },
        "6-7": {
            "short": "Viral hype phrase",
            "explanation": "A nonsense interjection used for excitement or hype, without fixed meaning.",
            "example": "6-7! That drop was wild!"
        },
        "pookie": {
            "short": "Term of endearment",
            "explanation": "Used for someone adorable or sweet.",
            "example": "Come here, pookie."
        },
        "I’m dead": {
            "short": "Something is extremely funny or shocking.",
            "explanation": "Used to say you’re laughing hard or can’t believe what just happened — not literal.",
            "example": "That plot twist came out of nowhere, I’m dead."
        },
        "it hits different": {
            "short": "Feels more intense or special than usual.",
            "explanation": "Used when something has a stronger emotional impact than expected, often because of mood, timing, or personal connection.",
            "example": "Listening to this song at night just hits different."
        },
        "sip tea": {  
            "short": "Watching drama without getting involved.",
            "explanation": "Used when someone observes gossip or chaos quietly instead of participating.",
            "example": "I’m not saying anything about this drama, just gonna sip tea."
        },
        "take an l": {
            "short": "Accepting a loss or failure.",
            "explanation": "Used when someone messes up, loses, or should admit they were wrong.",
            "example": "He missed the deadline again — just take the L and move on."
        },
        "i’m weak": {
            "short": "Something is extremely funny.",
            "explanation": "Used to say you’re laughing hard or can’t handle how funny something is.",
            "example": "That video was so funny, I’m weak."
        },
        "it's giving": {
            "short": "Suggests a strong vibe or impression.",
            "explanation": "Used to describe what something feels or seems like, often in a dramatic or expressive way.",
            "example": "That outfit? It’s giving main character energy."
        },
        "main character energy": {
            "short": "Feeling like the protagonist of your life.",
            "explanation": "Used when someone behaves confidently or dramatically, as if the world revolves around them.",
            "example": "She walked into the party like main character energy!"
        },
        "that's wild": {
            "short": "Crazy or unbelievable.",
            "explanation": "Used to react to something surprising, shocking, or hard to believe.",
            "example": "You finished the project in one day? That's wild!"
        },
        "af": {
            "short": "As f*** (intensifier).",
            "explanation": "Used to emphasize a statement or feeling strongly.",
            "example": "I’m tired af after that workout."
        },
        "clowning": {
            "short": "Acting foolish or ridiculous.",
            "explanation": "Used when someone is behaving silly, over-the-top, or making fun of themselves/others.",
            "example": "He forgot his homework again? He’s clowning."
        },
        "throw shade": {
            "short": "Insult or criticize subtly.",
            "explanation": "Used when someone makes a sneaky or indirect insult toward another person.",
            "example": "She didn’t say it outright, but she was definitely throwing shade at him."
        },
        "spill the tea": {
            "short": "Share gossip or news.",
            "explanation": "Used when someone reveals interesting, juicy, or scandalous information.",
            "example": "Come on, spill the tea about what happened at the party!"
        },
        "go off": {
            "short": "Express strong emotion or opinion.",
            "explanation": "Used when someone passionately speaks, rants, or reacts energetically.",
            "example": "She really went off in her speech about climate change!"
        },
        "on point": {
            "short": "Perfect or accurate.",
            "explanation": "Used to describe something done exactly right or very well.",
            "example": "Her makeup today is on point!"
        },
        "chill": {
            "short": "Relaxed or easygoing.",
            "explanation": "Used to describe someone calm, or to tell someone to relax.",
            "example": "Just chill, everything’s going to be fine."
        },
        "i can't even": {
            "short": "Overwhelmed or speechless.",
            "explanation": "Used when something is so surprising, frustrating, or shocking that you don’t know how to react.",
            "example": "I can't even with all this drama right now."
        },
        "we move": {
            "short": "Keep going / move on.",
            "explanation": "Used to express resilience or the idea of moving forward despite setbacks or drama.",
            "example": "Lost the game? Oh well, we move."
        },
        "pull up": {
            "short": "Arrive at a place.",
            "explanation": "Used when someone goes to a location, often to hang out or confront someone.",
            "example": "Pull up to the party around 8!"
        },
        "rizz": {
            "short": "Charm or flirting skill",
            "explanation": "Refers to someone's ability to attract others through confidence or charisma.",
            "example": "He’s got insane rizz with everyone at the club."
        },
        "ragequit": {
            "short": "Leaves angrily",
            "explanation": "To suddenly leave a game, conversation, or situation out of frustration or anger.",
            "example": "He ragequit the online match after losing in the last round."
        },
        "W": {
            "short": "Win",
            "explanation": "Used to show approval or that something is good, successful, or a victory.",
            "example": "You finished your project early? Big W!"
        },
        "L": {
            "short": "Loss",
            "explanation": "Used to show disapproval or that something is bad, failed, or a defeat.",
            "example": "Forgot your homework again? That’s an L."
        }
    }

    try:
        with open(APPROVED_FILE, "r") as f:
            approved_words = json.load(f)
            dictionary.update(approved_words)
    except json.JSONDecodeError:
        pass

    return dictionary
@app.route("/", methods=["GET", "POST"])
def index():
    dictionary = load_dictionary()

    # Word of the Day
    word_of_the_day = random.choice(list(dictionary.keys()))
    wotd_entry = dictionary[word_of_the_day]

    all_words = sorted(dictionary.keys())

    searched_word = None
    entry = None
    similar_words = []

    if request.method == "POST":
        searched_word = request.form.get("word").lower().strip()
        normalized_word = searched_word.replace(" ", "")

        entry = dictionary.get(searched_word)

        if not entry:
            entry = dictionary.get(normalized_word)

        if not entry:
            similar_words = find_similar_words(
                searched_word,
                dictionary.keys()
            )

        if not entry and not similar_words:
            for word, data in dictionary.items():
                text = (data.get("short","") + data.get("explanation","")).lower()
                if searched_word in text:
                    similar_words.append(word)

    return render_template(
        "index.html",
        searched_word=searched_word,
        entry=entry,
        similar_words=similar_words,
        word_of_the_day=word_of_the_day,
        wotd_entry=wotd_entry,
        all_words=all_words
    )

@app.route("/word/<word>")
def word_detail(word):
    dictionary = load_dictionary()
    entry = dictionary.get(word.lower())
    
    if not entry:
        return "Word not found", 404
    
    return render_template("word.html", word=word, entry=entry)

@app.route("/suggest", methods=["GET", "POST"])
def suggest_word():
    success = False

    if request.method == "POST":
        dictionary = load_dictionary()
        submitted_word = request.form.get("word").lower().strip()

        if submitted_word in dictionary:
            return render_template(
                "suggest.html",
                success=False,
                error="This word already exists in the dictionary."
            )

        new_entry = {
            "word": request.form.get("word").lower(),
            "meaning": request.form.get("meaning"),
            "example": request.form.get("example"),
        }

        with open(PENDING_FILE, "r") as f:
            pending = json.load(f)

        pending.append(new_entry)

        with open(PENDING_FILE, "w") as f:
            json.dump(pending, f, indent=4)

        success = True

    return render_template("suggest.html", success=success)

@app.route("/admin-review", methods=["GET", "POST"])
def admin_review():

    if not session.get("admin"):
        if request.method == "POST":
            if request.form.get("password") == ADMIN_PASSWORD:
                session["admin"] = True
                return redirect("/admin-review")
        return render_template("admin_login.html")
    
    with open(PENDING_FILE, "r") as f:
        pending = json.load(f)

    if request.method == "POST":
        action = request.form.get("action")
        index = int(request.form.get("index"))
        selected = pending[index]

        if action == "approve":
            with open(APPROVED_FILE, "r") as f:
                approved = json.load(f)

            approved[selected["word"]] = {
                "short": selected["meaning"],
                "explanation": selected["meaning"],
                "example": selected.get("example", ""),
                "added_at": int(time.time())
            }

            with open(APPROVED_FILE, "w") as f:
                json.dump(approved, f, indent=4)

        pending.pop(index)

        with open(PENDING_FILE, "w") as f:
            json.dump(pending, f, indent=4)

        return redirect("/admin-review")
    
    return render_template("admin.html", pending=pending)

@app.route("/explore")
def explore():
    dictionary = load_dictionary()
    all_words = sorted(dictionary.keys())  # [(word, data), ...]
    current_time = int(time.time())

    return render_template(
        "explore.html",
        all_words=all_words,
        dictionary=dictionary,
        current_time=current_time
    )

@app.route("/random")
def random_word():
    dictionary = load_dictionary()
    word = random.choice(list(dictionary.keys()))
    return redirect(f"/word/{word}")

@app.route("/suggestions")
def suggestions():
    query = request.args.get("q", "").lower().strip()
    if not query:
        return {"results": []}

    dictionary = load_dictionary()

    matches = difflib.get_close_matches(
        query,
        dictionary.keys(),
        n=5,
        cutoff=0.5
    )

    return {"results": matches}

if __name__ == "__main__":
    app.run(debug=True)