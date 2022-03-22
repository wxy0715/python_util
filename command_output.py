import sys
import os

record_id = 0
commandFile = "command.txt"
outputFile = "output"

linuxPrompt = ''
output = []


def getAllRecord():
    try:
        with open(commandFile,"r",encoding="utf-8") as f1:
            lines = f1.readlines()  # 读取全部内容 ，并以列表方式返回
            print(lines)
            i = 0
            for line in lines:
                infoList = line.split()
                _time = int(infoList[0])
                if len(infoList) > 1:
                    keyWord = infoList[1]
                else:
                    keyWord = ''
                content = output[i]
                i += 1
                print(i, keyWord, content['cmd'])
                if(len(keyWord)>0):
                    print(record_id, _time, keyWord, content['output'])
    except Exception as err:
        print(err)


if __name__ == '__main__':
    try:
        # 接收传入的参数
        os.system('cat '+ outputFile + '| /opt/lsblj/server/bin/ansi2txt | col -b > '+outputFile+'.ascii')
        info = open(outputFile+'.ascii', 'r')                                                 # 读取文件内容
        txt = info.read() 
        pos2 = 0
        pos3 = 1000
        i=0
        command_line = 0
        while True:
            command_line = 0
            if protocol_id == 3:
                pos1 = txt.find('<',pos2)
                pos2 = txt.find('>',pos1)
                if pos2 > pos1:
                    command_line = 1
            else:
                pos1 = txt.find('[',pos2)
                pos2 = txt.find(']',pos1)
                if txt[pos1:pos2+1].find('@')>=0:
                    command_line = 1
            if command_line == 1:
                if pos3<pos1:
                    _output = txt[pos3+1:pos1]
                    output.append({'cmd':cmd.strip(), 'output':_output})
                pos3 = txt.find('\n',pos2)
                i=i+1
                cmd = txt[pos2+1:pos3]
                print('cmd:'+str(i)+" "+cmd)
            if pos2 < 0:
                break
        if pos3 > pos1:
            _output = txt[pos3+1:]
            output.append({'cmd':cmd, 'output':_output})
        print(output)
        getAllRecord()
    except Exception as err:
        print(err)
    