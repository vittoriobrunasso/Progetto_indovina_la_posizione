import socket
import random
import pickle

def spiega_regole():
    print("Benvenuto al gioco della Pallina Nascosta!")
    print("L'obiettivo del gioco è indovinare la posizione della pallina nascosta e di non far indovinare la tua...")
    print("Le coordinate della griglia vanno da 0 a 4.")
    print("Ogni turno, inserisci le coordinate per indovinare e nascondi la tua pallina.")
    print("Il tuo avversario farà lo stesso. Buona fortuna!\n")

def visualizza_griglia(riga_pallina, colonna_pallina, riga_giocatore, colonna_giocatore):
    for i in range(5):
        for j in range(5):
            if i == riga_giocatore and j == colonna_giocatore:
                print(" O ", end="")
            elif i == riga_pallina and j == colonna_pallina:
                print(" P ", end="")
            else:
                print(" . ", end="")
        print()

def gestisci_turno(client_socket, riga, colonna, riga_pallina, colonna_pallina):
    visualizza_griglia(riga_pallina, colonna_pallina, riga, colonna)

    tupla = (riga, colonna)
    dati = pickle.dumps(tupla)
    client_socket.send(dati)
    risultato = client_socket.recv(1024).decode()
    print(risultato)
    if risultato == "Hai indovinato":
        return 3
    else:
        return 0

def gestisci_turno2(client_socket, riga, colonna):
    while True:
        try:
            riga_avversario = int(input("Inserisci la riga per posizionare la pallina (da 0 a 4): "))
            colonna_avversario = int(input("Inserisci la colonna per posizionare la pallina (da 0 a 4): "))

            if 0 <= riga_avversario <= 4 and 0 <= colonna_avversario <= 4:
                break
            else:
                print("Coordinate non valide. Riprova.")
        except ValueError:
            print("Inserisci un numero valido.")

    visualizza_griglia(riga_avversario, colonna_avversario, riga_avversario, colonna_avversario)
    print(f"Client ha nascosto la pallina alla riga {riga_avversario}, colonna {colonna_avversario}")

    if (riga, colonna) == (riga_avversario, colonna_avversario):
        client_socket.send("Hai indovinato!".encode())
        return 0
    else:
        client_socket.send(f"Non hai indovinato. {riga_avversario},{colonna_avversario}".encode())
        return 1

def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        spiega_regole()
        print("Messaggio iniziale:", client_socket.recv(1024).decode())

        punteggio_totale = 0

        for turno in range(1, 4):
            print("\nROUND", turno)
            print("\nIl tuo avversario ha posizionato la pallina")

            print("\nInserisci le tue coordinate per indovinare la posizione della pallina:")
            while True:
                try:
                    riga_indovinare = int(input("Inserisci la riga (da 0 a 4): "))
                    colonna_indovinare = int(input("Inserisci la colonna (da 0 a 4): "))

                    if 0 <= riga_indovinare <= 4 and 0 <= colonna_indovinare <= 4:
                        break
                    else:
                        print("Coordinate non valide. Riprova.")
                except ValueError:
                    print("Inserisci un numero valido.")

            punteggio_turno = gestisci_turno(client_socket, riga_indovinare, colonna_indovinare, riga_indovinare, colonna_indovinare)
            punteggio_totale += punteggio_turno

            print("Attendo le coordinate del server")
            dati = client_socket.recv(1024)
            tupla = pickle.loads(dati)
            riga_giocatore, colonna_giocatore = tupla

            punteggio_turno = gestisci_turno2(client_socket, riga_giocatore, colonna_giocatore)
            punteggio_totale += punteggio_turno

        # Ricevi e stampa il punteggio finale
        print("Punteggio finale client")
        print(punteggio_totale)

        client_socket.send(f"Punteggio finale: {punteggio_totale}".encode())
        print(client_socket.recv(1024).decode())

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
