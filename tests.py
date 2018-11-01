from qrandom import qrandom as qr
qgen = qr.build_generator(1)
for i in range(100):
    answer = qr.inclusive_between(qgen, 1, 17)
    if answer == 0:
        break
