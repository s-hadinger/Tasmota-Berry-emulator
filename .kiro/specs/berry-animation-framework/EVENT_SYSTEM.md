# Event System Documentation

The Berry Animation Framework includes a comprehensive event system that enables responsive, interactive animations. This system allows animations to react to external events like button presses, timers, brightness changes, and custom events.

## Overview

The event system consists of several key components:

- **EventHandler**: Individual event handlers that execute callbacks when events occur
- **EventManager**: Central manager that coordinates event registration, triggering, and execution
- **DSL Integration**: Support for event handlers directly in the Animation DSL
- **Animation Engine Integration**: Built-in support for event processing in the animation loop

## Core Components

### EventHandler Class

The `EventHandler` class represents a single event handler with the following properties:

```berry
var handler = animation.EventHandler(
  event_name,     # String: Name of the event (e.g., "button_press")
  callback_func,  # Function: Callback to execute when event occurs
  priority,       # Integer: Handler priority (higher = executed first)
  condition,      # Function: Optional condition function (returns true/false)
  metadata        # Map: Additional event metadata
)
```

**Methods:**
- `execute(event_data)` - Execute the handler if conditions are met
- `set_active(active)` - Enable/disable the handler
- `get_info()` - Get handler information for debugging

### EventManager Class

The `EventManager` class coordinates all event handling:

```berry
var manager = animation.EventManager()
```

**Methods:**
- `register_handler(event_name, callback, priority, condition, metadata)` - Register an event handler
- `unregister_handler(handler)` - Remove an event handler
- `trigger_event(event_name, event_data)` - Trigger an event
- `get_registered_events()` - List all registered event names
- `get_handlers(event_name)` - Get handlers for a specific event
- `clear_all_handlers()` - Remove all handlers
- `set_event_active(event_name, active)` - Enable/disable all handlers for an event

## Animation Module Integration

The animation module provides convenient functions for event management:

```berry
# Register an event handler
var handler = animation.register_event_handler(
  "button_press",
  def(event_data) 
    print("Button pressed!")
    # Add flash animation (auto-starts if engine is running)
    var flash = animation.solid(0xFFFFFFFF)
    engine.add_animation(flash)
  end,
  10,   # High priority
  nil,  # No condition
  {}    # No metadata
)

# Trigger an event
animation.trigger_event("button_press", {"button": "main"})

# Unregister handler
animation.unregister_event_handler(handler)
```

## DSL Integration

The Animation DSL supports event handlers with natural syntax:

### Basic Event Handler

```dsl
strip length 30
color red = #FF0000

# Simple event handler
on button_press: solid(red)

# Event handler with parameters
on timer(5s): solid(red)

# Main animation sequence
sequence main {
  play solid(red) for 2s
}

run main
```

### Event Handler with Actions

```dsl
# Multiple actions in event handler
on button_press:
  interrupt current
  solid(white) repeat 3 times
  resume after 1s

# Conditional event handling
on brightness_change:
  if brightness > 80: solid(yellow)
  else: solid(blue)
```

### Supported Event Types

The DSL recognizes these built-in event types:

- `startup` - System startup
- `shutdown` - System shutdown  
- `button_press` - Button press event
- `button_hold` - Button hold event
- `motion_detected` - Motion sensor trigger
- `brightness_change` - Ambient brightness change
- `timer(duration)` - Timer events with specified intervals
- `time` - Time-based events
- `sound_peak` - Audio peak detection
- `network_message` - Network message received
- Custom event names (any identifier)

## Event Priority System

Events are processed in priority order (higher numbers first):

```berry
# High priority handler (executes first)
animation.register_event_handler("test", callback1, 10, nil, nil)

# Medium priority handler
animation.register_event_handler("test", callback2, 5, nil, nil)

# Low priority handler (executes last)
animation.register_event_handler("test", callback3, 1, nil, nil)
```

## Conditional Event Handlers

Event handlers can include conditions that must be met for execution:

```berry
# Only execute if brightness data is present
var condition = def(event_data) 
  return event_data.contains("brightness") 
end

animation.register_event_handler(
  "brightness_change",
  def(event_data)
    if event_data["brightness"] > 80
      print("Bright environment detected")
    end
  end,
  0,
  condition,  # Condition function
  nil
)
```

## Global Event Handlers

Global handlers respond to all events:

```berry
# Monitor all events
animation.register_event_handler(
  "*",  # Global event name
  def(event_data)
    var event_name = event_data["event_name"]
    print(f"Event triggered: {event_name}")
  end,
  1,    # Low priority (after specific handlers)
  nil,
  {"type": "global_monitor"}
)
```

## Event Metadata

Handlers can include metadata for configuration:

```berry
# Timer event with metadata
animation.register_event_handler(
  "timer",
  def(event_data)
    print(f"Timer: {event_data['interval']}ms")
  end,
  0,
  nil,
  {"interval": 5000, "repeat": true}  # Metadata
)
```

## Animation Engine Integration

The AnimationEngine includes built-in event processing and control methods:

### Event Processing

Events are processed automatically during the animation loop:

```berry
var engine = animation.create_engine(strip)
engine.run()  # Auto-starts all animations and enables event processing in fast_loop
```

### Interrupt and Resume

The engine supports interrupting and resuming animations:

```berry
# Interrupt current animations
engine.interrupt_current()

# Interrupt all animations
engine.interrupt_all()

# Interrupt specific animation by name
engine.interrupt_animation("my_animation")

# Resume animations
engine.resume()

# Resume after delay (placeholder for future implementation)
engine.resume_after(1000)  # 1 second delay
```

## Event Queue

The event system includes a queue to handle events triggered during event processing:

```berry
# This handler triggers another event
animation.register_event_handler("chain_start", def(event_data)
  print("First event")
  animation.trigger_event("chain_next", {})  # Queued for later processing
end, 0, nil, nil)

animation.register_event_handler("chain_next", def(event_data)
  print("Second event")
end, 0, nil, nil)

# Trigger the chain
animation.trigger_event("chain_start", {})
# Output: "First event", then "Second event"
```

## Error Handling

The event system includes robust error handling:

```berry
# Events that cause errors don't crash the system
animation.register_event_handler("error_test", def(event_data)
  raise "test_error", "This is a test error"
end, 0, nil, nil)

# This will print an error message but continue processing
animation.trigger_event("error_test", {})
```

## Performance Considerations

The event system is designed for embedded environments:

- **Minimal Memory Usage**: Simple data structures and efficient algorithms
- **Non-blocking Processing**: Events are processed during fast_loop without blocking
- **Priority-based Execution**: Important events are processed first
- **Condition Filtering**: Avoid unnecessary callback execution
- **Queue Management**: Prevents recursive event processing

## Best Practices

### 1. Use Appropriate Priorities

```berry
# Critical system events - high priority
animation.register_event_handler("emergency_stop", callback, 100, nil, nil)

# User interactions - medium priority  
animation.register_event_handler("button_press", callback, 50, nil, nil)

# Background monitoring - low priority
animation.register_event_handler("status_update", callback, 1, nil, nil)
```

### 2. Include Conditions for Efficiency

```berry
# Only process brightness events with valid data
var brightness_condition = def(event_data)
  return event_data.contains("brightness") && 
         type(event_data["brightness"]) == "int"
end

animation.register_event_handler("brightness_change", callback, 0, brightness_condition, nil)
```

### 3. Use Metadata for Configuration

```berry
# Timer configuration in metadata
animation.register_event_handler("heartbeat", callback, 0, nil, {
  "interval": 1000,
  "enabled": true,
  "description": "System heartbeat monitor"
})
```

### 4. Clean Up Handlers

```berry
# Store handler references for cleanup
var handlers = []

handlers.push(animation.register_event_handler("event1", callback1, 0, nil, nil))
handlers.push(animation.register_event_handler("event2", callback2, 0, nil, nil))

# Clean up when done
for handler : handlers
  animation.unregister_event_handler(handler)
end
```

## Examples

### Simple Button Handler

```berry
# Flash white when button is pressed
animation.register_event_handler(
  "button_press",
  def(event_data)
    var flash = animation.solid(0xFFFFFFFF)
    engine.add_animation(flash)  # Auto-starts if engine is running
  end,
  10,
  nil,
  nil
)
```

### Timer-based Animation

```berry
# Change colors every 5 seconds
animation.register_event_handler(
  "timer",
  def(event_data)
    var colors = [0xFFFF0000, 0xFF00FF00, 0xFF0000FF]  # Red, Green, Blue
    var color = colors[tasmota.millis() / 5000 % 3]
    var anim = animation.solid(color)
    engine.clear()
    engine.add_animation(anim)  # Auto-starts if engine is running
  end,
  0,
  nil,
  {"interval": 5000}
)
```

### Brightness-responsive Animation

```berry
# Adjust animation based on ambient brightness
animation.register_event_handler(
  "brightness_change",
  def(event_data)
    var brightness = event_data["brightness"]
    if brightness > 80
      # Bright environment - use subtle colors
      var anim = animation.solid(0xFF404040)  # Dim white
    else
      # Dark environment - use bright colors
      var anim = animation.solid(0xFFFFFFFF)  # Bright white
    end
    engine.clear()
    engine.add_animation(anim)  # Auto-starts if engine is running
  end,
  5,
  def(data) return data.contains("brightness") end,
  {"type": "brightness_monitor"}
)
```

### DSL Event Example

```dsl
strip length 60

# Define colors
color red = #FF0000
color blue = #0000FF
color white = #FFFFFF

# Define animations
animation flash_red = solid(red)
animation flash_blue = solid(blue)
animation flash_white = solid(white)

# Event handlers
on button_press: flash_white
on timer(3s): flash_blue
on startup: flash_red

# Main sequence
sequence main {
  play flash_red for 2s
  play flash_blue for 2s
  repeat forever
}

run main
```

## Integration with Tasmota

The event system is designed to integrate with Tasmota's event system:

```berry
# Example Tasmota integration (conceptual)
def tasmota_button_handler()
  animation.trigger_event("button_press", {
    "button": "main",
    "timestamp": tasmota.millis(),
    "state": "pressed"
  })
end

# Register with Tasmota's button system
# tasmota.add_rule("Button1#State", tasmota_button_handler)
```

## Troubleshooting

### Common Issues

1. **Events not triggering**: Check event name spelling and handler registration
2. **Handlers not executing**: Verify conditions and handler active state
3. **Wrong execution order**: Check handler priorities
4. **Memory issues**: Clean up unused handlers

### Debugging

```berry
# List all registered events
var events = animation.get_registered_events()
print(f"Registered events: {events}")

# Get handlers for specific event
var handlers = animation.get_event_handlers("button_press")
for handler_info : handlers
  print(f"Handler: priority={handler_info['priority']}, active={handler_info['is_active']}")
end

# Test event triggering
animation.trigger_event("test", {"debug": true})
```

The event system provides a powerful foundation for creating responsive, interactive LED animations that can react to real-world events and user interactions.