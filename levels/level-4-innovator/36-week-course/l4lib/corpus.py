"""corpus.py - the ~7,000-character TinyGPT corpus and a seeded toy-grammar generator.

Used in weeks 8-19: Week 8 (bag-of-words vs order sentences, via toy_sentences),
Weeks 14-17 and 19 (TinyGPT training and ablations on CORPUS).

CORPUS is the course author's own typed text (lowercase, minimal punctuation, heavy
repetition so a tiny model can learn it). Nothing is downloaded.
toy_sentences(n, seed) produces simple subject-verb-object sentences; it is a
stand-in generator for teaching, not a model.
"""
import random

CORPUS = """
the sun rose over the quiet town and the baker opened her door.
the baker made bread every morning before the sun rose.
the boy walked to school with a book under his arm.
the girl walked to school with a kite under her arm.
the teacher asked a question and the class went quiet.
a question is a small door and an answer is a room behind it.
the river ran past the town and the town grew beside the river.
in the morning the river was quiet and in the evening it was loud.
the old man fed the birds by the river every single morning.
the birds knew the old man and the old man knew the birds.
a bridge crossed the river and the children crossed the bridge.
under the bridge the water was cold and dark and slow.
the market opened at noon and closed when the sun went down.
at the market you could buy bread and fish and rope and salt.
the fisherman sold fish and the baker sold bread and both were happy.
the rope maker made rope and nobody asked how the rope was made.
a cat slept on the wall beside the market every afternoon.
the cat did not care about bread or fish or rope or salt.
the cat cared about the sun on the wall and nothing else.
when it rained the market closed and the cat found a dry door.
the rain fell on the roofs and ran down into the river.
the river rose and the bridge held and the town slept.
in the winter the river froze and the children walked on it.
the old man told them not to walk on the river in the winter.
the children listened to the old man because the old man was right.
a story is a road and a road goes somewhere if you follow it.
the teacher said that a question is better than a guess.
the boy said that a guess is better than nothing at all.
the girl said that both of them were right and both were wrong.
the class laughed and the teacher wrote the question on the board.
every morning the baker counted her loaves before she opened.
every evening the fisherman counted his fish before he went home.
counting is a quiet thing and it makes the world hold still.
the old man did not count the birds because the birds moved too much.
the sun rose over the quiet town and the day began again.
a town is a machine made of people and roads and small kindnesses.
the baker gave bread to the old man and the old man fed the birds.
the birds sang over the river and the children heard them sing.
the teacher opened a window so the class could hear the birds.
a window is a door for sound and light but not for people.
the boy drew a bird in his book and the girl drew a river.
the teacher drew a bridge between the bird and the river.
that is how a lesson works said the teacher and the class went quiet.
in the spring the ice broke and the river ran fast and brown.
the fisherman waited because the fish would come back in time.
waiting is work even when it does not look like work.
the rope maker made a long rope and gave it to the fisherman.
the fisherman tied his boat to the bridge with the long rope.
the boat held and the river ran and the town went on.
the cat watched the boat from the wall and did not move.
the sun went down behind the roofs and the market closed.
the baker swept her floor and the teacher closed her window.
the old man walked home along the river in the last of the light.
the children ran ahead of him and he did not try to keep up.
a town at night is a quiet machine and it still runs.
in the morning the baker opened her door before the sun rose.
the boy asked the old man why the birds came back every year.
the old man said that the birds remember the shape of the river.
the girl asked whether a river has a shape at all.
the old man said that everything has a shape if you watch it long enough.
the teacher wrote the word shape on the board and drew a river beside it.
the class copied the word and nobody copied the river.
the boy copied the river and left the word out.
the teacher said that both of those are notes and neither one is wrong.
a note is a rope you throw to the person you will be tomorrow.
the rope maker liked that line and asked the teacher to write it down.
the teacher wrote it on a small card and gave it to the rope maker.
the rope maker kept the card in his pocket for the rest of the winter.
the fisherman found a broken oar under the bridge one cold morning.
he carried the oar to the rope maker and the rope maker mended it.
mending is quieter than making and it is often harder.
the baker mended a torn sack with thread and did not tell anyone.
the teacher mended a broken chair and told the whole class about it.
the old man mended nothing because the old man threw nothing away.
the cat mended nothing and the cat was not ashamed.
in the summer the market stayed open until the light was gone.
the children ran between the stalls and nobody stopped them.
the fisherman gave a small fish to the cat and the cat took it.
the cat did not thank the fisherman because cats do not do that.
the fisherman did not mind because he had not asked for thanks.
a gift with a price on it is a trade and both of them are fine.
the baker traded bread for fish and the fisherman traded fish for bread.
the rope maker traded rope for both and everyone went home full.
the teacher traded questions for answers and the class grew.
the old man traded nothing and the town gave him bread anyway.
in the autumn the leaves fell into the river and floated to the sea.
the boy asked where the sea was and the girl said far past the bridge.
the old man said the sea is where the river stops explaining itself.
the teacher wrote that on the board and did not explain it.
the class thought about it for a long time and then went home.
some questions are meant to be carried and not answered.
the boy carried that one all winter and asked about it in the spring.
the old man had forgotten saying it and laughed a long time.
the girl remembered every word and told him what he had said.
the old man said that is why we need more than one person in a town.
the baker heard the story and put it in her bread song.
she sang the bread song every morning while the loaves rose.
the loaves did not care about the song but the baker did.
a song is a way of counting that does not feel like counting.
the fisherman sang nothing and counted his fish in his head.
the rope maker hummed and lost count and started over every time.
the teacher sang badly and the class loved her for it.
the children sang the bread song walking home over the bridge.
the old man heard them from the river and fed the birds and smiled.
the birds did not sing back because the birds were eating.
in the last week of winter the ice broke with a sound like a door.
the whole town heard it and everybody knew what it meant.
the fisherman untied his boat and the rope maker checked the rope.
the baker made extra bread and the teacher opened the window.
the old man walked to the bridge and watched the brown water go.
the children came running and the cat stayed on the wall.
the sun rose over the quiet town and the day began again.
"""

TEXT = CORPUS.strip()

_SUBJECTS = ["the dog", "the cat", "the baker", "the postman", "the girl", "the boy",
             "the teacher", "the fisherman"]
_VERBS = ["bit", "saw", "chased", "helped", "found", "called"]
_OBJECTS = ["the dog", "the cat", "the baker", "the postman", "the girl", "the boy",
            "the teacher", "the fisherman"]


def toy_sentences(n, seed=0):
    """Return n seeded 'subject verb object' sentences (subject != object).

    Same (n, seed) always gives the same list. Because word order carries the
    meaning ('the dog bit the postman' vs 'the postman bit the dog'), these are
    the sentences where a bag of words fails and order matters (Week 8).
    """
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        s, v, o = rng.choice(_SUBJECTS), rng.choice(_VERBS), rng.choice(_OBJECTS)
        if s != o:
            out.append(f"{s} {v} {o}")
    return out
