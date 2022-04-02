import RPi.GPIO as GPIO
import sys
import time
import datetime

delay = 0.003

data = 14
latch = 15
clock = 18


GPIO.setmode(GPIO.BCM)
GPIO.setup((data,latch,clock),GPIO.OUT)


tenth_hours = [65280, 61186, 63234]
hours = [65280, 61188, 63236, 59140 ,64260, 60164, 62212, 58116, 6477, 260676]

tenth_minutes = [65280, 61192, 63240, 59144, 64264, 60168]
minutes = [65280, 28560, 30608, 26512, 31632, 27536, 29584, 25488, 32144, 28048]

tenth_seconds = [65280, 61216, 63264, 59168, 64288, 60192]
seconds = [65280, 61185, 63233, 59137, 64257, 60161, 62209, 57857, 64769,  60673]



def latch_down():
  global clock, latch, data
  GPIO.output(clock,0)
  GPIO.output(latch,0)
  GPIO.output(clock,1)


def latch_up():
  global clock, latch, data
  GPIO.output(clock,0)
  GPIO.output(latch,1)
  GPIO.output(clock,1)



def shift_update(number):

  latch_down()
  for bit in bin(number)[2:]:
    GPIO.output(clock, 0)
    GPIO.output(data, int(bit))
    GPIO.output(clock, 1)
  latch_up()


def count():
  date = datetime.datetime.now()
  hrs = int(date.strftime("%H"))
  mins = int(date.strftime("%M"))
  secs = int(date.strftime("%S"))


  hours_tens = hrs // 10
  hours_ones = hrs % 10

  mins_tens = mins // 10
  mins_ones = mins % 10

  seconds_tens = secs // 10
  seconds_ones = secs % 10

  shift_update(seconds[seconds_ones])
  shift_update(tenth_seconds[seconds_tens])
  time.sleep(delay)

  shift_update(tenth_hours[hours_tens])
  shift_update(hours[hours_ones])
  time.sleep(delay)


  shift_update(tenth_minutes[mins_tens])
  shift_update(minutes[mins_ones])
  time.sleep(delay)


def main():

  try:
      while 1:
        count()
  except KeyboardInterrupt:
    print("Keyboard Interrupt.")

  except:
    print ("Other error or exception occurred!")


  finally:
    print ("GPIO cleanup. Ending program.")
    GPIO.cleanup()

if __name__ == "__main__":
  print("Running binary clock ...")
  main()
else:
  print("Programing ending.")
  GPIO.cleanup()
