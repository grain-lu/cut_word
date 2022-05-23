import jieba
import csv
import pandas as pd

def read_data(filename,colums):
    data=pd.read_excel(filename)

    new_data=pd.DataFrame(data,columns=colums)
    return new_data
    pass
def preprocess_text(sentences,stopwords):
        listA=[]

        jieba.load_userdict('key_word.txt')
        for item in sentences:

            #消除空格
            item = item.split()
            item = ''.join(item)
            try:
                segs=jieba.lcut(item)
                print(item,segs)
                segs = filter(lambda x: x not in stopwords, segs)
                segs=[word for word in segs if not word.isspace() and word]
                segs = [word for word in segs if not word.isdecimal()]
                segs = list(set(segs))
                if '儿童' in segs or '地毯'in segs:
                    segs.append('儿童地毯')
                if '儿童' in segs:
                    segs.remove('儿童')
                if '地毯' in segs:
                    segs.remove('地毯')

                segs = list(set(segs))
                listA.append(','.join(segs))

            except Exception as e:
                print(item)
        return listA

if __name__ == '__main__':
    sentences=pd.read_excel('chartlet.xlsx')
    stopwords=pd.read_csv('stop_word.txt')
    sentences['keyname_list']=preprocess_text(sentences['title'].astype(str).tolist(), stopwords['停用词'].tolist())
    print( sentences['keyname_list'])
    sentences.to_csv('data.csv',sep='\t',index=False, quoting=csv.QUOTE_NONE)












