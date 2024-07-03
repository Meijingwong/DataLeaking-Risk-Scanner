import json
from flask import Flask, render_template,request,jsonify

from geturl import scan_url,clickjack
from hostname import valid_hostname,valid_scheme
from authentication import analyze_authentication_layers,check_authorization_meta_tags,check_authentication_meta_tags,calculate_authentication_score
from sqlinjection import sql_injection_scan
from thirdParty import analyze_website
from cookies import check_for_cookies

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    url = output.get('url', '')
    error=scan_url(url)
    #avoid getting invalid url
    if(error):
        return jsonify(error=error)
    else:
        boolArr=clickjack(url)[0]
        CJScore=clickjack(url)[1]
        hostName=valid_hostname(url)[0]
        hnScore=valid_hostname(url)[1]
        scheme=valid_scheme(url)[0]
        schemeScore=valid_scheme(url)[1]
        auth_header=analyze_authentication_layers(url)
        auth_meta=check_authentication_meta_tags(url)
        aaScore=calculate_authentication_score(url)
        authorize=check_authorization_meta_tags(url)[1]
        sqlScore=sql_injection_scan(url)
        cookiesScore=check_for_cookies(url)[0]
        cookiesNum=check_for_cookies(url)[1]
        thirdPartyScore=analyze_website(url)[0]
        thirdPartyRequest=analyze_website(url)[1]
        thirdPartyCookies=analyze_website(url)[2]
        total=CJScore+hnScore+schemeScore+aaScore+sqlScore+cookiesScore+thirdPartyScore
        print(total)
        return jsonify(boolArr=boolArr,CJScore=CJScore,sqlScore=sqlScore,hnScore=hnScore,hostName=hostName,scheme=scheme,auth_header=auth_header,auth_meta=auth_meta,authorize=authorize,
                    cookiesNum=cookiesNum,thirdPartyCookies=thirdPartyCookies,thirdPartyRequest=thirdPartyRequest,total=total)

if __name__ == '__main__':
    app.run(debug=True)