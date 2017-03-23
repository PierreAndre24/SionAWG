import re

def ssplit2(seq,splitters):
    seq=list(seq)
    if splitters and seq:
        splitters=set(splitters).intersection(seq)
        if splitters:
            result=[]
            begin=0
            for end in range(len(seq)):
                if seq[end] in splitters:
                    if end > begin:
                        result.append(seq[begin:end])
                    begin=end+1
            if begin<len(seq):
                result.append(seq[begin:])
            return result
    return [seq]

def word_splitter(mystring):
    pattern = re.compile("^\s+|\s*,\s*|\s*:\s*|\s*{\s*|\s*}\s*|\s* \s*|\s+$")
    return [x for x in pattern.split(mystring) if x]

if __name__=='__main__':
    s = '# step : DAC: channel 2:3 to -810.0000E-3 V'
    print word_splitter(s[7:])
    s = '# step : counter: 0.0000E+0 '
    print word_splitter(s[7:])
    s = '# step2 : counter: 0.0000E+0 '
    print word_splitter(s[7:])
    s = '# step2 : fast seq: timing slot 21: 100.0000E+0 ms'
    print word_splitter(s[7:])
    s = '# step3 : fast seq: \delta_{0:0}^{26}: 144.0000E-3 V'
    print word_splitter(s[7:])
    s = '#sweep counter  from 0.000000E+0 a.u. to 601.000000E+0 a.u.'
    print word_splitter(s[7:])
    s ='#sweep offset panel 3 chanel 1 from -25.000000E-3 V to 224.999994E-3 V'
    print word_splitter(s[7:])
