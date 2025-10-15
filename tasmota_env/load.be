# load()

def load(filename, globalname)
  import global
  var code = compile(filename, "file")
  var res = code()
  if (globalname != nil)
    global.(globalname) = res
  end
  return res
end

return load
