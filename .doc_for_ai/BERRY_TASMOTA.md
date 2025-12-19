# Berry for Tasmota

Tasmota-specific Berry features and extensions. Complements `BERRY_LANGUAGE_REFERENCE.md`.

Berry is embedded in all ESP32-based Tasmota firmwares (not ESP8266). Used for drivers, automations, and UI extensions.

## Tasmota Modules

| Module | Description | Import |
|--------|-------------|--------|
| `tasmota` | Core integration | Auto-imported |
| `light` | Light control | Auto-imported |
| `energy` | Energy monitoring | Auto-imported |
| `mqtt` | MQTT operations | `import mqtt` |
| `webserver` | Web extensions | `import webserver` |
| `gpio` | GPIO control | `import gpio` |
| `persist` | Data persistence | `import persist` |
| `path` | File operations | `import path` |
| `display` | Display drivers | `import display` |
| `crypto` | Cryptography | `import crypto` |
| `re` | Regular expressions | `import re` |
| `mdns` | mDNS support | `import mdns` |
| `ULP` | Ultra Low Power | `import ULP` |

## Constants

```berry
# GPIO
gpio.INPUT, gpio.OUTPUT, gpio.PULLUP, gpio.PULLDOWN, gpio.HIGH, gpio.LOW
gpio.REL1, gpio.KEY1, gpio.LED1, gpio.I2C_SCL, gpio.I2C_SDA

# Serial
serial.SERIAL_8N1, serial.SERIAL_7E1

# Webserver
webserver.HTTP_GET, webserver.HTTP_POST, webserver.HTTP_ANY
webserver.HTTP_OFF, webserver.HTTP_USER, webserver.HTTP_ADMIN
```

## File System

```berry
load("filename")              # Load .be or .bec file
tasmota.compile("file.be")    # Compile to .bec
```

**Autostart**: `autoexec.be` runs at boot.

## Core Tasmota Functions

```berry
# System
tasmota.get_free_heap()       # Free heap bytes
tasmota.memory()              # Memory stats map
tasmota.arch()                # "esp32", "esp32s2", etc.
tasmota.millis()              # Milliseconds since boot
tasmota.yield()               # Yield to system
tasmota.delay(ms)             # Block for ms (avoid in drivers)
tasmota.gc()                  # Garbage collection stats

# Commands
tasmota.cmd("command")        # Execute Tasmota command
tasmota.resp_cmnd_done()      # Respond "Done"
tasmota.resp_cmnd_error()     # Respond "Error"
tasmota.resp_cmnd_str(msg)    # Custom string response
tasmota.resp_cmnd(json)       # JSON response

# Configuration
tasmota.get_option(index)     # Get SetOption value
tasmota.read_sensors()        # Sensor JSON string
tasmota.wifi()                # WiFi info
tasmota.eth()                 # Ethernet info
```

## Rules and Events

```berry
# Add rules
tasmota.add_rule("trigger", function)
tasmota.add_rule(["trigger1", "trigger2"], function)  # AND logic
tasmota.remove_rule("trigger")

# Rule callback: function(value, trigger, msg)
tasmota.add_rule("Dimmer>50", def(val) print("Bright:", val) end)
tasmota.add_rule("ANALOG#A1>300", def(val) print("ADC:", val) end)
```

## Timers and Scheduling

```berry
# Timers (50ms resolution)
tasmota.set_timer(delay_ms, function)
tasmota.remove_timer(id)
tasmota.defer(function)       # Run next millisecond

# Cron
tasmota.add_cron("*/15 * * * * *", function, "id")
tasmota.remove_cron("id")
tasmota.next_cron("id")

# Time
tasmota.rtc()                 # Current time info
tasmota.time_dump(ts)         # Decompose timestamp
tasmota.time_str(ts)          # ISO 8601 string
tasmota.strftime(fmt, ts)
tasmota.strptime(str, fmt)
```

## Device Control

```berry
# Relays
tasmota.get_power()           # Array of relay states
tasmota.set_power(idx, state)

# Lights
light.get()                   # Current status
light.set({"power": true, "bri": 128, "hue": 120, "sat": 255})
# Attributes: power, bri (0-255), hue (0-360), sat (0-255), ct (153-500), rgb, channels
```

## Custom Commands

```berry
def my_cmd(cmd, idx, payload, payload_json)
  tasmota.resp_cmnd_done()
end
tasmota.add_cmd("MyCmd", my_cmd)
tasmota.remove_cmd("MyCmd")
```

## Drivers

Implement event methods in a class:

```berry
class MyDriver
  def every_second() end          # Called every second
  def every_50ms() end            # Called every 50ms
  def web_sensor()                # Add to web UI
    tasmota.web_send("{s}Label{m}Value{e}")
  end
  def json_append()               # Add to JSON teleperiod
    tasmota.response_append(',"MySensor":{"Value":123}')
  end
  def web_add_main_button()       # Button on main page
    import webserver
    webserver.content_send("<button onclick='la(\"&action=1\");'>Click</button>")
  end
  def button_pressed() end
  def mqtt_data(topic, idx, data, databytes) end
  def save_before_restart() end
end

tasmota.add_driver(MyDriver())
```

## Fast Loop

For high-frequency events (200Hz, 5ms):

```berry
tasmota.add_fast_loop(function)
tasmota.remove_fast_loop(function)
```

## GPIO

```berry
import gpio

gpio.pin_used(gpio.REL1)          # Check if used
gpio.pin(gpio.REL1)               # Physical GPIO number
gpio.digital_write(pin, gpio.HIGH)
gpio.digital_read(pin)
gpio.pin_mode(pin, gpio.OUTPUT)

# PWM
gpio.set_pwm(pin, duty, phase)
gpio.set_pwm_freq(pin, freq)

# DAC (ESP32: GPIO 25-26)
gpio.dac_voltage(pin, voltage_mv)

# Counters
gpio.counter_read(counter)
gpio.counter_set(counter, value)
```

## I²C

```berry
wire1.scan()                      # Scan for devices
wire1.detect(addr)                # Check device present
wire1.read(addr, reg, size)       # Read from device
wire1.write(addr, reg, val, size) # Write to device
wire1.read_bytes(addr, reg, size)
wire1.write_bytes(addr, reg, bytes)

# Find device on any bus
wire = tasmota.wire_scan(addr, i2c_index)
```

## MQTT

```berry
import mqtt

mqtt.publish(topic, payload, retain)
mqtt.subscribe(topic, callback)   # callback(topic, idx, payload_s, payload_b)
mqtt.unsubscribe(topic)
mqtt.connected()
```

## Web Server

```berry
import webserver

webserver.on("/page", def()
  webserver.content_send("<html>Content</html>")
end)

webserver.has_arg("param")
webserver.arg("param")
webserver.arg_size()
webserver.content_send(html)
webserver.html_escape(str)
```

## Persistence

```berry
import persist

persist.my_value = 123
persist.save()                    # Force save to flash
persist.has("key")
persist.remove("key")
persist.find("key", default)
```

## HTTP Client

```berry
cl = webclient()
cl.begin("https://example.com/api")
cl.set_auth("user", "pass")
cl.add_header("Content-Type", "application/json")
result = cl.GET()                 # or cl.POST(payload)
if result == 200
  response = cl.get_string()
end
cl.close()
```

## TCP/UDP

```berry
# TCP
tcp = tcpclient()
tcp.connect("192.168.1.100", 80)
tcp.write("GET / HTTP/1.0\r\n\r\n")
response = tcp.read()
tcp.close()

# UDP
u = udp()
u.begin("", 2000)                 # Listen on port
u.send("192.168.1.10", 2000, bytes("Hello"))
packet = u.read()                 # Returns bytes or nil
```

## Serial

```berry
ser = serial(rx_gpio, tx_gpio, baud, serial.SERIAL_8N1)
ser.write(bytes("Hello"))
data = ser.read()
ser.available()
ser.flush()
ser.close()
```

## Crypto

```berry
import crypto

# AES-GCM
aes = crypto.AES_GCM(key_32, iv_12)
encrypted = aes.encrypt(plaintext)
tag = aes.tag()

# Hashing
crypto.SHA256().update(data).finish()
crypto.MD5().update(data).finish()
crypto.HMAC_SHA256(key).update(data).finish()
```

## File System

```berry
import path

path.exists("file")
path.listdir("/")
path.remove("file")
path.mkdir("dir")
path.last_modified("file")
```

## Regular Expressions

```berry
import re

re.search("pattern", string)      # Returns matches array
re.searchall("pattern", string)   # All matches
re.split("/", "a/b/c")

# Compiled (faster for reuse)
pattern = re.compilebytes("\\d+")
re.search(pattern, string)
```

## Energy Monitoring

```berry
energy.voltage
energy.current
energy.active_power
energy.total

# Multi-phase
energy.voltage_phases[0]
energy.current_phases[1]
```

## Example: Sensor Driver

```berry
class MySensor
  var wire, addr, temperature
  
  def init()
    self.addr = 0x48
    self.wire = tasmota.wire_scan(self.addr, 99)
  end
  
  def every_second()
    if !self.wire return end
    var raw = self.wire.read(self.addr, 0x00, 2)
    self.temperature = raw / 256.0
  end
  
  def web_sensor()
    if !self.wire return end
    tasmota.web_send_decimal(f"{{s}}Temp{{m}}{self.temperature:.1f} °C{{e}}")
  end
  
  def json_append()
    if !self.wire return end
    tasmota.response_append(f',"MySensor":{{"Temp":{self.temperature:.1f}}}')
  end
end

tasmota.add_driver(MySensor())
```

## Common Patterns

### Custom Command with JSON Response

```berry
def my_status(cmd, idx, payload, payload_json)
  var response = {
    "Uptime": tasmota.millis(),
    "FreeHeap": tasmota.get_free_heap()
  }
  tasmota.resp_cmnd(json.dump(response))
end
tasmota.add_cmd("MyStatus", my_status)
```

### MQTT Automation

```berry
import mqtt

mqtt.subscribe("sensors/temperature", def(topic, idx, payload_s, payload_b)
  var data = json.load(payload_s)
  if data && data.find("temp") && data["temp"] > 25
    tasmota.cmd("Power1 ON")
  end
  return true
end)
```

### Web UI Button

```berry
class WebButton
  def web_add_main_button()
    import webserver
    webserver.content_send("<button onclick='la(\"&toggle=1\");'>Toggle</button>")
  end
  def web_sensor()
    import webserver
    if webserver.has_arg("toggle")
      var state = gpio.digital_read(2)
      gpio.digital_write(2, !state)
    end
  end
end
tasmota.add_driver(WebButton())
```

### Scheduled Task with Persistence

```berry
import persist

class ScheduledTask
  def init()
    if !persist.has("count") persist.count = 0 end
    tasmota.add_cron("0 */5 * * * *", /-> self.run(), "task")
  end
  def run()
    persist.count += 1
    print("Task run", persist.count, "times")
    persist.save()
  end
end
ScheduledTask()
```

### HTTP API Client

```berry
class WeatherAPI
  def fetch(city, api_key)
    var cl = webclient()
    cl.begin(f"http://api.example.com/weather?q={city}&key={api_key}")
    if cl.GET() == 200
      var data = json.load(cl.get_string())
      if data print(f"Temp: {data['temp']}°C") end
    end
    cl.close()
  end
end
```

### Rule-based Automation

```berry
# Multiple conditions (AND logic)
tasmota.add_rule(["ANALOG#A0>500", "Switch1#State=1"], def(values, triggers)
  print("ADC:", values[0], "Switch:", values[1])
  tasmota.cmd("Power2 ON")
end)

# Time-based
tasmota.add_rule("Time#Minute=30", def()
  if tasmota.rtc()["hour"] == 18
    tasmota.cmd("Dimmer 20")
  end
end)
```

## Best Practices

1. **Check nil returns** from Tasmota functions
2. **Use timers** instead of `delay()` to avoid blocking
3. **Use `persist`** for settings that survive reboots
4. **Use `tasmota.wire_scan()`** for I²C device detection
5. **Use fast_loop sparingly** - runs 200x/second
6. **Import modules only when needed** to save memory
