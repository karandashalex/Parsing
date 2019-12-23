# print('Flats characteristics:\n1. Rooms\n2. Area\n3. Address\n4. Floor\n5. Square\n6. Year\n7. Balcony\n8. Price')
# a,b = map(int, input('Choose characteristic: ').split())
# print(a)
# print(b)
# rubles = 10
# kop = 99
# print('I have got', rubles, 'rubles and', kop, 'kop')
# print('I have got %s rubles and %s kop' % (rubles, kop))
# print(41576//1000%10)
# print(41576%100)
# x = int(input())
# a = x//10000
# b = x//1000%10
# c = x//100%10
# d = x//10%10
# e = x%10
# print(a, b, c, d, e, sep=',')
# print('='.join(['1','2','3']))

a = int(input('Enter number: '))
count = 0
col_chet = col_nechet = 0
while a > 0:
    last = a % 10
    if last % 2 == 0:
        col_chet += 1
    else:
        col_nechet += +1
    count += 1
    a = a // 10
print('Count numbers: %d, chetnumbers: %d, nechetnumbers: %d' % (count, col_chet, col_nechet))
print('Count numbers: {all}, chetnumbers: {chet}, nechetnumbers: {nechet}'.format(all=count, chet=col_chet,
                                                                                  nechet=col_nechet))
