from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Dictionary data
words_list = [
    "sus", "yeet", "cap", "stan", "vibe", "simp", "flex", "no cap",
    "lit", "salty", "ghost", "lowkey", "highkey", "mood", "tea",
    "slaps", "clout", "shook", "fam", "bop", "drip", "snatched",
    "receipts", "periodt", "cheugy", "big yikes", "meme", "snack",
    "woke", "extra", "bet", "cheese", "fit", "sksksk", "and I oop",
    "finna", "cringe", "glow up", "cancelled", "ok boomer", "okurrr",
    "goat", "sus vibe", "deadass", "pog", "rip", "ratio", "bussin", "main character", "quiet quitting", 
    "boujee", "cancel culture", "capper", "cheugy vibes", "clap back", "cuffed", "dime", "drama llama",
    "fam jam", "finsta", "fit check", "gaslight", "ghosting", "hits different", "hits different vibes",
    "humblebrag", "iconic", "ig", "influencer", "karen", "keeping it 100", "litty", "lurk",
    "main account", "mood af", "no chill", "on fleek", "period", "pov", "queen", "receipt", "salty af",
    "savage", "ship", "stan culture", "stan twitter", "sus moment", "tbh", "vibe check", "vibing", "weird flex",
    "wholesome", "wypipo", "yass", "yikes", "zip it"
]

dictionary = {
    "sus": {
        "short": "Suspicious or shady",
        "explanation": "Used to describe someone or something acting suspiciously.",
        "example": "He said he didn’t take the cookie, but that’s kinda sus.",
        "category": "slang"
    },
    "yeet": {
        "short": "To throw or move quickly",
        "explanation": "Used when tossing something or expressing excitement.",
        "example": "He yeeted the ball across the yard!",
        "category": "slang"
    },
    "cap": {
        "short": "Lie or false statement",
        "explanation": "Used to call out someone who is lying.",
        "example": "He said he won the game, but that’s cap.",
        "category": "slang"
    },
    "stan": {
        "short": "Super fan",
        "explanation": "To strongly support someone or something.",
        "example": "I totally stan that new singer!",
        "category": "slang"
    },
    "vibe": {
        "short": "Mood or feeling",
        "explanation": "Refers to the overall feeling of a person, place, or thing.",
        "example": "This cafe has a chill vibe.",
        "category": "slang"
    },
    "simp": {
        "short": "Overly affectionate person",
        "explanation": "Someone who goes overboard to impress another person.",
        "example": "He bought her flowers every day, what a simp!",
        "category": "slang"
    },
    "flex": {
        "short": "Show off",
        "explanation": "To brag about something in a flashy way.",
        "example": "He’s always trying to flex his new shoes.",
        "category": "slang"
    },
    "no cap": {
        "short": "No lie / seriously",
        "explanation": "Used to emphasize truthfulness.",
        "example": "That concert was amazing, no cap!",
        "category": "slang"
    },
    "lit": {
        "short": "Exciting or amazing",
        "explanation": "Describes something that’s fun, energetic, or excellent.",
        "example": "The party last night was lit!",
        "category": "slang"
    },
    "salty": {
        "short": "Bitter or annoyed",
        "explanation": "Being upset or irritated about something small.",
        "example": "She’s salty because she lost the game.",
        "category": "slang"
    },
    "ghost": {
        "short": "Disappear without notice",
        "explanation": "To stop communicating suddenly.",
        "example": "He ghosted me after our first date.",
        "category": "slang"
    },
    "lowkey": {
        "short": "Secretly or quietly",
        "explanation": "Something you don’t want to announce loudly.",
        "example": "I’m lowkey excited for the exam.",
        "category": "slang"
    },
    "highkey": {
        "short": "Clearly or openly",
        "explanation": "Something that is obvious or not hidden.",
        "example": "I highkey love this song!",
        "category": "slang"
    },
    "mood": {
        "short": "Relatable feeling",
        "explanation": "Used to express something you relate to.",
        "example": "Sleeping all day is a mood.",
        "category": "slang"
    },
    "tea": {
        "short": "Gossip",
        "explanation": "Information, rumors, or juicy news.",
        "example": "Spill the tea about what happened yesterday!",
        "category": "slang"
    },
    "slaps": {
        "short": "Really good",
        "explanation": "Usually for music, meaning it’s excellent.",
        "example": "This new song slaps!",
        "category": "slang"
    },
    "clout": {
        "short": "Influence or fame",
        "explanation": "Being popular or famous online.",
        "example": "She’s just posting for clout.",
        "category": "slang"
    },
    "shook": {
        "short": "Surprised or shocked",
        "explanation": "Feeling amazed or startled by something.",
        "example": "I was shook after watching that movie.",
        "category": "slang"
    },
    "fam": {
        "short": "Close friends",
        "explanation": "Refers to your trusted circle of friends.",
        "example": "What’s up, fam?",
        "category": "slang"
    },
    "bop": {
        "short": "Catchy song",
        "explanation": "A song that’s fun and easy to listen to.",
        "example": "This new track is a bop!",
        "category": "slang"
    },
    "drip": {
        "short": "Stylish or trendy",
        "explanation": "Refers to someone’s fashion sense or outfit.",
        "example": "Check out his drip!",
        "category": "slang"
    },
    "snatched": {
        "short": "Looking great",
        "explanation": "Usually about appearance or style.",
        "example": "Her outfit is snatched.",
        "category": "slang"
    },
    "receipts": {
        "short": "Proof or evidence",
        "explanation": "Used to back up claims, especially in gossip.",
        "example": "I got receipts for what she said!",
        "category": "slang"
    },
    "periodt": {
        "short": "Emphasis on finality",
        "explanation": "Used to end a statement for emphasis.",
        "example": "That’s the best movie ever, periodt.",
        "category": "slang"
    },
    "cheugy": {
        "short": "Outdated or trying too hard",
        "explanation": "Something that isn’t trendy anymore.",
        "example": "That outfit is kinda cheugy.",
        "category": "slang"
    },
    "big yikes": {
        "short": "Awkward or cringy",
        "explanation": "Something extremely embarrassing or awkward.",
        "example": "He fell in front of everyone—big yikes.",
        "category": "slang"
    },
    "meme": {
        "short": "Funny internet content",
        "explanation": "A humorous picture, video, or text shared online.",
        "example": "I can’t stop laughing at this meme!",
        "category": "slang"
    },
    "snack": {
        "short": "Attractive person",
        "explanation": "Someone who looks good or appealing.",
        "example": "He’s a whole snack!",
        "category": "slang"
    },
    "woke": {
        "short": "Socially aware",
        "explanation": "Being conscious of social issues.",
        "example": "She’s really woke about environmental issues.",
        "category": "slang"
    },
    "extra": {
        "short": "Over the top",
        "explanation": "Doing too much in an unnecessary way.",
        "example": "He’s so extra with his party decorations.",
        "category": "slang"
    },
    "bet": {
        "short": "Agreement or affirmation",
        "explanation": "Used like 'okay' or 'you got it'.",
        "example": "Can you pick me up at 8? Bet.",
        "category": "slang"
    },
    "cheese": {
        "short": "Smile",
        "explanation": "To grin widely, usually for a photo.",
        "example": "Say cheese!",
        "category": "slang"
    },
    "fit": {
        "short": "Outfit",
        "explanation": "Refers to someone’s clothing or style.",
        "example": "That fit is fire!",
        "category": "slang"
    },
    "sksksk": {
        "short": "Excited expression",
        "explanation": "Used to express excitement or laughter.",
        "example": "Sksksk I can’t believe it!",
        "category": "slang"
    },
    "and I oop": {
        "short": "Expression of shock",
        "explanation": "Used when something surprising happens.",
        "example": "And I oop, I spilled my coffee!",
        "category": "slang"
    },
    "finna": {
        "short": "Going to",
        "explanation": "Short for 'fixing to', meaning about to do something.",
        "example": "I’m finna leave soon.",
        "category": "slang"
    },
    "cringe": {
        "short": "Embarrassing or awkward",
        "explanation": "Something that causes secondhand embarrassment.",
        "example": "That dance move was so cringe.",
        "category": "slang"
    },
    "glow up": {
        "short": "Transformation for the better",
        "explanation": "Improving appearance or style over time.",
        "example": "She had a major glow up this year.",
        "category": "slang"
    },
    "cancelled": {
        "short": "Rejected socially",
        "explanation": "Someone who is socially boycotted for a mistake.",
        "example": "That influencer got cancelled after the scandal.",
        "category": "slang"
    },
    "ok boomer": {
        "short": "Dismissive phrase",
        "explanation": "Used to dismiss outdated opinions.",
        "example": "He said homework is pointless—ok boomer.",
        "category": "slang"
    },
    "okurrr": {
        "short": "Expression of excitement",
        "explanation": "Popularized by Cardi B, used to affirm something.",
        "example": "We’re going to the concert, okurrr!",
        "category": "slang"
    },
    "goat": {
        "short": "Greatest of all time",
        "explanation": "Used to describe someone excellent at something.",
        "example": "She’s the GOAT at chess.",
        "category": "slang"
    },
    "sus vibe": {
        "short": "Suspicious feeling",
        "explanation": "A general sense of something being off.",
        "example": "That party gave me a sus vibe.",
        "category": "slang"
    },
    "deadass": {
        "short": "Seriously / for real",
        "explanation": "Used to emphasize truth.",
        "example": "I’m deadass tired right now.",
        "category": "slang"
    },
    "pog": {
        "short": "Exciting or awesome",
        "explanation": "Used in gaming communities for hype moments.",
        "example": "That play was pog!",
        "category": "slang"
    },
    "rip": {
        "short": "Rest in peace / sad",
        "explanation": "Used when something bad happens or someone dies.",
        "example": "RIP my phone, it fell in water.",
        "category": "slang"
    },
    "ratio": {
        "short": "Social media metric",
        "explanation": "When a post gets more replies than likes, often negative.",
        "example": "Your tweet got ratioed.",
        "category": "slang"
    },
    "bussin": {
        "short": "Really good",
        "explanation": "Usually refers to food or something impressive.",
        "example": "This pizza is bussin!",
        "category": "slang"
    },
    "main character": {
        "short": "Center of attention",
        "explanation": "Feeling like the protagonist of your own life.",
        "example": "She’s living her best main character life.",
        "category": "slang"
    },
    "quiet quitting": {
        "short": "Doing the bare minimum at work",
        "explanation": "Not overextending yourself professionally.",
        "example": "He’s quiet quitting, only finishing assigned tasks.",
        "category": "slang"
    },
    "boujee": {
        "short": "Fancy or high-class",
        "explanation": "Used for someone who acts upscale or pretentious.",
        "example": "She’s so boujee, always at the nicest cafes.",
        "category": "slang"
    },
    "cancel culture": {
        "short": "Public shaming",
        "explanation": "The practice of socially boycotting someone after a mistake or controversial action.",
        "example": "The influencer faced cancel culture after their tweet.",
        "category": "slang"
    },
    "capper": {
        "short": "Someone who lies",
        "explanation": "A person who exaggerates or isn’t truthful.",
        "example": "He said he got 100% on the test, what a capper.",
        "category": "slang"
    },
    "cheugy vibes": {
        "short": "Outdated aesthetic",
        "explanation": "Describes something that’s trying to be trendy but isn’t anymore.",
        "example": "Her outfit is giving cheugy vibes.",
        "category": "slang"
    },
    "clap back": {
        "short": "Sharp response",
        "explanation": "A witty or fierce reply, usually to criticism.",
        "example": "She clapped back at the rude comment perfectly.",
        "category": "slang"
    },
    "cuffed": {
        "short": "In a relationship",
        "explanation": "Being romantically attached to someone.",
        "example": "He’s cuffed now, so he’s off the market.",
        "category": "slang"
    },
    "dime": {
        "short": "Perfect 10 / attractive person",
        "explanation": "Refers to someone who is extremely attractive.",
        "example": "She’s a dime, no doubt.",
        "category": "slang"
    },
    "drama llama": {
        "short": "Overly dramatic person",
        "explanation": "Someone who exaggerates problems or emotions.",
        "example": "Stop being a drama llama, it’s not that serious.",
        "category": "slang"
    },
    "fam jam": {
        "short": "Family gathering",
        "explanation": "Used for a fun get-together with family or close friends.",
        "example": "We had a little fam jam over the weekend.",
        "category": "slang"
    },
    "finsta": {
        "short": "Fake Instagram",
        "explanation": "A secondary Instagram account for private posts.",
        "example": "I only post funny memes on my finsta.",
        "category": "slang"
    },
    "fit check": {
        "short": "Outfit inspection",
        "explanation": "Showing off what you’re wearing.",
        "example": "Let me do a quick fit check before we leave.",
        "category": "slang"
    },
    "gaslight": {
        "short": "Manipulate someone",
        "explanation": "Make someone doubt their own reality or sanity.",
        "example": "He tried to gaslight her into thinking she was wrong.",
        "category": "slang"
    },
    "ghosting": {
        "short": "Sudden disappearance",
        "explanation": "Cutting off communication with someone without explanation.",
        "example": "He ghosted after our second date.",
        "category": "slang"
    },
    "hits different": {
        "short": "Feels unique or intense",
        "explanation": "Something that impacts you emotionally in a distinct way.",
        "example": "This song hits different at night.",
        "category": "slang"
    },
    "humblebrag": {
        "short": "Brag disguised as modesty",
        "explanation": "Pretending to be modest while boasting.",
        "example": "She humblebragged about her new car.",
        "category": "slang"
    },
    "iconic": {
        "short": "Memorable or legendary",
        "explanation": "Something widely recognized as impressive or important.",
        "example": "That scene from the movie is iconic.",
        "category": "slang"
    },
    "ig": {
        "short": "Instagram",
        "explanation": "Short for Instagram.",
        "example": "Check out my new post on IG.",
        "category": "slang"
    },
    "influencer": {
        "short": "Social media personality",
        "explanation": "Someone who promotes products or ideas online.",
        "example": "She’s a popular fashion influencer.",
        "category": "slang"
    },
    "karen": {
        "short": "Entitled woman",
        "explanation": "Stereotype for someone acting demanding or privileged.",
        "example": "The lady at the store was acting like a total Karen.",
        "category": "slang"
    },
    "keeping it 100": {
        "short": "Being honest",
        "explanation": "Keeping things real or truthful.",
        "example": "I’m keeping it 100, that movie was terrible.",
        "category": "slang"
    },
    "litty": {
        "short": "Even more lit",
        "explanation": "An amplified way of saying 'exciting' or 'fun'.",
        "example": "This party is litty!",
        "category": "slang"
    },
    "lurk": {
        "short": "Watch without participating",
        "explanation": "Observing online activity silently.",
        "example": "I just lurk on Twitter sometimes.",
        "category": "slang"
    },
    "main account": {
        "short": "Primary social media account",
        "explanation": "The main profile someone posts publicly from.",
        "example": "I keep my selfies on my main account.",
        "category": "slang"
    },
    "mood af": {
        "short": "Relatable feeling, intensified",
        "explanation": "Used to emphasize how relatable something is.",
        "example": "Sleeping all day? Mood af.",
        "category": "slang"
    },
    "no chill": {
        "short": "Overreacting",
        "explanation": "Someone who cannot relax or calm down.",
        "example": "He’s so extra, no chill at all.",
        "category": "slang"
    },
    "on fleek": {
        "short": "Perfectly done",
        "explanation": "Used to describe appearance, especially eyebrows or outfits.",
        "example": "Her makeup is on fleek today.",
        "category": "slang"
    },
    "period": {
        "short": "End of discussion",
        "explanation": "Used to emphasize a point with no debate.",
        "example": "That’s the best movie ever, period.",
        "category": "slang"
    },
    "pov": {
        "short": "Point of view",
        "explanation": "Refers to perspective in a video or meme.",
        "example": "POV: You just finished finals.",
        "category": "slang"
    },
    "queen": {
        "short": "Amazing person",
        "explanation": "Used to praise someone, usually a woman.",
        "example": "You handled that so well, queen!",
        "category": "slang"
    },
    "receipt": {
        "short": "Proof or evidence",
        "explanation": "Evidence backing up a claim, similar to 'receipts'.",
        "example": "I have the receipt of what they said!",
        "category": "slang"
    },
    "salty af": {
        "short": "Very annoyed or bitter",
        "explanation": "Extreme version of being salty.",
        "example": "She was salty af about losing the game.",
        "category": "slang"
    },
    "savage": {
        "short": "Bold or ruthless",
        "explanation": "Someone or something being impressively daring or fierce.",
        "example": "That comeback was savage.",
        "category": "slang"
    },
    "ship": {
        "short": "Support a relationship",
        "explanation": "Rooting for two people to be together romantically.",
        "example": "I totally ship them!",
        "category": "slang"
    },
    "stan culture": {
        "short": "Fandom obsession",
        "explanation": "When fans aggressively support someone or something.",
        "example": "Stan culture can be intense on Twitter.",
        "category": "slang"
    },
    "stan twitter": {
        "short": "Community of obsessive fans",
        "explanation": "Part of Twitter dedicated to fandoms.",
        "example": "Stan Twitter went crazy over the new trailer.",
        "category": "slang"
    },
    "sus moment": {
        "short": "Suspicious event",
        "explanation": "A situation that feels shady or questionable.",
        "example": "That was a sus moment when he disappeared.",
        "category": "slang"
    },
    "tbh": {
        "short": "To be honest",
        "explanation": "Used to express sincerity.",
        "example": "TBH, I didn’t like the movie.",
        "category": "slang"
    },
    "vibe check": {
        "short": "Test mood or energy",
        "explanation": "Assessing someone’s energy or behavior.",
        "example": "Vibe check: Are we ready for the party?",
        "category": "slang"
    },
    "vibing": {
        "short": "Relaxed enjoyment",
        "explanation": "Enjoying a moment or atmosphere.",
        "example": "Just vibing to some music.",
        "category": "slang"
    },
    "weird flex": {
        "short": "Unusual brag",
        "explanation": "Boasting about something strange or unexpected.",
        "example": "He owns 10 staplers—what a weird flex.",
        "category": "slang"
    },
    "wholesome": {
        "short": "Heartwarming or positive",
        "explanation": "Something that makes you feel good emotionally.",
        "example": "This video of puppies is wholesome.",
        "category": "slang"
    },
    "wypipo": {
        "short": "White people (playful)",
        "explanation": "Slang referring to white people, usually jokingly.",
        "example": "Wypipo love pumpkin spice lattes.",
        "category": "slang"
    },
    "yass": {
        "short": "Excited affirmation",
        "explanation": "Enthusiastic way of saying 'yes'.",
        "example": "Yass! That’s amazing news!",
        "category": "slang"
    },
    "yikes": {
        "short": "Reaction to awkwardness",
        "explanation": "Used when something is shocking or cringy.",
        "example": "He tried to rap in class—yikes.",
        "category": "slang"
    },
    "zip it": {
        "short": "Be quiet",
        "explanation": "Telling someone to stop talking.",
        "example": "Zip it! I’m trying to concentrate.",
        "category": "slang"
    }
}
@app.route("/", methods=["GET", "POST"])
def index():
    searched_word = None
    entry = None

    if request.method == "POST":
        searched_word = request.form.get("word", "").strip().lower()
        entry = dictionary.get(searched_word)

    word_of_the_day = random.choice(list(dictionary.keys()))
    wotd_entry = dictionary[word_of_the_day]

    return render_template(
        "index.html",
        all_words=list(dictionary.keys()),  # ✅ IMPORTANT
        searched_word=searched_word,
        entry=entry,
        word_of_the_day=word_of_the_day,
        wotd_entry=wotd_entry
    )

if __name__ == "__main__":
    app.run(debug=True)
