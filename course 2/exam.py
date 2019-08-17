import urllib.request,re, codecs, os


for root, dirs, files in os.walk (r'C:\Users\student\Desktop\thai_pages', topdown = False):
    for file in files[1:2]:
        dict = {}
        try:
           with codecs.open(os.path.join(root,file), 'r', 'utf-8') as f:
               text = f.read()
               for line in f.readlines():
                   try:
                      Tword = re.search(r'<a href=\'/id/[0-9]*\'>(.*)?</a>', line, flags = re.DOTALL).group(0)
                      Eword = re.search(r'<td>[a-zA-Z; ]*</td></tr>', line, flags = re.DOTALL).group(0)
                      print(word)
                    except:
                        continue
            except:
                print('no')
