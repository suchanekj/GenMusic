import random
import melody
import write
import play


melody.generate()
write.write([melody.melody], [melody.rhythm])
play.autoplay()
