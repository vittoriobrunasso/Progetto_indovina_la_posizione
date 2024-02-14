import socket
import random
import time
import pickle


def gestisci_turno(client_socket, riga, colonna):
    riga_avversario = random.randint(0, 4)
    colonna_avversario = random.randint(0, 4)

    print(riga_avversario, colonna_avversario)

    print(f"Server ha nascosto la pallina alla riga {riga_avversario}, colonna {colonna_avversario}")

    if (riga, colonna) == (riga_avversario, colonna_avversario):
        client_socket.send("Hai indovinato!".encode())
        return 0
    else:
        client_socket.send(f"Non hai indovinato. {riga_avversario},{colonna_avversario}".encode())
        return 1


def gestisci_turno2(client_socket, riga, colonna):
    tupla = (riga, colonna)
    dati = pickle.dumps(tupla)
    client_socket.send(dati)
    risultato = client_socket.recv(1024).decode()
    print(risultato)
    if risultato == "Hai indovinato":
        return 3
    else:
        return 0


def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    riga_pallina = random.randint(0, 4)
    colonna_pallina = random.randint(0, 4)

    print("In attesa di connessione dall'avversario...")
    client_socket, addr = server_socket.accept()
    print("Connessione stabilita con l'avversario", addr)

    try:
        client_socket.send("Messaggio iniziale: Connessione stabilita".encode())

        punteggio_totale = 0

        for turno in range(1, 4):
            print("\nROUND", turno)
            print("\nIl tuo avversario ha posizionato la pallina")

            print("\nIn attesa delle coordinate del client per indovinare la posizione della pallina...")
            dati = client_socket.recv(1024)
            tupla = pickle.loads(dati)
            riga_giocatore, colonna_giocatore = tupla


            punteggio_turno = gestisci_turno(client_socket, riga_giocatore, colonna_giocatore)
            punteggio_totale += punteggio_turno


            print("Provo ad indovinare dove il client ha posizionato la pallina")
            punteggio_turno = gestisci_turno2(client_socket, riga_pallina,  colonna_pallina)
            punteggio_totale += punteggio_turno

        # Invio del punteggio finale al
        print("Punteggio finale server")
        print(punteggio_totale)

        punteggio = client_socket.recv(1024).decode()
        punteggio_client = int(punteggio.split(":")[1].strip())

        if punteggio_totale < punteggio_client:
            client_socket.send("Il client ha vinto".encode())
        elif punteggio_totale > punteggio_client:
            client_socket.send("Il server ha vinto".encode())
        else:
            client_socket.send("Parità".encode())

    finally:
        client_socket.close()
        server_socket.close()


if __name__ == "__main__":
    main()
