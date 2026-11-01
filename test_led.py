# import neopixel
# import board
# import time

# try:
#     pixels = neopixel.NeoPixel(board.D18, 8, auto_write=False)
#     pixels.fill((255,0,0))
#     pixels.show()
#     print("Sleeping for 3s now board should be red hopefully\n")
#     time.sleep(3)
#     pixels.fill((0,0,0))
#     pixels.show()
#     print("Now, I die lol\n")
# except:
#     print("lol")


#!/usr/bin/env python3

import time
import board
import neopixel

LED_COUNT = 24

pixels = neopixel.NeoPixel(
    board.D18,
    LED_COUNT,
    auto_write=False
)

try:
    for i in range(LED_COUNT):
        pixels.fill((0, 0, 0))
        pixels[i] = (255, 0, 0)
        pixels.show()

        print(f"LED {i + 1} activated")
        time.sleep(0.5)

finally:
    pixels.fill((0, 0, 0))
    pixels.show()
