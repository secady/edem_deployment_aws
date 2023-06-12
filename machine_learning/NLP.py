from spanlp.palabrota import Palabrota
from better_profanity import profanity

palabrota = Palabrota()

text = "Tus muertos cabron"
#returns True if it contains bad language
print(palabrota.contains_palabrota(text))

dirty_text = "That l3sbi4n did a very good H4ndjob."
#returns True if it contains bad language

profanity.contains_profanity(dirty_text)