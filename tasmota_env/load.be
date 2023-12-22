# load()

def load(name)
  var code = compile(name, "file")
  code()
end

return load
