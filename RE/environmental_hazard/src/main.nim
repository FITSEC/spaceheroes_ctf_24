{.passC:"-masm=intel".}

import std/os
import std/osproc
import std/algorithm
import std/strutils
import strenc_custom
import art


# will either make reversing this a lot better or a lot worse. maybe both.
proc return_int(a: int): int {.asmNoStackFrame.} = 
  asm """
    mov rax, rdi
    pop rdi
    jmp rdi
  """

# decompiler death
proc get_envp(): ptr cstring {.asmNoStackFrame.} =
  asm """
    mov rax, r13
    jmp $+6
    .byte 0xe9,0xff,0xe7
    .byte 0x0f,0x5f
    jmp $-4
    
  """

# decompiler death 2: binja isn't fooled by this one edition
proc get_funny(): cstring {.asmNoStackFrame.} =
  asm """
    mov rax, 0xE7FFC871485B
    mov rcx, 0xe7ffc831485f
    jmp $-8
  """

# written this way to prevent strenc from hiding this one
proc check_funny() {.noinline.} =
  var a: seq[char] = @['s', 'p', 'a', 'c', 'e', 'h', 'e', 'r', 'o', 'e', 's']
  if $get_funny() != a:
    quit(return_int(1))


proc is_number(x: string): bool =
  try:
    discard parseInt(x)
    result = true
  except ValueError:
    result = false


check_funny()

var envvar: string = $get_envp()[]


iterator leetspeakify*(a: string): char {.noinline.} =
  var i = 0
  while i < len(a):
    if not is_number("" & a[i]):
      yield ($a[i]).replace("e", "3").replace("i", "1").replace("o", "0").replace("a", "4")[0]
    inc(i)


# let safearg = "lol"
# echo "safearg: ", safearg
# echo "argv0: ", commandLineParams()[0]
# echo "argv1: ", commandLineParams()[1]
# if commandLineParams()[0] != safearg:
#   discard execProcess("/proc/self/exe", args=["lol"], options={poEchoCmd})
#   quit()


var flag = ""
for i in leetspeakify("shctf{nEver_ToUcHing_nim_Again}"): flag = flag & cast[char](return_int(cast[int](i)))
# echo flag
if envvar == flag:
  discard flag
  echo envvar
  quit(return_int(0))
else:
  quit(return_int(1))

