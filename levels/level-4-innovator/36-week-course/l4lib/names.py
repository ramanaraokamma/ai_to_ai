"""names.py - the 231 typed names (lowercase, letters only, all distinct).

Used in weeks 8-13 (character model, name generator, sampling); Week 12 trains on them
and measures what fraction of generated names already exist in this list.

These are the names from the Level 4 reference module 2, typed by the course author.
Nothing is downloaded. Import NAMES (a list of 231 str), or use the helpers below.
"""

_RAW = """
aarav aditi adrian agnes ahmed aiko alina amara amelia anders
andrei anika anita ansel arjun armin arnav asha aslan astrid
aurora bashir beatrix bela bhavya bianca bjorn bodhi bruno cadence
caleb carla carmen cedric celia chandra chitra cira clara colette
dagmar dalia damian daria deepak delia devika dilan divya dmitri
dorian edith eleni elias elina elodie emil enzo esha eshan esme
fabio farah farhan felix fiona flora franka freya gabor gauri
gemma georgi gita greta gustav hana harini harsha havel heidi
helena hugo ilya imran indira ingrid irina iris isolde ivar jaden
jarek jasmin jatin javier jelena jonas joris juno kaia kalinda
karim kasper katya kavya kiran klara koen lakshmi lars latika
leena lena leonie liana linnea lucia lucas magnus maja malik manav
maren marek marisol matteo mila mira nadia nandini natan nikhil
niko nina noor nuria olen olga omkar oorja orla oskar pablo paloma
pavel petra pooja pranav priya quintus rachna radek rafael rahul
rasmus rekha renata rhea rosa rustam saga sameer sanjay sanna
sasha selma senna serge sigrid simone sofia stefan svea tamara
tanvi tarek tatiana thea tibor tomas torsten trisha uday ujwal
ulla ulrich uma vadim valeria varsha veda vera viggo vikram vilma
wanda willem yamini yara yash ylva yuri zaid zara zenon zoltan
zora zuri alma bex cato dara eero fenna gero hilde ilma jarl kajsa
lior nael oona pim risto suvi timo urho vito wren xanthe
"""

NAMES = _RAW.split()

PAD, EOS = 0, 1                      # id 0 = padding, id 1 = end-of-name
CHARS = sorted(set("".join(NAMES)))  # the letters that actually occur
STOI = {c: i + 2 for i, c in enumerate(CHARS)}   # ids 2..
ITOS = {i: c for c, i in STOI.items()}
VOCAB_SIZE = len(STOI) + 2           # includes PAD and EOS
MAXLEN = max(len(n) for n in NAMES) + 1          # +1 leaves room for EOS


def encode(name):
    """'aarav' -> [2, 2, 19, 2, 23, 1, 0, 0]  (letters, EOS, then PAD up to MAXLEN)."""
    ids = [STOI[c] for c in name] + [EOS]
    return ids + [PAD] * (MAXLEN - len(ids))


def decode(ids):
    """Inverse of encode: stops at EOS, skips PAD."""
    out = []
    for i in ids:
        i = int(i)
        if i == EOS:
            break
        if i != PAD:
            out.append(ITOS[i])
    return "".join(out)
