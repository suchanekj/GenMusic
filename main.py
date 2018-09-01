import os

import config
import melody
import write
import play
import genetic
import miditotxt

if not os.path.exists("pianotxt/"):
    miditotxt.makecorpus()
genetic.autorun()
config.init()
melody.generate()
write.write([melody.melody], [melody.rhythm])
play.autoplay()
