def txtwindow(str):

 o = open(r"./info/orange.txt","r",encoding='utf-8')
 ora = o.read()
 o.close()

 m = open("./info/mango.txt","r",encoding='utf-8')
 man = m.read()
 m.close()

 a = open("./info/apple.txt","r",encoding='utf-8')
 app = a.read()
 a.close()

 b = open("./info/banana.txt","r",encoding='utf-8')
 ban = b.read()
 b.close()

 p = open("./info/pineapple.txt","r",encoding='utf-8')
 pin = p.read()
 p.close()

 fruit_dic = {'apple':app,'orange':ora,'mango':man,'banana':ban,'pineapple':pin}
 dic1 = fruit_dic

 if (str == 'Apple'):
  return (dic1['apple'])
 elif(str == 'Orange'):
  return (dic1['orange'])
 elif (str == 'Pineapple'):
  return (dic1['pineapple'])
 elif (str == 'Banana'):
  return (dic1['banana'])
 else:
  return (dic1['mango'])


if __name__ == '__main__':
 str = 'Apple'
 s = txtwindow(str)
 # print(s)

