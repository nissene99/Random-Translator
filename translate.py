# Hier werden alle Module importiert

from datetime import datetime
from random import random
import translators as ts
import json

SPRACHEN = json.load(open('sprachen.json', encoding='utf-8'))  # Sprachen aus JSON-Datei laden
DEBUG = False


# Hier wird die Übersetzung durchgeführt, indem die Google-API aufgerufen wird
def translate(text, to_lang, from_lang='auto'):
	return ts.google(text, to_language=to_lang, from_language=from_lang)

# Das selbe wie oben, nur mit mehreren Sprachen
def batch_translate(text, sprachen=SPRACHEN.keys(), output=None):
	"""
	Übersetzt den Text in die angegebenen Sprachen.
	"""
	t0 = datetime.now()
	org_text = text
	for sprache in sprachen:
		if output is not None:
			msg = u"\nÜbersetze in {}...".format(SPRACHEN[sprache])
			output.insert("1.0", msg)
			output.update()
		else:
			if DEBUG:
				print("\nÜbersetze zu {}...".format(sprache).encode('utf-8'))
		if DEBUG:
			print("Übersetze in", sprache.encode('utf-8'))
		text = translate(text, sprache)
	text = translate(text, 'de')
	t1 = datetime.now()
	diff = t1 - t0
	# format diff to hours, minutes, seconds
	diff = str(diff).split('.')[0]
	if DEBUG:
		print(f"Übersetzung in {len(sprachen) + 1} Sprachen dauerte {diff}")
		print("Originaltext:", org_text, "Übersetzter Text:", text)
	return text


# Hier werden die zufälligen Sprachen ausgewählt
def random_translate(text, anzahl, output=None):
	# wähle zufällig anzahl Sprachen aus
	sprachen = []
	while len(sprachen) < anzahl:
		sprache = list(SPRACHEN.keys())[int(random() * len(SPRACHEN.keys()))]
		if sprache not in sprachen:
			sprachen.append(sprache)
	return batch_translate(text, sprachen, output)
