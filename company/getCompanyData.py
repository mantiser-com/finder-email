from urllib.parse import urlparse
import dns.resolver
import re



def getCompanyData(url):
    '''
    Check if the domain is valid
    '''
    theurl=urlparse(url)
    domainResult={
        "domain": theurl.netloc,
    }
    domain = str(theurl.netloc).replace("www.","")
    print("Checking domain" + domain)

    #Check NS records
    try:
        nameservers = dns.resolver.resolve(domain,'NS')
        domainsNameservers = []
        for data in nameservers:
            domainsNameservers.append(str(data))
        domainResult['nameservers']=domainsNameservers

        for nameserver in  domainsNameservers:
            if re.search(r"googledomains", nameserver):
                domainResult['googleDomain']=True
    except:
        pass
    #Check SOA records
    try:
        soaservers = dns.resolver.resolve(domain,'SOA')
        domainsSoaservers = []
        for data in soaservers:
            domainsSoaservers.append(str(data))
        domainResult['soaservers']=domainsSoaservers
    except:
        pass

    #Check A records
    try:    
        servers = dns.resolver.resolve(domain,'A')
        domainsservers = []
        for data in servers:
            domainsservers.append(str(data))
        domainResult['servers']=domainsservers
    except:
        pass
    #Check MX records
    try:
        mailservers = dns.resolver.resolve(domain,'MX')
        domainsMailservers = []
        for data in mailservers:
            domainsMailservers.append(str(data))
        domainResult['mailservers']=domainsMailservers
        for mailserver in  domainsMailservers:
            if re.search(r"google", mailserver):
                domainResult['googleEmail']=True
            if re.search(r"outlook", mailserver):
                domainResult['outlookEmail']=True
    except:
        pass


    #Check for diffrent service spicifydn record
    # Stripe
    try:
        stripeservers = dns.resolver.resolve("_acme-challenge.checkout."+domain,'txt')
        if stripeservers:
            domainResult['stripe']=True
            domainsStripeservers = []
            for data in stripeservers:
                domainsStripeservers.append(str(data))
            domainResult['stripesever']=domainsStripeservers
    except:
        pass
    # Paypal
    try:
        paypalservers = dns.resolver.resolve("_paypal-challenge."+domain,'txt')
        if paypalservers:
            domainResult['paypal']=True
            domainspaypalservers = []
            for data in paypalservers:
                domainspaypalservers.append(str(data))
            domainResult['paypalsever']=domainspaypalservers
    except: 
        pass
    # mailchimp
    try:
        mailchimpservers = dns.resolver.resolve("k2._domainkey."+domain,'txt')
        if mailchimpservers:
            domainResult['mailchimp']=True
            domainsmailchimpservers = []
            for data in mailchimpservers:
                domainsmailchimpservers.append(str(data))
            domainResult['mailchimpservers']=domainsmailchimpservers
    except: 
        pass


    return domainResult
