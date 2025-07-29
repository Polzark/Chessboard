import neopixel
import board
import time

pixels = neopixel.NeoPixel(board.D18, 8, auto_write=False)
pixels.fill((255,0,0,0))
pixels.show()
print("Sleeping for 3s now board should be read hopefully\n")
time.sleep(3)
pixels.fill((0,0,0,0))
pixels.show()
print("Now, I die lol\n")
