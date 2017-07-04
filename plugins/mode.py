import os.path


dev    = os.path.exists(".dev")
card   = os.path.exists(".card")
sushi  = os.path.exists(".sushi")
uranai = not any([card, sushi])

test_prefix = "^test " if dev else "^(?!test ).*"
