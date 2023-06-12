from spanlp.palabrota import Palabrota
from better_profanity import profanity


class TextFilter:
    def __init__(self):
        self.palabrota = Palabrota(censor_char="*", include=['subnormal', 'tus muertos', 'maricón', ''])
        profanity.load_censor_words()
        self.custom_badwords = ['idiot',]

    def filter_text(self, texto):
        # Spanish filter
        texto = self.palabrota.censor(texto)
        # English filter
        texto = profanity.censor(texto)
        return texto