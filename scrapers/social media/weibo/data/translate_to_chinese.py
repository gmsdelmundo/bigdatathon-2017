# -*- coding: utf-8 -*-
from yandex_translate import YandexTranslate
import sys

reload(sys)
sys.setdefaultencoding('utf8')

translate = YandexTranslate('trnsl.1.1.20171205T165353Z.97d52ad0fa0d3795.b9af51a5e3f8283c5978d4da3ea3dfd0b2cd6ea1')
print translate.translate(sys.argv[1], 'en-zh')['text'][0]
