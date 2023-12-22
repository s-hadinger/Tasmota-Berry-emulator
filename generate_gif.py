# test

import argparse
from PIL import Image
import imageio as iio
import json

leds = None
images = []

class Led_GIF:
  leds = None
  name = None
  img = None

  def __init__(self, images, leds):
    self.leds = leds
    self.images = images

  def draw(self, t, buf):
    img = Image.new('RGB', (self.leds * 9 + 1, 10))
    for i in range(self.leds):
      for x in range(8):
        for y in range(8):
          img.putpixel((i * 9 + 1 + x, y + 1), (buf[i*3+1], buf[i*3], buf[i*3+2]))
    self.images.append(img)   # add image to series

  def save(self):
    pass


def run(fname, fout):
  global leds
  global images
  with open(fname, 'r', newline='') as f:
    for line in f.readlines():
      line = line.strip()
      jline = json.loads(line)

      if 'leds' in jline:
        if leds == None:
          leds = jline['leds']
        else:
          raise Exception("More than one set of leds")
      elif 't' in jline and 'buf' in jline:
        # parse line
        timestamp = jline['t']
        buf = bytes.fromhex(jline['buf'])
        # print(f"timestamp: {timestamp:5d} buf: {buf.hex()}")
        gif = Led_GIF(images, leds)
        gif.draw(timestamp, buf)

  iio.mimwrite(fout, images, format='GIF', loop=0, duration=0.05, fps=20, subrectangles=True)#, duration=1)      

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-o', '--output', type=str, default='out.gif', help="output to file")
  parser.add_argument('input', help="input file in JSONL format from Berry Tasmota emulator")
  args = parser.parse_args()
  # Example:
  # `python3 generate_gif.py -o aa bb` -> `Namespace(output='aa', input='bb')`
  run(args.input, args.output)

if __name__ == '__main__':
  main()
