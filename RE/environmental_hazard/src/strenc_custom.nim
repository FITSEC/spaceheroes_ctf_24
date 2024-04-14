# Stolen from https://github.com/Yardanico/nim-strenc
# Modified to reduce complexity significantly

# Code is based on https://forum.nim-lang.org/t/1305
# and https://forum.nim-lang.org/t/338
import macros

type
  # Use a distinct string type so we won't recurse forever
  estring = distinct string

# Use a "strange" name
proc gkkaekgaEE(s: estring, key: int): string {.inline.} =
  # We need {.noinline.} here because otherwise C compiler
  # aggresively inlines this procedure for EACH string which results
  # in more assembly instructions
  var k = key
  result = string(s)
  for i in 0 ..< result.len:
    for f in [0, 8, 16, 24]:
      result[i] = chr(uint8(result[i]) xor uint8((k shr f) and 0xFF))
    k = k +% 1

var encodedCounter {.compileTime.} = 0x7FFFFFF0

# Use a term-rewriting macro to change all string literals
macro encrypt*{s}(s: string{lit}): untyped =
  var encodedStr = gkkaekgaEE(estring($s), encodedCounter)

  template genStuff(str, counter: untyped): untyped = 
    {.noRewrite.}:
      gkkaekgaEE(estring(`str`), `counter`)
  
  result = getAst(genStuff(encodedStr, encodedCounter))
  encodedCounter = (encodedCounter *% 16777619) and 0x7FFFFFF0
