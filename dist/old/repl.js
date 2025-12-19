var term = new Terminal({
    cols: 80,
    rows: 25,
    screenKeys: true,
    useStyle: true,
    cursorBlink: true,
});
term.colors[256] = '#1a2d2d';
term.colors[257] = '#d0d0d0';
term.open(document.getElementById("terminal"));

var readline = (function () {
  var history = [], historyIndex = 0, linePos = 0;
  var content = "", line = null;
  function sendBack(n) {
    if (n > 0)
      term.write("\033[" + n + "D");
  }
  function selectHistory() {
    history[historyIndex];
    sendBack(content.length);
    term.write(content = history[historyIndex]);
    term.write("\033[K");
    linePos = content.length;
  }
  function keyUp() {
    if (historyIndex > 0) {
      historyIndex--;
      selectHistory()
    }
  }
  function keyDown() {
    if (historyIndex < history.length - 1) {
      historyIndex++;
      selectHistory()
    }
  }
  function keyLeft() {
    if (linePos) {
      linePos--;
      term.write("\b");
    }
  }
  function keyRight() {
    if (linePos < content.length) {
      term.write(content[linePos++]);
    }
  }
  function insert(data) {
    if (linePos == content.length) {
      content += data;
      term.write(data);
    } else {
      var tail = data + content.slice(linePos);
      term.write(tail);
      content = content.slice(0, linePos) + tail;
      sendBack(tail.length - 1);
    }
    linePos++;
  }
  function backspace() {
    if (linePos > 0) {
      if (linePos == content.length) {
        content = content.slice(0, --linePos);
        term.write("\b \b");
      } else {
        var tail = content.slice(linePos);
        term.write("\b" + tail + " ");
        sendBack(tail.length + 1);
        content = content.slice(0, --linePos) + tail;
      }
    }
  }
  function remove() {
    if (linePos < content.length) {
      var tail = content.slice(linePos + 1);
      term.write(tail + " ");
      sendBack(tail.length + 1);
      if (linePos > 0)
        content = content.slice(0, linePos) + tail;
      else
        content = tail;
    }
  }
  return {
    putchar: function (data) {
      switch (data) {
        case "\033[A": // up
          keyUp();
          break;
        case "\033[B": // down
          keyDown();
          break;
        case "\033[C": // right
          keyRight();
          break;
        case "\033[D": // left
          keyLeft();
          break;
        case "\b": case "\177":
          backspace();
          break;
        case "\033[3~":
          remove();
          break;
        case "\r": case "\n":
          history.push(content)
          historyIndex = history.length;
          line = content + "\n";
          content = "";
          linePos = 0;
          term.write("\r\n");
          break;
        default:
          if (data.length == 1)
            insert(data);
          break;
      }
    },
    readline: async function () {
      const waitms = delay => new Promise(resolve => setTimeout(resolve, delay));
      while (!line) await waitms(0);
      var str = line;
      line = null;
      return str;
    }
  }
})();

term.on('data', function (data) {
  readline.putchar(data);
});
async function waitLineText(prompt) {
  return readline.readline(prompt);
}
async function writeOutputText(text) {
  term.write(text.replace("\n", "\r\n"));
}