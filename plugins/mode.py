import os.path


dev    = os.path.exists(".dev")
mode   = os.path.exists(".card")
sushi  = os.path.exists(".sushi")
uranai = not any([mode, sushi])

test_prefix = "^test " if dev else "^(?!test ).*"
