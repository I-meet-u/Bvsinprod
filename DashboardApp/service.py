# import  requests
# def get_open_bid_list(userid,from_registration,auth_token):
#     auth={'Authorization':auth_token}
#     url="http://20.193.226.5/bidding/open-bid-list-buyer-publish-list/"
#     dataobj={'userid':userid,'from_registration':from_registration}
#     r=requests.post(url,data=dataobj,headers=auth)
#     openleadsvalue=r.json()
#     return openleadsvalue
#
#
# def get_deadline_date(userid,auth_token):
#     auth={'Authorization':auth_token}
#     url="http://20.193.226.5/bidding/deadline-date-list/"
#     dataobj={'userid':userid}
#     r=requests.post(url,data=dataobj,headers=auth)
#     deadline_date=r.json()
#     return deadline_date
#
#
# def get_vendor_award_list(userid,auth_token):
#     auth={'Authorization':auth_token}
#     url="http://20.193.226.5/bidding/awards-vendor-list/"
#     dataobj={'userid':userid}
#     r=requests.post(url,data=dataobj,headers=auth)
#     vendoraward=r.json()
#     return vendoraward
#
# def get_purchase_order_vendor_list(userid,auth_token):
#     auth = {'Authorization': auth_token}
#     url="http://20.193.226.5/bidding/purchase-order-vendors-list/"
#     dataobj = {'userid': userid}
#     r = requests.post(url, data=dataobj, headers=auth)
#     purchaseorder = r.json()
#     return purchaseorder
#
# def get_business_request_list(userid,auth_token):
#     auth = {'Authorization': auth_token}
#     url="http://20.193.226.5/dashboard-page/sendergetbuzrequestdata/"
#     dataobj = {'userid': userid}
#     r = requests.post(url, data=dataobj, headers=auth)
#     businesslist = r.json()
#     return businesslist
#
#
# def get_business_connections(userid,auth_token):
#     auth = {'Authorization': auth_token}
#     url="http://20.193.226.5/dashboard-page/buzrequest/"
#     dataobj = {'userid': userid}
#     r = requests.post(url, data=dataobj, headers=auth)
#     businesslist = r.json()
#     return businesslist

# def get_source_created_items(userid,auth_token):
#     auth = {'Authorization': auth_token}
#     url="http://20.193.226.5/bidding/bidding-router-urls/source-list-create-items/"
#     dataobj = {'userid': userid}
#     r = requests.post(url, params=dataobj, headers=auth)
#     businesslist = r.json()
#     return businesslist

import json

import  requests

def get_open_bid_list(userid,from_registration,auth_token):
    auth={'Authorization':auth_token}
    # url = "http://127.0.0.1:8000/bidding/open-bid-list-buyer-publish-list/"
    url="https://v2apis.vendorsin.com/bidding/open-bid-list-buyer-publish-list/"
    dataobj={'userid':userid,'from_registration':from_registration}
    r=requests.post(url,data=dataobj,headers=auth)
    openleadsvalue=r.json()
    return openleadsvalue


def get_deadline_date(userid,auth_token):
    auth={'Authorization':auth_token}
    # url = "http://127.0.0.1:8000/bidding/deadline-date-list/"
    url="https://v2apis.vendorsin.com/bidding/deadline-date-list/"
    dataobj={'userid':userid}
    r=requests.post(url,data=dataobj,headers=auth)
    deadline_date=r.json()
    return deadline_date


def get_vendor_award_list(userid,auth_token):
    auth={'Authorization':auth_token}
    # url = "http://127.0.0.1:8000/bidding/awards-vendor-list/"
    url="https://v2apis.vendorsin.com/bidding/awards-vendor-list/"
    dataobj={'userid':userid}
    r=requests.post(url,data=dataobj,headers=auth)
    vendoraward=r.json()
    return vendoraward

def get_purchase_order_vendor_list(userid,auth_token):
    auth = {'Authorization': auth_token}
    # url = "http://127.0.0.1:8000/bidding/purchase-order-vendors-list/"
    url="https://v2apis.vendorsin.com/bidding/purchase-order-vendors-list/"
    dataobj = {'userid': userid}
    r = requests.post(url, data=dataobj, headers=auth)
    purchaseorder = r.json()
    return purchaseorder

# def get_business_connections(userid,auth_token):
#     try:
#         auth = {'Authorization': auth_token,
#                 "Content-Type": "application/json"
#         }
#         url="http://20.193.226.5/dashboard-page/buzrequest/"
#         data = {'userid': userid}
#         r = requests.post(url,data=json.dumps(data), headers=auth).json()
#         return  r
#     except Exception as e:
#         print('error',e)

def get_source_created_items(userid,auth_token):
    auth = {'Authorization': auth_token}
    # url="http://127.0.0.1:8000/bidding/getsorcelistresponse/"
    url="https://v2apis.vendorsin.com/bidding/getsorcelistresponse/"
    dataobj = {'userid': userid}
    r = requests.post(url, data=dataobj, headers=auth)
    businesslist = r.json()
    return businesslist

# def get_business_request_list(userid,auth_token):
#     try:
#         auth = {'Authorization': auth_token,
#                 }
#         url="http://20.193.226.5/dashboard-page/sendergetbuzrequestdata/"
#         data = {'userid': userid}
#         r = requests.post(url, data=data, headers=auth)
#         return r.json()
#     except Exception as e:
#         print('error got',e)
def get_business_request_list(userid,auth_token):
    try:
        # url = "http://127.0.0.1:8000/dashboard-page/sendergetbuzrequestdata/"
        auth = {'Authorization': auth_token,
                "Content-Type": "application/json"
                }
        url="https://v2apis.vendorsin.com/dashboard-page/sendergetbuzrequestdata/"
        data = {'userid': userid}
        r = requests.post(url,headers=auth,data=json.dumps(data)).json()
        return  r
    except Exception as e:
        print('error got',e)


def total_all_responses_buyer(userid,from_registration,auth_token):
    try:
        auth = {'Authorization': auth_token}
        url="https://v2apis.vendorsin.com/bidding/bidding-data-response-count/"
        data={'userid':userid,'from_registration':from_registration}
        r = requests.post(url,data=data,headers=auth)
        totacount=r.json()
        return  totacount


    except Exception as e:
        print('error response',e)



def awarded(userid, auth_token):
    try:
        auth = {'Authorization': auth_token,
                "Content-Type": "application/json"
                }
        url = "https://v2apis.vendorsin.com/bidding/get-all-types-of-awards/"
        data = {'userid': userid}
        r = requests.post(url, headers=auth, json=json.dumps(data)).json()
        awarded = r
        return awarded
    except Exception as e:
        print('error-------------------------------------', e)
