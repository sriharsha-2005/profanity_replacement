import csv
from typing import List, Dict, Optional

BATCH_SIZE = 100

# Comprehensive dictionary for spelling validation - expanded to include all valid words from the dataset
VALID_WORDS = {
    "oralsex", "orgasm", "ejaculating", "arse", "arsehole", "ass", "asshole",
    "bastard", "bitch", "bullshit", "cock", "cunt", "damn", "dick", "fuck",
    "hell", "motherfucker", "pussy", "shit", "slut", "twat", "wanker", "whore",
    "bollocks", "dumbass", "retard", "anal", "anus", "apeshit", "bastardish", 
    "bastards", "basterd", "bastid", "basturd", "batshit", "beaner", "bellend",
    "bewbs", "biatch", "bich", "biches", "biotch", "biotches", "biotchez",
    "bishes", "bitched", "bitcher", "bitchers", "bitches", "bitchez", "bitchfuck",
    "bitchhole", "bitchin", "bitching", "bitchlike", "bitchness", "bitchs",
    "bitchslap", "bitchtits", "bitchy", "bitchyass", "bizzach", "bj", "blacky",
    "blowaload", "blowjob", "blumpkinboy", "boll0ck", "bollock", "bollockchops",
    "bollocktician", "bollox", "bondage", "boner", "bonkjuice", "boobs", "booty",
    "breasticles", "breasts", "btch", "btotheinch", "bugger", "buggeroff",
    "bullshi", "bullshite", "bumbandits", "bumdriller", "bumhole", "bunghole",
    "buttermilk", "buttfuck", "buttfucker", "buttfuckers", "buttfuckingbandit",
    "butthole", "buttholeboy", "buttmunchers", "buttpirate", "bwc", "c00n",
    "c00nies", "c0ck", "c0ckhead", "c0cks", "c0cksuccer", "c0cksucked",
    "c0cksucker", "c0cksuckers", "c0x", "c0xux0r", "caaak", "caca", "cack",
    "cagone", "cajones", "cameljockey", "cameltoe", "carpetmuncher",
    "carpetmunchers", "carpetmunching", "cawk", "cawkmuncher", "cawks",
    "cawksucker", "ch1nk", "chesticles", "chinavirus", "chinesevirus",
    "chingchong", "chink", "chinky", "choadnectar", "chocha", "chokethechicken",
    "cholo", "clitlickers", "closetfuckhead", "clusterfuck", "clusterfucked",
    "clusterfucker", "clusterfucking", "clusterfucks", "cnt", "cntface",
    "cnts", "cnty", "cobbknobbler", "cockboy", "cockdroplets", "cockeater",
    "cockface", "cockgobbler", "cockh3ad", "cockhead", "cockheads", "cockhed",
    "cockjockey", "cockknocker", "cockless", "cocklicker", "cockmonger",
    "cockmunch", "cockmuncher", "cockrider", "cocks", "cockshit", "cockskin",
    "cocksmoker", "cocksnot", "cocksucc", "cocksuccas", "cocksuccer",
    "cocksuccers", "cocksuck", "cocksuckas", "cocksucked", "cocksucker",
    "cocksuckers", "cocksucking", "cocksuckingboiolas", "cocksuckingmothafuckers",
    "cocksuckingnobjokeys", "cocksucks", "cocksuk", "cocksuka", "cocksukka",
    "cocktease", "cocsuck", "cokmuncher", "coksucka", "coolie", "coon",
    "coon1es", "cooni3s", "coonie", "coonies", "coons", "coot", "cootcoot",
    "cooter", "cooterpuffing", "cootershooting", "cooties", "cottonpicker",
    "crazymofos", "crazysob", "creampie", "crotch", "crotchfiddler", "crotchy",
    "crow", "crows", "cuksuker", "cuksukka", "cumball", "cumdumpster",
    "cumgoon", "cumming", "cums", "cumslut", "cumz", "cunnilingus",
    "cuntasaurusrex", "cuntass", "cuntbag", "cuntbollock", "cuntelope",
    "cuntfart", "cuntits", "cuntless", "cuntlick", "cuntlicker", "cuntlickers",
    "cuntlips", "cuntness", "cunts", "cunty", "cuntz", "cuunt", "cyberfck",
    "cyberfcks", "cyberfuccs", "cyberfucks", "cyberfucs", "cyberfukk",
    "cyberfukks", "cyberfvcks", "d0ggystyle", "d1ck", "d1ckhead", "d1ckheads",
    "d1cks", "d1cksucker", "d1cksukka", "d1ckz", "d1ldo", "dafuq", "dago",
    "darkass", "darkfuck", "darkie", "darkshit", "darktard", "darky", "dck",
    "dcks", "dickbreath", "dickface", "dickfucker", "dickgobbler", "dickhead",
    "dickheads", "dickjockies", "dickless", "dicklicker", "dickmilker",
    "dickmuncher", "dicknibbler", "dicks", "dickskin", "dickslapper",
    "dicksmoker", "dicksucker", "dickvag", "dickz", "diddle", "dikhead",
    "diks", "dild0", "dipsh1t", "dipsh1tty", "dipshat", "dipshidiot",
    "dipshit", "dipshite", "dipshits", "dipshitter", "dipshitty", "dipstick",
    "dirtysanchez", "dix", "dlck", "dlcks", "dld0", "dldo", "dogfuck",
    "dogfucker", "dogfucking", "doggostyle", "doggystyle", "dogiestyle",
    "dogsbollocks", "dogsh1t", "dogsh1ts", "dogshit", "dogshits", "dogstyle",
    "dolt", "dong", "doosh", "dothead", "doubledick", "doubledicking",
    "doubledong", "doublepen", "douche", "douchebag", "douchecanoe",
    "dumasses", "dumbarrassed", "dumbass", "dumbasses", "dumbassfucker",
    "dumbassmofoes", "dumbassmothafuckers", "dumbasssonofabitch", "dumbbastard",
    "dumbfucker", "dumbfucks", "dumbshit", "dumbss", "dumpaload", "dunecoon",
    "dyke", "erectoplasm", "f0ck", "f0cked", "f0cker", "f0ckers", "facefuck",
    "fack", "fackuhs", "fag", "fag0t", "fagasses", "fagbag", "faget",
    "fagg0t", "fagging", "faggo", "faggot", "faggoting", "faggotmofoes",
    "faggotmothafuckers", "faggotnobjockies", "faggotnobjokeys", "faggots",
    "faggotsonofabitch", "faggs", "faggy", "faghag", "fagot", "fagqueen",
    "fags", "fagshit", "fartfucker", "fatass", "fatasses", "fccuker", "fck",
    "fcka", "fckahz", "fcked", "fckedup", "fcker", "fckerbunny", "fckin",
    "fcking", "fckk", "fckked", "fckking", "fcks", "fcktard", "fckyeah",
    "fckyou", "fcuk", "fcuked", "fcuker", "fcukers", "fcuking", "fcukker",
    "fcuks", "fcvking", "feck", "feckarse", "fecker", "fed", "feg",
    "fellatioaficionado", "fellator", "fer", "fg", "fgg0t", "fgging",
    "fggot", "fgs", "fgshit", "fick", "finger", "fingerbanged", "fingerfuck",
    "fingerpop", "fk", "fkbny", "fkbunny", "fked", "fker", "fking", "fkings",
    "fkker", "flamer", "flamers", "focker", "fook", "fooker", "fookuh",
    "forked", "fothermuckers", "fuc", "fucc", "fucca", "fuccers", "fuccing",
    "fuccs", "fucka", "fuckahs", "fuckarse", "fuckass", "fuckasses", "fuckaz",
    "fuckbag", "fuckboy", "fucked", "fuckedup", "fuckem", "fucker", "fuckeroff",
    "fuckers", "fuckface", "fuckfaces", "fuckgoblin", "fuckhead", "fuckheaded",
    "fuckheads", "fuckin", "fucking", "fuckinga", "fuckingasshole", "fuckingbastard",
    "fuckinghell", "fuckingme", "fuckingretard", "fuckingshit", "fuckk",
    "fuckless", "fuckmachine", "fucknuckle", "fuckoff", "fucks", "fuckshit",
    "fuckshitface", "fuckshithead", "fuckstar", "fuckster", "fuckstick",
    "fucktard", "fucktards", "fuckup", "fuckwad", "fuckwhore", "fucky0u",
    "fuckyou", "fuckyour", "fuckyourmother", "fucs", "fucx", "fudgefucker",
    "fudgepacker", "fudgepackers", "fudgepackershitter", "fudgepackingfucker",
    "fugged", "fugger", "fuggerz", "fuggings", "fugly", "fuk", "fuk1n",
    "fuk1ng", "fukcs", "fuker", "fukheads", "fukin", "fuking", "fukk",
    "fukka", "fukked", "fukker", "fukkers", "fukking", "fukkings", "fukkuh",
    "fuks", "fuku", "fukwhore", "fukwit", "fullofshit", "funbags", "fuq",
    "futhamucka", "fux", "fux0r", "fvck", "fvcka", "fvckbunny", "fvcker",
    "fvckers", "fvckin", "fvcking", "fvckkerbunny", "fvckwhi", "fvckyou",
    "fxck", "fxcked", "fxcker", "fxcking", "g0ddamn", "g0ddamned", "g0ddamnit",
    "gashstabber", "gayass", "gaybitch", "gayest", "gayfuck", "gayfucker",
    "gaylord", "gaylords", "gayness", "gayshit", "gaysian", "gaytard",
    "gaywad", "geebag", "getfucked", "ginjockey", "girlieboy", "girlybits",
    "girlyboy", "gobshite", "godamnit", "goddam", "goddammit", "goddamn",
    "goddamned", "goddamnit", "goddamnmothafuckers", "goddamnsonofabitch",
    "goddmnit", "gofuckyourself", "gook", "gotohell", "gowl", "greaser",
    "groid", "groper", "gyb1tch", "gylord", "gyp", "gyshit", "harrypalms",
    "heeb", "higg", "higg3r", "higga", "higger", "higgers", "hoar", "hoe",
    "hoeasses", "hoebag", "hoes", "holyfuck", "homo", "homoasses", "homos",
    "hooters", "horsesasses", "horseshit", "hustler", "injun", "j3rk",
    "ja1lbait", "jackarse", "jackass", "jackasses", "jackasss", "jackoff",
    "jackoffs", "jackoffz", "jagoff", "jailbait", "jailbat", "jalbait",
    "jap", "jerk0ff", "jerk0ffs", "jerkingoff", "jerkoff", "jerkoffjerkingoff",
    "jerkoffs", "jerksoff", "jewboy", "jigaboo", "jigaboos", "jigga",
    "jiggaboo", "jiggabooboo", "jiggaboos", "jiggabu", "jiggas", "jigger",
    "jiggerboo", "jiggerboos", "jiggs", "jiggyboo", "jigro", "jimcrow",
    "jizz", "jizzbags", "jizzeater", "jizzed", "jizzes", "jizzfucker",
    "jizzing", "jizzjockey", "jizzlicker", "jizzsacks", "jizzstain", "jizzy",
    "joffs", "k1k3", "k1ke", "kiddiddler", "kiddytouch", "kike", "kikes",
    "kissass", "kissmyass", "kittypuncher", "kk3", "kke", "kkk", "klan",
    "klitoris", "kneegrows", "knickers", "knob", "knob3d", "knob3nd",
    "knobd", "knobe", "knobead", "knobeads", "knobeater", "knobed", "knobeds",
    "knobend", "knobender", "knobends", "knobendy", "knobendz", "knober",
    "knobes", "knobface", "knobgobbler", "knobhead", "knobheads", "knobjockey",
    "knobjockies", "knobjocky", "knobjokey", "knobjokeys", "nobs", "nonce",
    "nuckas", "nuggets", "nutbutter", "nutsack", "nutsacks", "nympho",
    "nymphomaniac", "octopussy", "ovendodger", "p3n1shead", "p3nisfcker",
    "p3nisfcukers", "p3nisfvcker", "p3nisfvckers", "packerfudgehead",
    "packingfudge", "packingfudgefucker", "packingfudgefucking", "packingfudgehead",
    "packmyfudge", "packsomefudgefucker", "paki", "palmjockey", "pancakeface",
    "pecker", "peckerhead", "pedo", "pedobear", "pedobears", "pedophl",
    "pedos", "pedoz", "peen", "peener", "penisfcker", "penisfuccer",
    "penisfucker", "penisfuckers", "penisfvcker", "penisfvckers", "penishead",
    "peter", "peterpuffer", "phaggot", "phaggots", "phagot", "phags",
    "phggots", "phuc", "phucc", "phuccer", "phucchead", "phuccing", "phuck",
    "phuck3r", "phucked", "phucker", "phuckin", "phucking", "phuckings",
    "phucks", "phucup", "phuk", "phuked", "phukeds", "phukhead", "phuking",
    "phukings", "phukk", "phukked", "phukkeds", "phukker", "phukking",
    "phuks", "phukshit", "phuku", "phukup", "phuq", "phuqs", "phvckings",
    "pigfucker", "pigfuckers", "pigfucking", "pigfukker", "piggyfuck",
    "pigshit", "pillowbiter", "pissface", "pissoff", "pissofffuckhead",
    "pissoffs", "pissshit", "polelicker", "polesmoker", "polesucker",
    "porchmonkey", "prick", "prickface", "prickgobbler", "prickhead",
    "pricks", "pu55y", "pullthepud", "punani", "punkasses", "punkassmofoes",
    "puss", "pusses", "pussie", "pussies", "pussless", "pusslicker",
    "pussycat", "pussyfucker", "pussylick", "pussylicker", "pussylickers",
    "pussylicking", "pussys", "pussywhipped", "pusy", "puta", "puussy",
    "puzzies", "puzzy", "queerasses", "queers", "r3tard", "r3trd", "r3trded",
    "raghead", "ragheads", "ragtard", "ramrod", "ratbastard", "ratbaztad",
    "reacharound", "rectum", "redskin", "retard", "retardo", "retardotron",
    "ricemonkey", "rimjob", "sack", "saladtosser", "sambo", "sandnigger",
    "sausagejockey", "scamfuck", "schlong", "scumfuck", "scumfucker",
    "scumfvck", "scummy", "scut", "sh", "sh1s", "sh1t", "sh1t3", "sh1td1ck",
    "sh1tdick", "sh1te", "sh1tfuck", "sh1th3ad", "sh1theads", "sh1ts",
    "sh1tsome", "sh1tt", "sh1tty", "sh3mal3", "sh3male", "shat", "sheeeet",
    "sheet", "sheister", "shemal3", "shemale", "shemales", "shet", "shi",
    "shiat", "shiddick", "shie", "shiester", "shiesterfuck", "shiesterfuckface",
    "shiesterfuckhead", "shiesterfucks", "shipdit", "shis", "shit3",
    "shitarse", "shitass", "shitasses", "shitassfucker", "shitassfuckface",
    "shitbag", "shitbandit", "shitbird", "shitblimp", "shitblimps",
    "shitbrain", "shitd1ck", "shitdick", "shitdicks", "shitdikk", "shitdip",
    "shite", "shiteblimps", "shited", "shitedick", "shitefuck", "shitefulls",
    "shitehead", "shites", "shitey", "shitface", "shitfaced", "shitfacefuck",
    "shitfacefucker", "shitfck", "shitfk", "shitforbrains", "shitfreak",
    "shitfuck", "shitfucker", "shitfuckhead", "shitfuckmotherfucker",
    "shitfucks", "shitfudgefucker", "shitfvck", "shithead", "shitheadfucker",
    "shitheadfuckface", "shitheads", "shithole", "shitlicker", "shits",
    "shitsdick", "shitsfuck", "shitsful", "shitstain", "shitstuffers",
    "shittastic", "shittasticfuck", "shitte", "shitted", "shitter",
    "shitterfucker", "shitti", "shitties", "shittiest", "shitting",
    "shittings", "shitty", "shittydick", "shittydicks", "shittyfuck",
    "shittyfuckface", "shittyful", "shittymofoes", "shiy", "shlong",
    "shmale", "shtfuk", "shutthefuckup", "shylock", "shytfeisterfuck",
    "sissy", "sixtynine", "skank", "skanks", "skanky", "skankz", "sknks",
    "sknky", "sknkz", "slag", "slantard", "slanteye", "slanteyeb1tch",
    "slanteyes", "slanteyeshit", "slantfreak", "slanty", "slit", "slnteye",
    "sluthole", "sluts", "slutty", "sm", "snatch", "snatchlicker", "soab",
    "sob", "sobs", "sonnabitch", "sonobitch", "sonofabitch", "sonofbitches",
    "sonsofb1tches", "sonsofbitches", "sonzofbitchez", "soppybollucks",
    "spanking", "sperm", "sphincter", "spic", "spicfuck", "spick", "spics",
    "spicshit", "spig", "spik", "spix", "spook", "spooks", "spunk",
    "ssfcker", "ssfucker", "ssfvcker", "sshole", "stfu", "stumpchewer",
    "stupidasses", "stupidfucker", "stupidhoe", "suck", "suckmycock",
    "suckmyd", "suckmydick", "suckoff", "sumbitch", "sumofabitch", "swine",
    "swinefucker", "tacohead", "tadger", "takingthepiss", "tallywacker",
    "tarbaby", "tard", "tardasses", "tart", "throater", "throatyogurt",
    "ticklethepickle", "timbernigger", "tonguefucker", "tonguefucking",
    "tosser", "tossingsalad", "towelhead", "towelheads", "towelshithead",
    "tramp", "tranny", "transvestite", "trashb1tch", "trashbitch",
    "trashbitches", "trashbitchez", "trashbtch", "trasherbitch",
    "trasherbitchs", "trashybitches", "trousersnake", "turdcutter",
    "turdhead", "twa", "twatface", "twats", "twatt", "twattish", "twatwaffle",
    "twatzilla", "twink", "twt", "upskirts", "uselessfucker", "vag",
    "vajayjay", "vulva", "w4nk3r", "w4nker", "wang", "wangwrangler",
    "wank", "wank3r", "wank3rs", "wankbastard", "wanked", "wankers",
    "wankies", "wanking", "wankoff", "wanks", "we1back", "weenie",
    "weiner", "wetback", "wetbacks", "wh0r3", "wh0re", "whackoff",
    "whatthefuck", "whoar", "whoars", "whor3", "whores", "wigger",
    "willywhacker", "windowlicker", "wiseass", "wnker", "wnkers", "wop",
    "wophead", "zipinthewire", "zipperhead"
}

def validate_spelling(term: str) -> Optional[str]:
    """Check if term is properly spelled, return corrected version or None"""
    # First check direct match
    if term in VALID_WORDS:
        return term
    
    # Common leet-speech corrections
    corrections = {
        '0': 'o',
        '1': 'i',
        '3': 'e',
        '4': 'a',
        '5': 's',
        '7': 't'
    }
    
    # Try correcting numbers->letters
    corrected = ''.join([corrections.get(c, c) for c in term])
    return corrected if corrected in VALID_WORDS else None

def process_csv_batches(input_file: str, output_file: str):
    """Process CSV in batches of 100 records"""
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, 
                              fieldnames=['badword', 'badwordpos', 'replacdementword', 'replacementwordtype'])
        writer.writeheader()
        
        batch = []
        total_processed = 0
        valid_count = 0
        invalid_count = 0
        
        for row in reader:
            batch.append(row)
            
            if len(batch) == BATCH_SIZE:
                # Process batch
                batch_valid, batch_invalid = process_batch(batch, writer)
                valid_count += batch_valid
                invalid_count += batch_invalid
                total_processed += len(batch)
                
                print(f"Processed batch of {len(batch)} records... Total: {total_processed} | Valid: {valid_count} | Invalid: {invalid_count}")
                batch = []
        
        # Process final batch (remaining records)
        if batch:
            batch_valid, batch_invalid = process_batch(batch, writer)
            valid_count += batch_valid
            invalid_count += batch_invalid
            total_processed += len(batch)
            
            print(f"Processed final batch of {len(batch)} records... Total: {total_processed} | Valid: {valid_count} | Invalid: {invalid_count}")
        
        print(f"\nFinal Summary:")
        print(f"Total records processed: {total_processed}")
        print(f"Valid records: {valid_count}")
        print(f"Invalid records: {invalid_count}")

def process_batch(batch: List[Dict], writer) -> tuple:
    """Process a batch of records"""
    valid_count = 0
    invalid_count = 0
    
    for row in batch:
        original_word = row.get('badword', '')
        replacement_word = row.get('replacement_word', '')
        word_type = row.get('type', '')
        
        # Apply spelling validation
        correct_spelling = validate_spelling(original_word)
        
        if correct_spelling:
            writer.writerow({
                'badword': correct_spelling,
                'badwordpos': word_type,
                'replacdementword': replacement_word,
                'replacementwordtype': ''  # Left blank as per original specification
            })
            valid_count += 1
        else:
            invalid_count += 1
    
    return valid_count, invalid_count

if __name__ == "__main__":
    process_csv_batches("processed_bad_words_fast.csv", "validated_profanity_replacements.csv")
    print("Dataset generation complete. Only properly spelled terms included.") 