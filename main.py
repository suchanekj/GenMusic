import config
import melody
import write
import play
import genetic

genetic.autorun()
config.init()
melody.generate()
write.write([melody.melody], [melody.rhythm])
# play.autoplay()
