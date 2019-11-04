import re



str_l = '标普500医疗保健等权重指数收益率(使用估值汇率折算)*95%+活期存款利率(税后)*5%+标普500医疗保健等权重指数收益率(使用估值汇率折算)*95%+活期存款利率(税后)*5%'

matchObj = re.match(r'(.*?)([0-9]+)%\+(.*?)([0-9]+)%', str_l, re.M | re.I)

print(matchObj.group(1))
print(matchObj.group(2))
print(matchObj.group(3))
print(matchObj.group(4))
print(matchObj.lastindex)




r1 = re.findall(r'(.*?)([0-9]+)%',str_l)


print(r1)