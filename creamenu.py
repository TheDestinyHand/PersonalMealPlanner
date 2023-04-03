import hashlib
import json
import os
import random
import re
from typing import Any

FABBISOGNO_CALORIE = 1200
FABBISOGNO_PROTEINE = 30
FABBISOGNO_GRASSI = 40
FABBISOGNO_CARBOIDRATI = 120
FABBISOGNO_FIBRE = 17
global username
global nome_menu
global cas


# funzione per il login
def login():
    global username
    # controllo se il file JSON esiste
    if os.path.exists('account.json'):
        # apro il file JSON per leggere le informazioni dell'account
        with open('account.json', 'r') as f:
            account = json.load(f)
    else:
        # se il file JSON non esiste, crea un nuovo dizionario vuoto
        account = {}
    # chiedo all'utente di inserire il nome utente e la password
    # lista di caratteri non validi nell'username
    invalid_chars = ['/', '\\', '?', '%', '*', ':', '|', '"', '<', '>', '.']
    while True:
        username = input("Inserisci il nome utente: ")
        password = input("Inserisci la password: ")
        if any(char in invalid_chars for char in username) or any(char in invalid_chars for char in password):
            print(
                "Il nome utente e la password non possono contenere i seguenti caratteri: " + ", ".join(invalid_chars))
        else:
            break
    # controllo se l'utente esiste nel file JSON
    if username in account:
        # confronto l'hash della password inserita con quello memorizzato nel file JSON
        if hashlib.sha256(password.encode('utf-8')).hexdigest() == account[username]['password']:
            print("Accesso riuscito!")
            return False
        else:
            print("Password errata.")
            return True
            
    else:
        # chiedo all'utente le informazioni aggiuntive per la registrazione
        carne_pref = int(input("Quanto ti piace la carne? (da 1 a 5) "))
        while carne_pref < 1 or carne_pref > 5:
            carne_pref = int(input("Inserisci un numero tra 1 e 5: "))

        pesce_pref = int(input("Quanto ti piace il pesce? (da 1 a 5) "))
        while pesce_pref < 1 or pesce_pref > 5:
            pesce_pref = int(input("Inserisci un numero tra 1 e 5: "))

        glutine_int = input("Sei intollerante al glutine? (s/n) ")
        while glutine_int.lower() != "s" and glutine_int.lower() != "n":
            glutine_int = input("Rispondi 's' o 'n': ")

        lattosio_int = input("Sei intollerante al lattosio? (s/n) ")
        while lattosio_int.lower() != "s" and lattosio_int.lower() != "n":
            lattosio_int = input("Rispondi 's' o 'n': ")

        # creo un nuovo account e salvo le informazioni nel file JSON
        account[username] = {
            "password": hashlib.sha256(password.encode('utf-8')).hexdigest(),
            "carne_pref": carne_pref,
            "pesce_pref": pesce_pref,
            "glutine_int": glutine_int.lower() == "s",
            "lattosio_int": lattosio_int.lower() == "s"
        }
        with open('account.json', 'w') as f:
            json.dump(account, f)
        if not os.path.exists(username):
            os.makedirs(username)
        return False


def listaPietanzeAmmesse(file):
    with open('account.json', 'r') as f:
        account = json.load(f)
    with open('pietanze/' + file + '.json', 'r') as f:
        piatto = json.load(f)
    n_piatto: int = len(piatto['piatti'])
    lat = account[username]['lattosio_int']
    glut = account[username]['glutine_int']
    piatti_acc: list[Any] = []
    for i in range(n_piatto):
        if piatto['piatti'][i]['latticini'] != 's' and lat != True:
            if piatto['piatti'][i]['glutine'] != 's' and glut != True:
                piatti_acc.append(piatto['piatti'][i]['nome'])
    return (piatti_acc)


def generate_weekly_menu():
    done = True
    print("Inserisci il nome del menù:")
    nome_menu = input()
    # carico le preferenze dell'utente dal file account.json
    with open('account.json', 'r') as f:
        account = json.load(f)

    # carico i menu di pasta, carne e pesce dal file json corrispondente
    with open('pietanze/sughi.json', 'r') as f:
        sughi = json.load(f)

    with open('pietanze/carne.json', 'r') as f:
        carne = json.load(f)

    with open('pietanze/contorno.json', 'r') as f:
        contorno = json.load(f)

    with open('pietanze/colazione.json', 'r') as f:
        colazione = json.load(f)

    with open('pietanze/pesce.json', 'r') as f:
        pesce = json.load(f)

    with open('pietanze/merenda.json', 'r') as f:
        merenda = json.load(f)
    # creo una lista vuota per il menu settimanale
    menu_settimanale = []
    # mi prendo le intolleranze dell'utente
    lat = account[username]['lattosio_int']
    glut = account[username]['glutine_int']
    # inizializzo le liste per i piatti esclusi
    sughi_acc = []
    carne_acc = []
    pesce_acc = []
    contorno_acc = []
    colazione_acc = []
    merenda_acc = []
    # assegno casualmente una pietanza di pasta, carne o pesce in base alle preferenze dell'utente
    punteggio_carne = account[username]['carne_pref']
    punteggio_pesce = account[username]['pesce_pref']

    # Calcolo la somma dei punteggi delle preferenze
    somma_punteggi = punteggio_carne + punteggio_pesce

    # Calcolo le probabilità relative di scegliere una pietanza di pasta, carne o pesce
    probabilita_carne = punteggio_carne / somma_punteggi
    probabilita_pesce = punteggio_pesce / somma_punteggi
    n_sughi = len(sughi['piatti'])
    n_carne = len(carne['piatti'])
    n_pesce: int = len(pesce['piatti'])
    n_contorno = len(contorno['piatti'])
    n_colazione = len(colazione['piatti'])
    n_merenda = len(merenda['piatti'])
    # creo le liste di pietanze ammesse in base alle intolleranze dell'utente
    colazione_acc = listaPietanzeAmmesse("colazione")
    sughi_acc = listaPietanzeAmmesse("sughi")
    merenda_acc = listaPietanzeAmmesse("merenda")
    carne_acc = listaPietanzeAmmesse("carne")
    pesce_acc = listaPietanzeAmmesse("pesce")
    contorno_acc = listaPietanzeAmmesse("contorno")

    pietanze_escluse = []

    # ciclo sui giorni della settimana
    for giorno in range(0, 7):
        done = True
        calorie = 0
        carboidrati = 0
        grassi = 0
        fibre = 0
        proteine = 0
        while done:
            # creo un dizionario vuoto per il menu del giorno corrente
            menu_giornaliero = []
            contorno_cena = ""
            pietanza_pranzo = ""
            pietanza_cena = ""
            merenda_giornaliera = ""
            colazione_giornaliera = ""
            valori = []
            
            ###COLAZIONE###
            colazione_giornaliera = seleziona_pietanza(colazione, n_colazione, [])
            valori = getinfonutrizione(calorie, proteine, grassi, carboidrati, fibre, colazione_giornaliera,"colazione.json")
            ###PRANZO###
            pietanza_pranzo = seleziona_pietanza(sughi, n_sughi, pietanze_escluse)
            valori = getinfonutrizione(valori["calorie"], valori["proteine"], valori["grassi"], valori["carboidrati"],
                                       valori["fibra"], pietanza_pranzo, "sughi.json")
            ###MERENDA###
            merenda_giornaliera = seleziona_pietanza(merenda, n_merenda, [])
            valori = getinfonutrizione(valori["calorie"], valori["proteine"], valori["grassi"], valori["carboidrati"],
                                       valori["fibra"], merenda_giornaliera, "merenda.json")
            ###CENA####
            #scelgo casualmente una categoria di pietanza in base alle probabilità relative delle preferenze
            categoria_scelta = random.choices(['carne', 'pesce'], weights=[probabilita_carne, probabilita_pesce])[0]
            # scelgo casualmente una pietanza della categoria scelta, meno quelle escluse
            if categoria_scelta == 'carne':
                pietanza_cena = seleziona_pietanza(carne, n_carne, pietanze_escluse)
                valori = getinfonutrizione(valori["calorie"], valori["proteine"], valori["grassi"],
                                           valori["carboidrati"], valori["fibra"], pietanza_cena, "carne.json")

            elif categoria_scelta == 'pesce':
                pietanza_cena = seleziona_pietanza(pesce, n_pesce, pietanze_escluse)
                valori = getinfonutrizione(valori["calorie"], valori["proteine"], valori["grassi"],
                                           valori["carboidrati"], valori["fibra"], pietanza_cena, "pesce.json")

            contorno_cena = seleziona_pietanza(contorno, n_contorno, [])
            valori = getinfonutrizione(valori["calorie"], valori["proteine"], valori["grassi"], valori["carboidrati"],
                                       valori["fibra"], contorno_cena, "contorno.json")
            if FABBISOGNO_CALORIE <= valori["calorie"] and FABBISOGNO_CARBOIDRATI <= valori[
                "carboidrati"] and FABBISOGNO_FIBRE <= valori["fibra"] and FABBISOGNO_GRASSI <= valori[
                "grassi"] and FABBISOGNO_PROTEINE <= valori["proteine"]:
                pietanze_escluse.append(pietanza_pranzo)
                pietanze_escluse.append(pietanza_cena)
                menu_giornaliero.append(
                    {'giorno': giorno, 'colazione': colazione_giornaliera, 'pranzo': pietanza_pranzo,
                     'merenda': merenda_giornaliera, 'cena': pietanza_cena, 'contorno_cena': contorno_cena})
                menu_settimanale.append(menu_giornaliero)
                done = False
    salva_menu(menu_settimanale, filename=username + "/" + nome_menu + ".json")

    # visualizzazione menù
    while True:
        print("\nCome vuoi visualizzare il nuovo menù?")
        print("1. Mostramelo a video")
        print("2. Non voglio vederlo")
        choice: str = input("\nCosa vuoi fare? ")
        if choice == "1":
            apri_menu(username + "/" + nome_menu + ".json")
            break
        elif choice == "2":
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida. Riprova.")
    # visualizzazione lista della spesa
    while True:
        print("\nVuoi vedere la lista della spesa?")
        print("1. Mostramela a video")
        print("2. Non voglio vederla")
        choice = input("\nCosa vuoi fare? ")

        if choice == "1":
            crea_lista_della_spesa(username + "/" + nome_menu + ".json")
            break
        elif choice == "2":
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida. Riprova.")


# funzione per la ricerca degli ingredienti dal nome del piatto
def ricerca_per_piatto(nome_piatto):
    files = ["pietanze/carne.json", "pietanze/pesce.json", "pietanze/sughi.json", "pietanze/contorno.json",
             "pietanze/merenda.json", "pietanze/colazione.json"]
    ingredienti = []
    for file in files:
        with open(file, "r") as f:
            data = json.load(f)
            n = len(data['piatti'])
            for i in range(0, n):
                piatto = data['piatti'][i]['nome']
                if piatto.lower() == nome_piatto.lower():
                    ingredienti.append(data['piatti'][i]['ingredienti'])
    if ingredienti:
        return ingredienti
    else:
        return "Nessun piatto trovato"


# funzione per la ricerca dei piatti che contengono un dato ingrediente
def ricerca_per_ingrediente(ingrediente):
    files = ["pietanze/carne.json", "pietanze/pesce.json", "pietanze/sughi.json", "pietanze/contorno.json",
             "pietanze/merenda.json", "pietanze/colazione.json"]
    lista_piatti = []
    for file in files:
        with open(file, "r") as f:
            data = json.load(f)
            n = len(data['piatti'])
            for i in range(0, n):
                ingredienti = data['piatti'][i]['ingredienti']
                for ing in ingredienti:
                    if ingrediente.lower() in ing.lower():
                        lista_piatti.append(data['piatti'][i]['nome'])
                        break  # esce dal ciclo appena viene trovato un ingrediente che soddisfa la ricerca
    if lista_piatti:
        return lista_piatti
    else:
        return "Nessun piatto trovato con questo ingrediente."


# funzioni che visualizzano le pietanze
def visualizza_sughi():
    with open("pietanze/sughi.json", "r") as f:
        sughi = json.load(f)
    n = len(sughi['piatti'])
    print("I piatti di pasta disponibili sono: ")
    for i in range(0, n):
        print("- " + sughi['piatti'][i]["nome"])


def visualizza_carni():
    with open("pietanze/carne.json", "r") as f:
        carni = json.load(f)
    n = len(carni['piatti'])
    print("I piatti di carne disponibili sono: ")
    for i in range(0, n):
        print("- " + carni['piatti'][i]["nome"])


def visualizza_merenda():
    with open("pietanze/merenda.json", "r") as f:
        merenda = json.load(f)
    n = len(merenda['piatti'])
    print("Le merende disponibili sono: ")
    for i in range(0, n):
        print("- " + merenda['piatti'][i]["nome"])


def visualizza_contorni():
    with open("pietanze/contorno.json", "r") as f:
        contorni = json.load(f)
    n = len(contorni['piatti'])
    print("I contorni disponibili sono: ")
    for i in range(0, n):
        print("- " + contorni['piatti'][i]["nome"])


def visualizza_colazione():
    with open("pietanze/colazione.json", "r") as f:
        colazione = json.load(f)
    n = len(colazione['piatti'])
    print("Le colazioni disponibili sono: ")
    for i in range(0, n):
        print("- " + colazione['piatti'][i]["nome"])


def visualizza_pesci():
    with open("pietanze/pesce.json", "r") as f:
        pesce = json.load(f)
    n = len(pesce['piatti'])
    print("I piatti di pesce disponibili sono: ")
    for i in range(0, n):
        print("- " + pesce['piatti'][i]["nome"])


# funzione che salva un menù in un file json
def salva_menu(menu, filename):
    with open(filename, "w") as f:
        json.dump(menu, f)


# funzione che riporta i menù presenti nella cartella dell'utente
def visualizza_vecchi_menu():
    global username
    folder_path = username + "/"
    files = os.listdir(folder_path)
    if "preferenze.json" in files:
        # Rimuovi il file "preferenze.json"
        files.remove("preferenze.json")
    else:
        pass
    print("I menu disponibili sono: ")
    for i, file in enumerate(files):
        print(i + 1, "-", file)
    while True:
        try:
            file_number = int(input("Quale file vuoi aprire? "))
            if file_number < 1 or file_number > len(files):
                raise ValueError
            break
        except ValueError:
            print("Input non valido. Inserisci un numero corretto.")
    file_name = files[file_number - 1]
    file_path = os.path.join(folder_path, file_name)
    return file_path


# funzione che apre un menù e lo stampa in un formato visivamente carino
def apri_menu(file_path):
    with open(file_path, "r") as f:
        menu = json.load(f)
    for i in range(0, 7):
        if i == 0:
            giorno = "Lunedì"
        elif i == 1:
            giorno = "Martedì"
        elif i == 2:
            giorno = "Mercoledì"
        elif i == 3:
            giorno = "Giovedì"
        elif i == 4:
            giorno = "Venerdì"
        elif i == 5:
            giorno = "Sabato"
        elif i == 6:
            giorno = "Domenica"
        print("######################" + giorno + "######################")
        print("colazione: " + menu[i][0]['colazione'])
        print("pranzo: " + menu[i][0]['pranzo'])
        print("merenda: " + menu[i][0]['merenda'])
        print("cena: " + menu[i][0]['cena'] + " con " + menu[i][0]['contorno_cena'])


# funzione che seleziona i piatti del menù
def seleziona_pietanza(piatti, n_pietanze, pietanze_escluse):
    global cas
    voti_file = username + "/preferenze.json"
    try:
        with open(voti_file, 'r') as f:
            voti = json.load(f)
    except FileNotFoundError:
        voti = {}
    done = False

    while not done:
        cas = random.randint(0, n_pietanze - 1)
        pietanza_pranzo = piatti['piatti'][cas]['nome']
        if pietanza_pranzo not in pietanze_escluse:
            if pietanza_pranzo in voti:
                voto = voti[pietanza_pranzo]
            else:
                voto = 3
            # Calcolo la probabilità per il piatto
            probabilita = voto / 5
            # Genero un numero random tra 0 e 1 ed se è minore del voto del piatto selezioni il piatto
            if random.random() < probabilita:
                done = True
    return pietanza_pranzo


# funzione che stampa la lista della spesa per un menù selezionato dall'utente
def crea_lista_della_spesa(nome_menu):
    if nome_menu == None:
        nome_menu = visualizza_vecchi_menu()
    with open(nome_menu, "r") as f:
        menu = json.load(f)
        # Creo la lista della spesa che conterrà gli ingredienti e le loro quantità
    lista_della_spesa = []
    for i in range(0, 7):
        colazione = menu[i][0]["colazione"]
        merenda = menu[i][0]["merenda"]
        contorno = menu[i][0]["contorno_cena"]
        pranzo = menu[i][0]["pranzo"]
        cena = menu[i][0]["cena"]

        lista_spesa_colazione = {}
        lista_spesa_pranzo = {}
        lista_spesa_merenda = {}
        lista_spesa_cena = {}
        lista_spesa_contorno = {}
        # Trovo gli ingredienti per i piatti della colazione
        lista_spesa_colazione = creaLista("colazione", colazione)
        if i == 0:
            lista_della_spesa = lista_spesa_colazione
        else:
            lista_della_spesa = mergeListe(lista_della_spesa, lista_spesa_colazione)
            # Trovo gli ingredienti per i piatti della merenda
        lista_spesa_merenda = creaLista("merenda", merenda)
        lista_della_spesa = mergeListe(lista_della_spesa, lista_spesa_merenda)
        # Trovo gli ingredienti per i piatti della cena
        lista_spesa_cena = creaLista(trova_tipo_piatto(cena), cena)
        lista_della_spesa = mergeListe(lista_della_spesa, lista_spesa_cena)
        # Trovo gli ingredienti per il contorno
        lista_spesa_contorno = creaLista("contorno", contorno)
        lista_della_spesa = mergeListe(lista_della_spesa, lista_spesa_contorno)
        # Trovo gli ingredienti per il pranzo
        lista_spesa_pranzo = creaLista("sughi", pranzo)
        lista_della_spesa = mergeListe(lista_della_spesa, lista_spesa_pranzo)
    stampaListaDellaSpesa(lista_della_spesa)


def mergeListe(list1, list2):
    result = {}
    for k1, v1 in list1.items():
        for k2, v2 in list2.items():
            if v1[0] == v2[0]:
                quantity1 = float(v1[1])
                quantity2 = float(v2[1])
                quantity_sum = quantity1 + quantity2
                unit = v1[2] if v1[2] else v2[2]
                result[v1[0]] = (v1[0], str(quantity_sum), unit)

    for k2, v2 in list2.items():
        if v2[0] not in result.keys():
            result[v2[0]] = v2
    for k1, v1 in list1.items():
        if v1[0] not in result.keys():
            result[v1[0]] = v1
    return result


def stampaListaDellaSpesa(lista):
    for ingrediente in lista:
        if lista[ingrediente][2] == 'cucchiaio' and float(lista[ingrediente][1]) > 1:
            print("ingrediente: " + lista[ingrediente][0] + ", quantita: " + str(lista[ingrediente][1]) + " cucchiai")
        elif lista[ingrediente][2] == 'spicchio' and float(lista[ingrediente][1]) > 1:
            print("ingrediente: " + lista[ingrediente][0] + ", quantita: " + str(lista[ingrediente][1]) + " spicchi")
        elif lista[ingrediente][2] == 'cucchiaino' and float(lista[ingrediente][1]) > 1:
            print("ingrediente: " + lista[ingrediente][0] + ", quantita: " + str(lista[ingrediente][1]) + " cucchiaino")
        elif lista[ingrediente][2] == 'bustina' and float(lista[ingrediente][1]) > 1:
            print("ingrediente: " + lista[ingrediente][0] + ", quantita: " + str(lista[ingrediente][1]) + " bustina")
        elif lista[ingrediente][2] == 'rametto' and float(lista[ingrediente][1]) > 1:
            print("ingrediente: " + lista[ingrediente][0] + ", quantita: " + str(lista[ingrediente][1]) + " rametti")
        elif lista[ingrediente][2] == 'gambo' and float(lista[ingrediente][1]) > 1:
            print("ingrediente: " + lista[ingrediente][0] + ", quantita: " + str(lista[ingrediente][1]) + " gambi")
        else:
            print("ingrediente: " + lista[ingrediente][0] + ", quantita: " + str(lista[ingrediente][1]) + " " +
                  lista[ingrediente][2])


def trova_tipo_piatto(piatto):
    with open('pietanze/carne.json') as f:
        carne = json.load(f)
    with open('pietanze/pesce.json') as f:
        pesce = json.load(f)
    for i in range(0, len(carne['piatti'])):
        if piatto in carne['piatti'][i]['nome']:
            return 'carne'
    for i in range(0, len(pesce['piatti'])):
        if piatto in pesce['piatti'][i]['nome']:
            return 'pesce'


def creaLista(categoria, piatto):
    lista_spesa = {}
    with open("pietanze/" + categoria + ".json", "r") as f:
        data = json.load(f)
    n_pietanze = len(data['piatti'])
    l = 0
    for i in range(0, n_pietanze):
        numero = 0
        unita_di_misura = ""
        if data['piatti'][i]['nome'] == piatto:
            ingredienti = data['piatti'][i]['ingredienti']
            for ingrediente in ingredienti:
                ingre = data['piatti'][i]['ingredienti'][ingrediente]
                ingrediente_split = ingre.split()
                if len(ingrediente_split) is not None:
                    if len(ingrediente_split) == 1:
                        if re.match("^[0-9]+$", ingre):
                            numero = ingre
                            unita_di_misura = ""
                        elif ingre == "qb":
                            numero = 1
                            unita_di_misura = "qb"
                        elif ingre == "0.25":
                            numero = 0.25
                        elif ingre == "0.5":
                            numero = 0.5
                        else:
                            match = re.match(r"(\d+)(\D+)", ingre)
                            numero = match.group(1)
                            unita_di_misura = match.group(2)
                    elif len(ingrediente_split) > 1:
                        numero = ingrediente_split[0]
                        unita_di_misura = ingrediente_split[1]
                    lista_spesa[l] = (ingrediente, numero, unita_di_misura)
                    l = l + 1
    return lista_spesa


# funzione che permette il voto di una pietanza all'utente
def vota_pietanza():
    global username
    voti_file = username + '\preferenze.json'
    voti = {}

    # Carica i voti già esistenti, se il file esiste
    if os.path.isfile(voti_file):
        with open(voti_file, "r") as f:
            voti = json.load(f)

    # Mostra all'utente la lista delle pietanze tra cui scegliere
    files = ["pietanze/carne.json", "pietanze/pesce.json", "pietanze/sughi.json", "pietanze/contorno.json",
             "pietanze/merenda.json", "pietanze/colazione.json"]
    piatti = []
    for file in files:
        with open(file, "r") as f:
            data = json.load(f)
            piatti.extend(data["piatti"])

    for i, piatto in enumerate(piatti):
        print(f"{i + 1}. {piatto['nome']}")

    # Chiedi all'utente di selezionare una pietanza
    while True:
        scelta = input("Seleziona il numero della pietanza che vuoi votare: ")
        try:
            scelta = int(scelta)
            if scelta < 1 or scelta > len(piatti):
                raise ValueError()
            break
        except ValueError:
            print("Input non valido. Seleziona un numero tra 1 e", len(piatti))

    piatto_scelto = piatti[scelta - 1]
    print(f"Hai scelto di votare per {piatto_scelto['nome']}")

    # Chiedi all'utente di dare un voto alla pietanza scelta
    while True:
        voto = input("Vota il piatto da 1 a 5: ")
        try:
            voto = int(voto)
            if voto < 1 or voto > 5:
                raise ValueError()
            break
        except ValueError:
            print("Input non valido. Inserisci un valore numerico tra 0 e 5.")

    # Aggiorna il voto del piatto selezionato
    if piatto_scelto["nome"] in voti:
        voti[piatto_scelto["nome"]] = voto
    else:
        voti.update({piatto_scelto["nome"]: voto})

    # Scrivi i voti sul file
    with open(voti_file, "w") as f:
        json.dump(voti, f)

    print("Voto registrato con successo!")


def getnutrizione(nome_piatto, categoria):
    global cas
    with open("pietanze/"f"{categoria}", "r") as f:
        piatti = json.load(f)
    n_pietanze = len(piatti['piatti'])
    for i in range(0, n_pietanze):
        if piatti['piatti'][i]["nome"] == nome_piatto:
            return piatti['piatti'][cas]["nutrizione"]


def getinfonutrizione(calorie, proteine, grassi, carboidrati, fibra, piatto, categoria):
    piatto_info = getnutrizione(piatto, categoria)
    calorie += piatto_info["calorie"]
    proteine += piatto_info["proteine"]
    grassi += piatto_info["grassi"]
    carboidrati += piatto_info["carboidrati"]
    fibra += piatto_info["fibra"]
    return {
        "calorie": calorie,
        "proteine": proteine,
        "grassi": grassi,
        "carboidrati": carboidrati,
        "fibra": fibra
    }


def __main__():
    accesso = True
    while accesso:
        accesso = login() 
        
    while True:
        print("\nBenvenuto nel menù di selezione!")
        print("1. Crea un menu settimanale")
        print("2. Visualizza un menu")
        print("3. Cerca un piatto da un ingrediente")
        print("4. Cerca gli ingredienti di un piatto")
        print("5. Visualizza i sughi disponibili")
        print("6. Visualizza i piatti di carne")
        print("7. Visualizza i piatti di pesce")
        print("8. Visualizza le colazioni disponibili")
        print("9. Visualizza i contorni disponibili")
        print("10. Visualizza le merende disponibili")
        print("11. Stila la lista della spesa per l'ultimo menù creato")
        print("12. Vota una pietanza")
        print("13. Chiudi il programma")
        choice = input("\nCosa vuoi fare? ")
        if choice == "1":
            generate_weekly_menu()
        elif choice == "2":
            apri_menu(visualizza_vecchi_menu())
        elif choice == "3":
            ingrediente = input("\nInserisci l'ingrediente:")
            print(ricerca_per_ingrediente(ingrediente))
        elif choice == "4":
            nome_piatto = input("\nInserisci il nome del piatto:")
            print(ricerca_per_piatto(nome_piatto))
        elif choice == "5":
            visualizza_sughi()
        elif choice == "6":
            visualizza_carni()
        elif choice == "7":
            visualizza_pesci()
        elif choice == "8":
            visualizza_colazione()
        elif choice == "9":
            visualizza_contorni()
        elif choice == "10":
            visualizza_merenda()
        elif choice == "11":
            crea_lista_della_spesa(None)
        elif choice == "12":
            vota_pietanza()
        elif choice == "13":
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida. Riprova.")


__main__()
