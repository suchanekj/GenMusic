import os
import subprocess

import config
import melody
import write
import genetic
import miditotxt
import discriminator

melody.tim = 0.0
genetic.tim = 0.0
discriminator.tim = 0.0
write.tim = 0.0
miditotxt.tim = 0.0

if not os.path.exists("pianotxt/"):
    miditotxt.makecorpus()
if not os.path.exists("nn/"):
    discriminator.init()
    discriminator.learn()
else:
    discriminator.load()
geneticResNum = len([name for name in os.listdir('geneticresults/')
                  if os.path.isfile('geneticresults/' + name)]) - 1
if(geneticResNum >= 0):
    genetic.load(geneticResNum)
genetic.autorun()
config.init()
melody.generate()
write.write([melody.melody], [melody.rhythm])
write.save()

print("Melody time " + str(melody.tim))
print("Genetic time " + str(genetic.tim))
print("Discriminator time " + str(discriminator.tim))
print("Write time " + str(write.tim))
print("Miditotxt time " + str(miditotxt.tim))


python3_command = "python play.py"  # launch your python2 script using bash
process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

