import json
import  requests


def get_open_bid_list(userid,from_registration,auth_token):
    auth={'Authorization':auth_token}
    json1 = {'status': 204, 'message': 'Not Present', 'data': []}
    json2 = {'status': 202, 'message': 'Not selected', 'data': []}
    json3 = {'status': 500, 'message': 'Not selected', 'data': []}
    try:
        # url = "http://127.0.0.1:8000/bidding/open-bid-list-buyer-publish-list/"
        url="https://v2apis.vendorsin.com/bidding/open-bid-list-buyer-publish-list/"
        dataobj={'userid':userid,'from_registration':from_registration}
        # r = requests.post(url, headers=auth, data=dataobj)
        # return r.json()
        r = requests.post(url, headers=auth, json=dataobj)
        if r.status_code==200:
            openleadsvalue=r.json()
            return openleadsvalue
        if r.status_code == 204:
            return json1
        if r.status_code == 202:
            return json2
        if r.status_code==500:
            return json3
    except Exception as e:
        return  e


def get_deadline_date(userid,from_registration,auth_token):
    auth={'Authorization':auth_token}
    json1 = {'status': 204, 'message': 'Not Present', 'data': []}
    json3 = {'status': 500, 'message': 'Not selected', 'data': []}
    # url = "http://127.0.0.1:8000/bidding/deadline-date-list/"
    try:
        url="https://v2apis.vendorsin.com/bidding/deadline-date-list/"
        dataobj={'userid':userid,'from_registration':from_registration}
        r = requests.post(url, headers=auth, json=dataobj)
        print('-----------------------------',r)
        if r.status_code == 200:
            openleadsvalue = r.json()
            return openleadsvalue
        if r.status_code == 204:
            return json1
        if r.status_code == 500:
            return json3
    except Exception as e:
        return e


def get_vendor_award_list(userid,auth_token):
    json1 = {'status': 500, 'message': 'Not Present', 'data': []}
    try:
        auth={'Authorization':auth_token}
        # url = "http://127.0.0.1:8000/bidding/awards-vendor-list/"
        url="https://v2apis.vendorsin.com/bidding/awards-vendor-list/"
        dataobj={'userid':userid}
        r = requests.post(url, headers=auth, json=dataobj)
        # vendoraward=r.json()
        if r.status_code == 200:
            vendoraward = r.json()
            return vendoraward
        if r.status_code == 500:
            return json1
    except Exception as e:
        return e

def get_purchase_order_vendor_list(userid,auth_token):
    json1 = {'status': 202, 'message': 'Not Present', 'data': []}
    json2 = {'status': 500, 'message': 'Not Present', 'data': []}
    try:
        auth = {'Authorization': auth_token}
        # url = "http://127.0.0.1:8000/bidding/purchase-order-vendors-list/"
        url="https://v2apis.vendorsin.com/bidding/purchase-order-vendors-list/"
        dataobj = {'userid': userid}
        # r = requests.post(url, data=dataobj, headers=auth)
        r = requests.post(url, headers=auth, json=dataobj)
        # vendoraward=r.json()
        if r.status_code == 200:
            vendoraward = r.json()
            return vendoraward
        if r.status_code == 202:
            return json1
        if r.status_code == 500:
            return json2
    except Exception as e:
        return e

def get_source_created_items(userid,auth_token):
    json1 = {'status': 204, 'message': 'Not Present', 'data': []}
    json2 = {'status': 500, 'message': 'Not Present', 'data': []}
    try:
        auth = {'Authorization': auth_token}
        # url="http://127.0.0.1:8000/bidding/getsorcelistresponse/"
        url="https://v2apis.vendorsin.com/bidding/getsorcelistresponse/"
        dataobj = {'userid': userid}
        r = requests.post(url, headers=auth, json=dataobj)
        # vendoraward=r.json()
        if r.status_code == 200:
            vendoraward = r.json()
            return vendoraward
        if r.status_code == 204:
            return json1
        if r.status_code == 500:
            return json2
    except Exception as e:
        return e

def get_business_accept_list(userid,auth_token):
    json1 = {'status': 202, 'message': 'Not Present', 'data': []}
    json2 = {'status': 204, 'message': 'Not Present', 'data': []}
    json3 = {'status': 500, 'message': 'Not Present', 'data': []}
    try:
        auth = {'Authorization': auth_token,
                "Content-Type": "application/json"
                }
        url="https://v2apis.vendorsin.com/dashboard-page/business-request-accept-list-userid/"
        data = {'userid': userid}
        r = requests.post(url, headers=auth, json=data)
        if r.status_code == 200:
            vendoraward = r.json()
            return vendoraward
        if r.status_code == 202:
            return json1
        if r.status_code == 204:
            return json2
        if r.status_code == 500:
            return json3
    except Exception as e:
        return e

def get_business_connections(userid,auth_token):
    json1 = {'status': 202, 'message': 'Not Present', 'data': []}
    json2 = {'status': 204, 'message': 'Not Present', 'data': []}
    json3 = {'status': 500, 'message': 'Not Present', 'data': []}
    try:
        auth = {'Authorization': auth_token,
                "Content-Type": "application/json"
                }
        url = "https://v2apis.vendorsin.com/dashboard-page/buzrequest/"
        data = {'userid': userid}
        r = requests.post(url, headers=auth, json=data)
        if r.status_code == 200:
            vendoraward = r.json()
            return vendoraward
        if r.status_code == 202:
            return json1
        if r.status_code == 204:
            return json2
        if r.status_code == 500:
            return json3
    except Exception as e:
        return e

def get_business_requests_list(userid,auth_token):
    json2 = {'status': 204, 'message': 'Not Present', 'data': []}
    json3 = {'status': 500, 'message': 'Not Present', 'data': []}
    try:
        auth = {'Authorization': auth_token,
                "Content-Type": "application/json"
                }
        url="https://v2apis.vendorsin.com/dashboard-page/sendergetbuzrequestdata/"
        data = {'userid': userid}
        r = requests.post(url, headers=auth, json=data)
        if r.status_code == 200:
            vendoraward = r.json()
            return vendoraward
        if r.status_code == 204:
            return json2
        if r.status_code == 500:
            return json3
    except Exception as e:
        return e

def total_all_responses_buyer(userid,from_registration,auth_token):
    json3 = {'status': 500, 'message': 'Not Present', 'data': []}
    try:
        auth = {'Authorization': auth_token}
        url="https://v2apis.vendorsin.com/bidding/bidding-data-response-count/"
        data={'userid':userid,'from_registration':from_registration}
        r = requests.post(url, headers=auth, json=data)
        if r.status_code == 200:
            vendoraward = r.json()
            return vendoraward
        if r.status_code == 500:
            return json3
    except Exception as e:
        print('error response',e)


def get_vendor_published_list(userid,auth_token):
    auth={'Authorization':auth_token}
    json2 = {'status': 202, 'message': 'Not selected', 'data': []}
    json3 = {'status': 500, 'message': 'Not selected', 'data': []}
    try:
        url = "https://v2apis.vendorsin.com/bidding/get-vendor-published-leads/"
        # url="http://20.193.226.5/bidding/get-vendor-published-leads/"
        dataobj={'userid':userid}
        r = requests.post(url, headers=auth, json=dataobj)
        print('---------------------', r.status_code)

        if r.status_code == 200:
            vendorpublishedval = r.json()
            return vendorpublishedval
        if r.status_code == 202:
            return json2
        if r.status_code == 500:
            return json3
    except Exception as e:
        return e

def get_source_list_leads(userid,auth_token):
    try:
        json1 = {'status': 204, 'message': 'Not Present', 'data': []}
        json2 = {'status': 500, 'message': 'Not Present', 'data': []}
        auth={'Authorization':auth_token}
        url = "https://v2apis.vendorsin.com/bidding/source-list-leads/"
        # url="http://20.193.226.5/bidding/deadline-date-list/"
        dataobj={'userid':userid}
        r = requests.post(url, headers=auth,json=dataobj)
        print('---------------------',r.status_code)

        if r.status_code==200:
            vendorpublishedval = r.json()
            return vendorpublishedval
        if r.status_code==204:
            return json1
        if r.status_code==500:
            return json2
    except Exception as e:
        return e


# https://v2apis.vendorsin.com/materials/getbuyerpostedresponse/

def get_listed_list_response(userid,auth_token):
    try:
        # json1 = {'status': 204, 'message': 'Not Present', 'data': []}
        json2 = {'status': 500, 'message': 'Not Present', 'data': []}
        auth={'Authorization':auth_token}
        url = "https://v2apis.vendorsin.com/materials/getbuyerpostedresponse/"
        # url="http://20.193.226.5/bidding/deadline-date-list/"
        dataobj={'userid':userid}
        r = requests.post(url, headers=auth,json=dataobj)
        print('---------------------',r.status_code)

        if r.status_code==200:
            vendorpublishedval = r.json()
            return vendorpublishedval
        if r.status_code==500:
            return json2
    except Exception as e:
        return e