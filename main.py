from conlib import Console as con

try:
    # inp : str = con.getchar(2)
    inp : str = con.input(replace_chars_with="*")
    print("xx", inp)
    print(hex(ord(inp[0])), len(inp))
finally:
    pass
    print("LOG")
    # print(con.log())
    print(*con.nlog(), sep="\n")