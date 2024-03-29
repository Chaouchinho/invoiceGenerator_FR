import datetime
from datetime import timedelta, date
import calendar
import locale
import os
from pyhtml2pdf import converter
from jours_feries_france import JoursFeries

askChargeJourFerie = True

locale.setlocale(locale.LC_ALL, 'fr_FR')

month_array = { "day" : [], "total_working_days":0, "tjmht": -1, "tjmttc": -1, "date_voulue":datetime.date.today(), "total_worked":0, "total_ht":-1, "total_tva":-1, "total_ttc":-1, "taux_tva":0.2}
print(month_array)

year = 0
month = 0
while((year == 0) and (month == 0)):
    print("\nSaisisez le mois et l'année de la facture [MM/YYYY]: \n   ex: 01/2024")
    val = input()
    try:
        month = int(val.split("/")[0])
        year = int(val.split("/")[1])
    except:
        month = 0
        year = 0
        print("Erreur lors de la saisie, de nouveau")


#print('Enter Taux TVA:')
#month_array["taux_tva"] = float(input())

weeks = calendar.monthcalendar(year, month)

for week in weeks:
    for i in range(len(week)):
        if( (week[i] > 0) and (i < 5) ):
            month_array["day"].append({"dayname" : calendar.day_name[i], "number" : week[i], "day_type" : -99, "cumulative_sum" : 0})
            month_array["total_working_days"] = month_array["total_working_days"] + 1



print('\nSaisisez le TJM HT en €:')
month_array["tjmht"] = float(input())
month_array["tjmttc"] = month_array["tjmht"] + month_array["tjmht"]  * month_array["taux_tva"] 


print('\nSaisie des données:\n   Jour férié :\t\t-1\n   Non travaillé:\t0\n   Demi-journée:\t0.5\n   Jour complet:\t1\n')
for i in range(len(month_array["day"])) :
    
    print('- Charge du jour : ' + month_array["day"][i]["dayname"].capitalize() +' '+ str(month_array["day"][i]["number"]) +' ' +  calendar.month_name[month].capitalize() +' ' + str(year))
    if(not JoursFeries.is_bank_holiday(datetime.date(year, month, month_array["day"][i]["number"]), zone="Métropole")):
        temp = input()
    elif(askChargeJourFerie):
        temp = input()
    else:
        print('   > Jour ferié ('+JoursFeries.next_bank_holiday(datetime.date(year, month, month_array["day"][i]["number"]), zone="Métropole")[0]+'): charge saisie automatiquement : 0\n')
        temp = -1

    try:
        if(float(temp) > 0):
            month_array["day"][i]["day_type"] = float(temp)
            month_array["day"][i]["cumulative_sum"] = month_array["total_worked"]  + float(temp)
            month_array["total_worked"] = month_array["total_worked"]  + float(temp)
        else:
            month_array["day"][i]["day_type"] = temp
            month_array["day"][i]["cumulative_sum"] = month_array["total_worked"]
    except:
        month_array["day"][i]["day_type"] = temp
        month_array["day"][i]["cumulative_sum"] = month_array["total_worked"]

month_array["total_ht"] = month_array["total_worked"] * month_array["tjmht"] 
month_array["total_tva"] = month_array["total_ht"] * month_array["taux_tva"] 
month_array["total_ttc"] = month_array["total_ht"] + month_array["total_tva"] 

print("> Generation de la facture HTML...")
line_ok = '''<tr>\n
              <td class="no centre">[[CUMULATIVELINE]]</td>
              <td class="jour">[[DAYNAME]]</td>
              <td class="journumber desc">[[DAYNUMBER]]</td>
              <td class="mission centre">HERMES SI [AC-2023-512] : Automatisation ...</td>
              <td class="client centre">Hermès</td>
              <td class="tjmht nombre">'''+locale.format_string("%.2f", month_array["tjmht"], grouping=True)+''' €</td>
              <td class="tva centre">'''+str(int(month_array["taux_tva"] *100))+'''%</td>
              <td class="totalttc nombre">'''+locale.format_string("%.2f", month_array["tjmttc"], grouping=True) +''' €</td>
            </tr>\n'''

line_partial = '''<tr>\n
              <td class="no centre">[[CUMULATIVELINE]]</td>
              <td class="jour">[[DAYNAME]]</td>
              <td class="journumber desc">[[DAYNUMBER]]</td>
              <td class="mission centre partial">[[DAYTYPE]]HERMES SI [AC-2023-512] : Automatisation ...</td>
              <td class="client centre partial">Hermès</td>
              <td class="tjmht nombre partial">[[PRIXJOURHT]]</td>
              <td class="tva centre partial">'''+str(int(month_array["taux_tva"] *100))+'''%</td>
              <td class="totalttc nombre partial">[[PRIXJOURTTC]]</td>
            </tr>\n'''

line_ferie = '''<tr>\n
              <td class="no centre">-</td>
              <td class="jour">[[DAYNAME]]</td>
              <td class="journumber desc">[[DAYNUMBER]]</td>
              <td class="jourferie centre" colspan="5" >Férié[[FERIERAISON]]</td>
            </tr>\n'''

line_off = '''<tr>\n
              <td class="no centre">-</td>
              <td class="jour">[[DAYNAME]]</td>
              <td class="journumber desc">[[DAYNUMBER]]</td>
              <td class="jouroff centre" colspan="5" >Non travaillé</td>
            </tr>\n'''
all_lines = ""
for lines in month_array["day"]:
    if(float(lines["day_type"]) > 0):
        if(float(lines["day_type"]) != 1):
            temp = line_partial
            temp = temp.replace("[[DAYTYPE]]", str(lines["day_type"]) + ' ' )
            temp = temp.replace("[[PRIXJOURHT]]", locale.format_string("%.2f", float(month_array["tjmht"]*float(lines["day_type"])), grouping=True)+ ' €' )
            temp = temp.replace("[[PRIXJOURTTC]]", locale.format_string("%.2f", float(month_array["tjmttc"]*float(lines["day_type"])), grouping=True) + ' €' )
        else:
            temp = line_ok
    elif(float(lines["day_type"]) == 0):
        temp = line_off
    else:
        temp = line_ferie
        if(JoursFeries.is_bank_holiday(datetime.date(year, month, lines["number"]), zone="Métropole")):
            temp = temp.replace("[[FERIERAISON]]", ' (' + JoursFeries.next_bank_holiday(datetime.date(year, month, lines["number"]), zone="Métropole")[0] + ')')
        else:
            temp = temp.replace("[[FERIERAISON]]", "")
    temp = temp.replace("[[CUMULATIVELINE]]", str(lines["cumulative_sum"]) )
    temp = temp.replace("[[DAYNAME]]", str(lines["dayname"]).capitalize() )
    temp = temp.replace("[[DAYNUMBER]]", str(lines["number"]) )
    all_lines = all_lines + temp



with open('html\\index.html', 'r', encoding="utf-8") as file:
    data = file.read()

data = data.replace("[[MONTHNAME]]", calendar.month_name[month].capitalize())
data = data.replace("[[YEAR]]", str(year))
data = data.replace("[[FACTUREDATE]]", month_array["date_voulue"].strftime("%d/%m/%Y"))
data = data.replace("[[DATEREGLEMENT]]", (month_array["date_voulue"] + timedelta(days=30)).strftime("%d/%m/%Y"))
data = data.replace("[[LINESCONTENT]]", all_lines)
data = data.replace("[[FACTURENB]]", str(int(year)) + str("%02d" % month) + '01')
data = data.replace("[[TOTALJOUR]]", locale.format_string("%.1f", month_array["total_worked"], grouping=True))
data = data.replace("[[TJMHT]]", locale.format_string("%.2f", month_array["tjmht"], grouping=True)+ ' €') 
data = data.replace("[[TAUXTVA]]", str(int(month_array["taux_tva"] *100))+'%')
data = data.replace("[[TJMTTC]]", locale.format_string("%.2f", month_array["tjmttc"], grouping=True)+ ' €') 
data = data.replace("[[TOTALHT]]", locale.format_string("%.2f", month_array["total_ht"], grouping=True)+ ' €') 
data = data.replace("[[TOTALTVA]]", locale.format_string("%.2f", month_array["total_tva"], grouping=True)+ ' €') 
data = data.replace("[[TOTALTTC]]", locale.format_string("%.2f", month_array["total_ttc"], grouping=True)+ ' €') 


with open('html\\generated.html', 'w+', encoding="utf-8") as file:
    file.write(data)

print("\t> OK")
print("> Export de la facture au format PDF...")

path = os.path.abspath('html\\generated.html')
converter.convert(f'file:///{path}', 'Facture ' +calendar.month_name[month].capitalize()+ ' ' +str(int(year)) + '.pdf')

print("> OK" )
print("Fichier generé :" + 'Facture ' +calendar.month_name[month].capitalize()+ ' ' +str(int(year)) + '.pdf')

input("Press Enter to continue...")
