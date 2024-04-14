from flask import Flask, render_template, request, redirect, url_for, abort
import re

app = Flask(__name__)

def sendToFrontEnd(request):
    datalen = int(request.headers.get('Content-Length'))
    data =  request.stream.read()
    data = data[:datalen] 
    return sendToBackEnd(request, data)

def sendToBackEnd(request, data):
    chunking = request.headers.get('Transfer-Encoding')

    if chunking == 'chunked':
        data = data.strip().decode('utf-8').split("\n")
        lastChunkIndex = 0
        i = 0
        while(i <= len(data)-1):
            data[i] = data[i]
            if (re.findall(r'^\d+$', data[i])):
                if int(data[i]) == 0:
                    lastChunkIndex = i+1
                    break
                i+=int(data[i])
                lastchunkindex = i
            i += 1
        
        remainingData = ('\n'.join(data[lastChunkIndex:]))
        if len(remainingData) > 0:
            if re.findall(r'^GET \/customsinspection HTTP\/1\.1', remainingData):
                if re.findall(r'\[\s*.*?"\s*Ice\s+Blocks\s*".*?\s*\]', remainingData):
                    return render_template('customsinspection.html')
        return "Thank you. Safe and/or approved cargo detected. Manual approval unnecessary. Inspection query will be processed shortly.", 200
    else:      
        return render_template('errorhint.html')

@app.route('/item1btabdata')
def item1():
    return render_template('/items/item1.html')
    
@app.route('/item2btabdata')
def item2():
    return render_template('/items/item2.html')

@app.route('/item3btabdata')
def item3():
    return render_template('/items/item3.html')

@app.route('/item4btabdata')
def item4():
    return render_template('/items/item4.html')

@app.route('/item5btabdata')
def item5():
    return render_template('/items/item5.html')

@app.route('/item6btabdata')
def item6():
    return render_template('/items/item6.html')

@app.route('/item7btabdata')
def item7():
    return render_template('/items/item7.html')

@app.route('/item8btabdata')
def item8():
    return render_template('/items/item8.html')

@app.route('/item9btabdata')
def item9():
    return render_template('/items/item9.html')

@app.route('/abouttabdata')
def about():
    return render_template('abouttabdata.html')

@app.route('/lawsregstabdata')
def lawsregstabdata():
    return render_template('lawsregstabdata.html')

@app.route('/inspectiontabdata')
def inspection():
    return render_template('inspectiontabdata.html')

@app.route('/inventorytabdata')
def inventorytabdata():
    return render_template('inventorytabdata.html')

@app.route('/securityquerytabdata')
def securityquery():
    return render_template('securityquerytabdata.html')

@app.route('/customsinspection', methods=['POST', 'GET'])
def customs():
    if request.method == 'POST':
        print(request)
        return sendToFrontEnd(request)
    elif request.method == 'GET':
        abort(405)

@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('menu', isadmin='false'))

@app.route('/menu', methods=['GET'])
def menu():
    query = request.args.get('isadmin')
    if query == None:
        query = 'false'    
    if query == 'true':
        return render_template('bruh.html')
    else:
        return render_template('manager.html')

if __name__ == '__main__':
    app.run(debug=True)



