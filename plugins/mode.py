import os.path


dev    = os.path.exists(".dev")
card   = os.path.exists(".card") or dev
sushi  = os.path.exists(".sushi") or dev
uranai = not any([card, sushi]) or dev

test_prefix = "^test " if dev else "^(?!test ).*"
