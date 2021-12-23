def recur(s, i=0, out=''):
    if i == len(s):
        print(out[1:])
    for j in reversed(range(i, len(s))):
        substr = s[i:j+1] 
        recur(s, j + 1, out + '+' + substr)
 
if __name__ == '__main__':
    s = 'ABCD'   
    recur(s)
 