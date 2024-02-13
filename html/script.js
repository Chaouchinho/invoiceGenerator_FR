function onLoadFunctions() {

    document.title = 'Facture ' + companyName
    document.getElementById("headercompanyName").innerText=companyName
    document.getElementById("headercompanyAddress").innerText=companyAddress
    document.getElementById("headercompanyZipCodeAndCity").innerText=companyZipCodeAndCity
    document.getElementById("headercompanyPhone").innerText=companyPhone
    document.getElementById("headercompanyHREF").innerText=companyWebsiteName
    document.getElementById("headercompanyHREF").href=companyWebsiteURL

    document.getElementById("clientExpedieName").innerText=clientName
    document.getElementById("clientExpedieAddress").innerText=clientAdress
    document.getElementById("clientExpedieZipCodeAndCity").innerText=clientZipCodeAndCity
    document.getElementById("clientExpediePhoneNumber").innerText=clientPhoneNumber

    document.getElementById("clientFacturationName").innerText=clientName
    document.getElementById("clientFacturationAddress").innerText=clientAdress
    document.getElementById("clientFacturationZipCodeAndCity").innerText=clientZipCodeAndCity
    document.getElementById("clientFacturationPhoneNumber").innerText=clientPhoneNumber

    document.getElementById("footercompanyName").innerText=companyName
    document.getElementById("footercompanySiren").innerText=companySiren
    document.getElementById("footercompanyCapital").innerText=companyCapital
    document.getElementById("footercompanySirenDeux").innerText=companySiren
    document.getElementById("footercompanyTVAIntracom").innerText=companyTVAIntracom
    document.getElementById("footercompanyAddress").innerText=companyAddress
    document.getElementById("footercompanyZipCodeAndCity").innerText=companyZipCodeAndCity
    document.getElementById("footercompanyHREF").innerText=companyWebsiteName
    document.getElementById("footercompanyHREF").href=companyWebsiteURL
    document.getElementById("footercompanyPhone").innerText=companyPhone
    document.getElementById("footercompanyEmail").innerText=companyEmail

}